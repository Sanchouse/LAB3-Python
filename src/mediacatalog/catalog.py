import errors
from models import MediaItem
from typing import Any, Iterator


class Catalog:
    """Catalog of media library items"""
    def __init__(self, json_file_input={}, json_file_output="output.json"):
        """Initialization of catalog"""

        if json_file_input:
            pass
        else:
            self.items = {}

    def add(self, item: MediaItem) -> None:
        """Add item in catalog"""

        item_id, item_value = item.for_dict()

        if type(item) == MediaItem:
            if item_id in self.items:
                raise errors.ExistingID(f"ID '{item_id}' already exists")
            
            check_type(item_id, item_value)
            self.items[item_id] = item_value
        else:
            raise errors.IncorrectType(f"type of item '{type(item)}' not MediaItem.")

    def get(self, item_id: str) -> MediaItem:
        """Get item in catalog by id"""
        return [item for item in self.items if item]

    def remove(self, item_id:str) -> Any:
        """Remove item from catalog by id"""
        try:
            return self.items.pop(item_id)
        except:
            print("There is no such ID.")
            return ""

    def find_by_category(self, category:str) -> dict:
        """Find an item by category"""

        ids = {}
        for item_id, item in self.items.items():
            if item["category"].lower() == category.lower():
                ids[item_id] = item
        return ids

    def find_by_name(self, query:str) -> dict:
        """Find an item by name"""

        ids = {}
        for item_id, item in self.items.items():
            if item["name"].lower() == query.lower():
                ids[item_id] = item
        return ids

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator:
        return iter(self.items.items())

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
