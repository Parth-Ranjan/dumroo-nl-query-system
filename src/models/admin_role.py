"""
Admin Role - Data class for admin user roles and access scope
"""
from dataclasses import dataclass
from typing import List


@dataclass
class AdminRole:
    """
    Represents an admin user's role and access scope.
    
    Attributes:
        admin_id: Unique identifier for the admin
        name: Admin's display name
        scope_type: Type of scope (grade, class, region)
        scope_values: List of values defining the scope (e.g., ["8", "9"] for grades)
    """
    admin_id: str
    name: str
    scope_type: str  # 'grade', 'class', or 'region'
    scope_values: List[str]
    
    def __str__(self) -> str:
        """String representation of the admin role."""
        values_str = ", ".join(self.scope_values)
        return f"{self.name} (Scope: {self.scope_type.title()} - {values_str})"
