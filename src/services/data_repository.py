"""
Data Repository - Abstract base class for data access
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Optional


class DataRepository(ABC):
    """
    Abstract base class for data repository.
    Defines interface for data access operations.
    """
    
    @abstractmethod
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all data from the data source.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all data tables
        """
        pass
    
    @abstractmethod
    def get_students(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get student records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered student records
        """
        pass
    
    @abstractmethod
    def get_homework(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get homework records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered homework records
        """
        pass
    
    @abstractmethod
    def get_quizzes(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get quiz records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered quiz records
        """
        pass
    
    @abstractmethod
    def get_performance(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get performance records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered performance records
        """
        pass
