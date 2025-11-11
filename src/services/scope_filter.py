"""
Scope Filter - Applies role-based access control to data
"""
import pandas as pd
from src.models.admin_role import AdminRole


class ScopeFilter:
    """
    Applies access control filters based on admin role scope.
    Ensures admins can only access data within their assigned scope.
    """
    
    @staticmethod
    def apply_scope(data: pd.DataFrame, admin: AdminRole) -> pd.DataFrame:
        """
        Apply scope filtering to a DataFrame based on admin role.
        
        Args:
            data: DataFrame to filter
            admin: AdminRole defining the access scope
            
        Returns:
            pd.DataFrame: Filtered DataFrame containing only data within scope
        """
        if data.empty:
            return data
        
        # Determine which column to filter on based on scope type
        scope_column = None
        
        if admin.scope_type == 'grade' and 'grade' in data.columns:
            scope_column = 'grade'
        elif admin.scope_type == 'class' and 'class' in data.columns:
            scope_column = 'class'
        elif admin.scope_type == 'region' and 'region' in data.columns:
            scope_column = 'region'
        
        # If the scope column doesn't exist in this data, return empty DataFrame
        # This prevents data leakage
        if scope_column is None:
            return pd.DataFrame(columns=data.columns)
        
        # Convert scope values to appropriate type
        if scope_column == 'grade':
            # Convert grade scope values to integers for comparison
            scope_values = [int(v) for v in admin.scope_values]
        else:
            scope_values = admin.scope_values
        
        # Filter data to only include rows within scope
        filtered_data = data[data[scope_column].isin(scope_values)].copy()
        
        return filtered_data
    
    @staticmethod
    def validate_access(query_params: dict, admin: AdminRole) -> bool:
        """
        Validate if a query's parameters are within the admin's scope.
        
        Args:
            query_params: Dictionary of query parameters
            admin: AdminRole defining the access scope
            
        Returns:
            bool: True if access is allowed, False otherwise
        """
        # If no specific scope parameters in query, allow (will be filtered by apply_scope)
        if admin.scope_type not in query_params:
            return True
        
        # Check if requested values are within admin's scope
        requested_values = query_params[admin.scope_type]
        if not isinstance(requested_values, list):
            requested_values = [requested_values]
        
        # Convert to strings for comparison
        requested_values = [str(v) for v in requested_values]
        
        # Check if all requested values are in admin's scope
        return all(val in admin.scope_values for val in requested_values)
