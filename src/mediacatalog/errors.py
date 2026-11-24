class CatalogError(ValueError):
    pass

class IncorrectType(CatalogError):
    pass

class ExistingID(CatalogError):
    pass

class ItemNotFound(CatalogError):
    pass