"""
JSON Data Repository - Concrete implementation for JSON file data source
"""
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Optional
from .data_repository import DataRepository


class JSONDataRepository(DataRepository):
    """
    Concrete implementation of DataRepository for JSON files.
    """
    
    def __init__(self, data_file_path: str):
        """
        Initialize the JSON data repository.
        
        Args:
            data_file_path: Path to the JSON data file
        """
        self.data_file_path = Path(data_file_path)
        self._data_cache = None
        
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all data from JSON file.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all data tables
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            json.JSONDecodeError: If JSON is malformed
        """
        if self._data_cache is not None:
            return self._data_cache
            
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert to DataFrames
            self._data_cache = {
                'students': pd.DataFrame(data.get('students', [])),
                'homework': pd.DataFrame(data.get('homework', [])),
                'quizzes': pd.DataFrame(data.get('quizzes', [])),
                'performance': pd.DataFrame(data.get('performance', []))
            }
            
            # Convert date columns to datetime
            if not self._data_cache['homework'].empty:
                self._data_cache['homework']['due_date'] = pd.to_datetime(
                    self._data_cache['homework']['due_date']
                )
                self._data_cache['homework']['submission_date'] = pd.to_datetime(
                    self._data_cache['homework']['submission_date'], errors='coerce'
                )
            
            if not self._data_cache['quizzes'].empty:
                self._data_cache['quizzes']['scheduled_date'] = pd.to_datetime(
                    self._data_cache['quizzes']['scheduled_date']
                )
            
            if not self._data_cache['performance'].empty:
                self._data_cache['performance']['date'] = pd.to_datetime(
                    self._data_cache['performance']['date']
                )
            
            return self._data_cache
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.data_file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in data file: {e.msg}", e.doc, e.pos)
    
    def get_students(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get student records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered student records
        """
        data = self.load_data()
        df = data['students'].copy()
        
        if filters:
            df = self._apply_filters(df, filters)
        
        return df
    
    def get_homework(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get homework records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered homework records
        """
        data = self.load_data()
        df = data['homework'].copy()
        
        if filters:
            df = self._apply_filters(df, filters)
        
        return df
    
    def get_quizzes(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get quiz records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered quiz records
        """
        data = self.load_data()
        df = data['quizzes'].copy()
        
        if filters:
            df = self._apply_filters(df, filters)
        
        return df
    
    def get_performance(self, filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Get performance records with optional filters.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered performance records
        """
        data = self.load_data()
        df = data['performance'].copy()
        
        if filters:
            df = self._apply_filters(df, filters)
        
        return df
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """
        Apply filters to a DataFrame.
        
        Args:
            df: DataFrame to filter
            filters: Dictionary of filter criteria
            
        Returns:
            pd.DataFrame: Filtered DataFrame
        """
        for key, value in filters.items():
            if key in df.columns:
                if isinstance(value, list):
                    df = df[df[key].isin(value)]
                else:
                    df = df[df[key] == value]
        
        return df
