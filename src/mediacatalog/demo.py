from catalog import Catalog
from models import MediaItem


if __name__ == "__main__":
    catalog = Catalog()
    catalog.add(MediaItem("0", "sqwore", "music", 2023, "I", 92))
    catalog.add(MediaItem("1", "soltwine", "music", 2025, "I", 92))
    catalog.add(MediaItem("s1", "soltwine", "music", 2025, "I", 92))
    catalog.add(MediaItem("2", "Я легенда", "film", 1999, "I", 92))
    print("-"*100)
    print(catalog.find_by_category("music"))
    catalog.remove("s2")
    print(catalog.find_by_category("music"))
    print(catalog.find_by_name("я легенда"))
    print("-"*100)
    print("len:", len(catalog))
    print("-"*100)
    for i in catalog:
        if "1" in i:
            print("FOUND", i)
        else:
            print(i)