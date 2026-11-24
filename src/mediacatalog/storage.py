import json
from pathlib import Path

def save_in_json(file_name, items):
    data = {item_id: item.for_dict()[1] for item_id, item in items.items()}
    with open(Path(file_name), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_from_json(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)