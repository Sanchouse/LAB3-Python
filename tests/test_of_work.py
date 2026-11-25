import json
import pytest

import mediacatalog.errors as err
from mediacatalog.catalog import Catalog
from mediacatalog.models import MediaItem
from mediacatalog.storage import FORMAT_VERSION


def make_item(item_id="1", name="Выздороветь", category="music",
              year=2025, creator="soltwine", duration_minutes=3):
    return MediaItem(item_id, name, category, year, creator, duration_minutes)


@pytest.fixture
def catalog():
    c = Catalog()
    c.add(make_item("1", "111", "music", 2024, "sqwore", 2))
    c.add(make_item("2", "корабли ходят по небу", "music", 2024, "sqwore", 3))
    c.add(make_item("3", "Я легенда", "film", 2007, "Francis Lawrence", 96))
    return c


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


class TestCatalog:
    def test_valid_item_with_required_id(self):
        item = make_item()
        assert item.item_id == "1" and item.name == "Выздороветь" and item.category == "music" and item.year == 2025 and item.creator == "soltwine" and item.duration_minutes == 3

    @pytest.mark.parametrize("kwargs", [{"item_id": ""},
        {"name": None},
        {"year": 1700},
        {"year": True},
        {"duration_minutes": -1}
    ])
    def test_invalid_item_is_not_created(self, kwargs):
        with pytest.raises(err.IncorrectType):
            make_item(**kwargs)

    def test_add_and_get(self):
        c = Catalog()
        item = make_item()
        c.add(item)
        assert c.get("1") == item
        assert len(c) == 1
        assert "1" in c
        assert "nope" not in c

    def test_get_missing_raises(self, catalog):
        with pytest.raises(err.ItemNotFound):
            catalog.get("nope")

    def test_remove_returns_item_and_deletes(self, catalog):
        removed = catalog.remove("2")
        assert removed.name == "корабли ходят по небу"
        assert "2" not in catalog
        assert len(catalog) == 2

    def test_remove_missing_raises(self, catalog):
        with pytest.raises(err.ItemNotFound):
            catalog.remove("nope")
        assert len(catalog) == 3

    def test_duplicate_id_forbidden(self, catalog):
        with pytest.raises(err.ExistingID):
            catalog.add(make_item("1", "Other", "film", 2000, "Z", 5))
        assert len(catalog) == 3
        assert catalog.get("1").name == "111"
    
    def test_find_by_category_case_insensitive(self, catalog):
        found = catalog.find_by_category("MUSIC")
        assert [i.item_id for i in found] == ["1", "2"]
        assert catalog.find_by_category("book") == []

    def test_find_by_name_case_insensitive(self):
        c = Catalog()
        c.add(make_item("1", "Я легенда", "film", 2007, "Francis Lawrence", 96))
        c.add(make_item("2", "бардак", "music", 2024, "sqwore", 3))
        assert [i.item_id for i in c.find_by_name("я ЛЕГЕНДА")] == ["1"]
        assert [i.item_id for i in c.find_by_name("бАрДаК")] == ["2"]
        assert c.find_by_name("omagad") == []

    def test_search_returns_copy_not_internal_structure(self, catalog):
        result = catalog.find_by_category("music")
        result.clear()
        assert len(catalog) == 3
        assert len(catalog.find_by_category("music")) == 2


    def test_iteration_order_is_insertion_order(self, catalog):
        assert [i.item_id for i in catalog] == ["1", "2", "3"]
        catalog.remove("2")
        catalog.add(make_item("4", "I can't scream but I must", "book", 2002, "idk", 20))
        assert [i.item_id for i in catalog] == ["1", "3", "4"]


    def test_round_trip_json(self, tmp_path, catalog):
        path = tmp_path / "catalog.json"
        catalog.save(path)

        loaded = Catalog()
        loaded.load(path)

        assert list(loaded) == list(catalog)

    def test_saved_file_has_format_version(self, tmp_path, catalog):
        path = tmp_path / "catalog.json"
        catalog.save(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["format_version"] == FORMAT_VERSION == 1
        assert len(data["items"]) == 3


    def test_corrupted_json_raises(self, tmp_path):
        path = tmp_path / "bad.json"
        path.write_text("{not json", encoding="utf-8")
        with pytest.raises(err.CorruptedFile):
            Catalog().load(path)

    def test_file_not_json(self, tmp_path):
        path = tmp_path / "bad.csv"
        with pytest.raises(err.CorruptedFile):
            Catalog().load(path)

    @pytest.mark.parametrize("data", [
        {"items": []},
        {"format_version": 1, "items": {}},
        {"format_version": 1, "items": [
            {"item_id": "1", "name": "", "category": "music",
             "year": 2020, "creator": "A", "duration_minutes": 3}]},
        {"format_version": 1, "items": [
            {"item_id": "1", "name": "A"}]},
    ])
    def test_wrong_content_raises_corrupted(self, tmp_path, data):
        path = tmp_path / "c.json"
        write_json(path, data)
        with pytest.raises(err.CorruptedFile):
            Catalog().load(path)

    def test_unsupported_version_raises(self, tmp_path):
        path = tmp_path / "v2.json"
        write_json(path, {"format_version": 2, "items": []})
        with pytest.raises(err.UnsupportedFormatVersion):
            Catalog().load(path)
    
    def test_corrupted_json_keeps_catalog(self, tmp_path, catalog):
        before = list(catalog)
        path = tmp_path / "bad.json"
        path.write_text("{not json", encoding="utf-8")

        with pytest.raises(err.CorruptedFile):
            catalog.load(path)

        assert list(catalog) == before

    def test_unsupported_version_keeps_catalog(self, tmp_path, catalog):
        before = list(catalog)
        path = tmp_path / "v2.json"
        write_json(path, {"format_version": 2, "items": []})

        with pytest.raises(err.UnsupportedFormatVersion):
            catalog.load(path)

        assert list(catalog) == before

    def test_valid_first_and_invalid_second_item_keeps_catalog(self, tmp_path, catalog):
        """The first valid record must not leak into the catalog."""
        before = list(catalog)
        path = tmp_path / "c.json"
        write_json(path, {"format_version": 1, "items": [
            {"item_id": "new", "name": "Good", "category": "music",
             "year": 2020, "creator": "A", "duration_minutes": 3},
            {"item_id": "bad", "name": "Bad", "category": "music",
             "year": 1700, "creator": "A", "duration_minutes": 3},
        ]})

        with pytest.raises(err.CorruptedFile):
            catalog.load(path)

        assert list(catalog) == before
        assert "new" not in catalog