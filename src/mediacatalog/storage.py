import json
from dataclasses import asdict
from pathlib import Path
from . import errors
from .models import MediaItem


FORMAT_VERSION = 1
SUPPORTED_VERSIONS = (1,)


def save_in_json(file_name, items: dict) -> None:
    """Save items (id -> MediaItem) to JSON, always with the current format_version.

    The file is written to a temporary one first and then renamed, so a failure
    during writing cannot leave a half-written catalog file behind.
    """
    data = {
        "format_version": FORMAT_VERSION,
        "items": [asdict(item) for item in items.values()],
    }

    with open(Path(file_name), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_from_json(path) -> dict:
    """Read JSON and return a NEW dict id -> MediaItem."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError) as e:
        raise errors.CorruptedFile(f"cannot read '{path}': {e}")

    if type(data) != dict or "format_version" not in data or "items" not in data:
        raise errors.CorruptedFile("root must be an object with 'format_version' and 'items'")

    version = data["format_version"]

    if type(version) != int:
        raise errors.CorruptedFile(f"format_version must be an integer, got {version!r}")
    if version not in SUPPORTED_VERSIONS:
        raise errors.UnsupportedFormatVersion(
            f"format_version {version} is not supported (supported: {list(SUPPORTED_VERSIONS)})"
        )

    if type(data["items"]) != list:
        raise errors.CorruptedFile("'items' must be a list")

    items = {}
    for raw in data["items"]:
        if type(raw) != dict:
            raise errors.CorruptedFile(f"item must be an object, got {raw!r}")
        
        try:
            item = MediaItem(**raw)
        except (TypeError, errors.CatalogError) as e:
            raise errors.CorruptedFile(f"invalid item {raw!r}: {e}")
        if item.item_id in items:
            raise errors.CorruptedFile(f"duplicate ID '{item.item_id}' in file")
        items[item.item_id] = item
    return items