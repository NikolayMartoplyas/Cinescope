from enum import Enum

class RolesEnum(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class LocationEnum(str, Enum):
    SPB = "SPB"
    MSK = "MSK"
