from dataclasses import dataclass
from datetime import date
import errors

MIN_YEAR = 1850

def parse_text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise errors.IncorrectType(f"{name}: A non‑empty string is required, but received {value!r}")

def parse_number(name, value, low, high=None):
    if not isinstance(value, int):
        raise errors.IncorrectType(f"{name}: An integer is required, but received {value!r}")
    if value < low or (high is not None and value > high):
        raise errors.IncorrectType(f"{name}: value {value} outside the permissible range")


@dataclass(frozen=True)
class MediaItem:
    item_id: str
    name: str
    category: str
    year: int
    creator: str
    duration_minutes: int

    def __post_init__(self) -> None:
        parse_text("item_id", self.item_id)
        parse_text("name", self.name)
        parse_text("category", self.category)
        parse_number("year", self.year, MIN_YEAR, date.today().year)
        parse_text("creator", self.creator)
        parse_number("duration_minutes", self.duration_minutes, 1)

    def for_dict(self) -> tuple[str, dict]:
        return (self.item_id, {"id": self.item_id, "name": self.name, "category": self.category, "year": self.year, "creator": self.creator, "duration in minutes": self.duration_minutes})