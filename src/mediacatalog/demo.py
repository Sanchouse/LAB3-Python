from .catalog import Catalog
from .models import MediaItem


if __name__ == "__main__":
    catalog = Catalog()
    catalog.load("../data/out.json")
    catalog.add(MediaItem("9", "111", "music", 2024, "sqwore", 3))
    catalog.add(MediaItem("10", "аквариум", "music", 2022, "sqwore", 2))
    catalog.save("../data/output.json")
    catalog.add(MediaItem("11", "Рандеву", "music", 2023, "soltwine", 4))
    catalog.add(MediaItem("12", "Я легенда", "film", 1999, "I", 92))
    catalog.save("../data/output.json")
    print("-"*100)
    print(catalog.find_by_category("music"))
    catalog.remove("11")
    print(catalog.find_by_category("music"))
    print(catalog.find_by_name("я легенда"))
    print("-"*100)
    print(catalog.get("10"))
    print("len:", len(catalog))
    print("-"*100)
    for i in catalog:
        if "1" in i.item_id:
            print("FOUND", i)
        else:
            print(i)