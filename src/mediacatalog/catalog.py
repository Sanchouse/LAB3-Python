import errors
from models import MediaItem
from typing import Any, Iterator
from storage import load_from_json, save_in_json



class Catalog:
    """Catalog of media library items"""
    def __init__(self, json_file_output=""):
        """Initialization of catalog"""

        if json_file_output:
            self.json_file_output = "../data/" + json_file_output
            self.items = load_from_json(self.json_file_output)
        else:
            self.json_file_output = "../data/output.json"
            self.items = {}

    def add(self, item: MediaItem) -> None:
        """Add item in catalog"""

        if type(item) == MediaItem:
            check_type(*item.for_dict())
            if item.item_id in self.items:
                raise errors.ExistingID(f"ID '{item.item_id}' already exists")
            self.items[item.item_id] = item
        else:
            raise errors.IncorrectType(f"type of item '{type(item)}' not MediaItem.")

        save_in_json(self.json_file_output, self.items)

    def get(self, item_id: str) -> MediaItem:
        """Get item in catalog by id"""
        try:
            return self.items[item_id]
        except KeyError:
            raise errors.ItemNotFound(f"ID '{item_id}' not in catalog")

    def remove(self, item_id:str) -> Any:
        """Remove item from catalog by id"""
        try:
            item = self.items.pop(item_id)
            save_in_json(self.json_file_output, self.items)
            return item
        except KeyError:
            raise errors.ItemNotFound(f"ID '{item_id}' not in catalog")

    def find_by_category(self, category:str) -> list[MediaItem]:
        """Find an item by category"""
        return [i for i in self.items.values() if i.category.lower() == category.lower()]

    def find_by_name(self, query:str) -> list[MediaItem]:
        """Find an item by name"""
        return [i for i in self.items.values() if i.name.lower() == query.lower()]

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[MediaItem]:
        """Objects in the order of addition."""
        return iter(list(self.items.values()))

    def __contains__(self, item_id:str) -> bool:
        return item_id in self.items 





def check_type(item_id:str, item_value:dict) -> None:
    """Check types of data"""
    if type(item_id) != str:
        raise errors.IncorrectType(f"type of id '{type(item_id)}' not 'str'.")
    if type(item_value["name"]) != str:
        raise errors.IncorrectType(f"type of name '{type(item_id)}' not 'str'.")
    if type(item_value["category"]) != str:
        raise errors.IncorrectType(f"type of category '{type(item_id)}' not 'str'.")
    if type(item_value["year"]) != int:
        raise errors.IncorrectType(f"type of year '{type(item_id)}' not 'int'.")
    if type(item_value["creator"]) != str:
        raise errors.IncorrectType(f"type of creator '{type(item_id)}' not 'str'.")
    if type(item_value["duration in minutes"]) != int:
        raise errors.IncorrectType(f"type of duration in minutes '{type(item_id)}' not 'int'.")
