"""
Role Manager - Manages admin roles and access control
"""
import json
from pathlib import Path
from typing import List, Optional
from src.models.admin_role import AdminRole


class RoleManager:
    """
    Manages admin roles and provides access to role configurations.
    """
    
    def __init__(self, roles_file_path: str):
        """
        Initialize the role manager.
        
        Args:
            roles_file_path: Path to the admin roles JSON file
        """
        self.roles_file_path = Path(roles_file_path)
        self._roles_cache = None
    
    def load_admin_role(self, admin_id: str) -> Optional[AdminRole]:
        """
        Load a specific admin role by ID.
        
        Args:
            admin_id: The admin's unique identifier
            
        Returns:
            AdminRole: The admin role object, or None if not found
        """
        roles = self._load_all_roles()
        
        for role_data in roles:
            if role_data['admin_id'] == admin_id:
                return AdminRole(
                    admin_id=role_data['admin_id'],
                    name=role_data['name'],
                    scope_type=role_data['scope_type'],
                    scope_values=role_data['scope_values']
                )
        
        return None
    
    def get_all_admins(self) -> List[AdminRole]:
        """
        Get all admin roles.
        
        Returns:
            List[AdminRole]: List of all admin roles
        """
        roles = self._load_all_roles()
        
        return [
            AdminRole(
                admin_id=role['admin_id'],
                name=role['name'],
                scope_type=role['scope_type'],
                scope_values=role['scope_values']
            )
            for role in roles
        ]
    
    def _load_all_roles(self) -> List[dict]:
        """
        Load all roles from the JSON file.
        
        Returns:
            List[dict]: List of role dictionaries
            
        Raises:
            FileNotFoundError: If roles file doesn't exist
            json.JSONDecodeError: If JSON is malformed
        """
        if self._roles_cache is not None:
            return self._roles_cache
        
        try:
            with open(self.roles_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._roles_cache = data.get('admins', [])
            return self._roles_cache
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Roles file not found: {self.roles_file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in roles file: {e.msg}", e.doc, e.pos)
