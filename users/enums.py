from enum import Enum

class UserRole(Enum):
    """Enums for user role definitions"""

    ADMIN = "admin"
    EMPLOYEE = "employee"

    @classmethod
    def choices(cls):
        """method that return list of tuple for role choices"""
        return [(role.value, role.name.capitalize()) for role in cls]