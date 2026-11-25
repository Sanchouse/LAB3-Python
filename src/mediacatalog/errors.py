class CatalogError(ValueError):
    """Base class for all catalog errors."""


class IncorrectType(CatalogError):
    """Invalid entity (wrong type or value of a field)."""


class ExistingID(CatalogError):
    """Item with this ID already exists in the catalog."""


class ItemNotFound(CatalogError):
    """Item with this ID is not in the catalog."""


class UnsupportedFormatVersion(CatalogError):
    """File has a format_version the loader cannot read."""


class CorruptedFile(CatalogError):
    """File is unreadable or has an invalid structure."""