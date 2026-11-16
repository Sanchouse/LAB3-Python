from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MediaItem:
    item_id: str
    name: str
    category: str
    year: int
    creator: str
    duration_minutes: int

    def for_dict(self):
        return (self.item_id, {"name": self.name, "category": self.category, "year": self.year, "creator": self.creator, "duration in minutes": self.duration_minutes})