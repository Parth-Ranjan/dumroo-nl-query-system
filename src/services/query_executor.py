"""
Query Executor - Executes parsed queries and returns results
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from src.models.query_intent import QueryIntent
from src.models.admin_role import AdminRole
from src.services.data_repository import DataRepository
from src.services.scope_filter import ScopeFilter


class QueryExecutor:
    """
    Executes queries based on parsed intent and applies access control.
    """
    
    def __init__(self, data_repository: DataRepository):
        """
        Initialize the query executor.
        
        Args:
            data_repository: Data repository instance for data access
        """
        self.data_repository = data_repository
        self.scope_filter = ScopeFilter()
    
    def execute(self, intent: QueryIntent, admin: AdminRole) -> pd.DataFrame:
        """
        Execute a query based on intent and admin scope.
        
        Args:
            intent: Parsed query intent
            admin: Admin role for access control
            
        Returns:
            pd.DataFrame: Query results filtered by admin scope
        """
        # Route to appropriate handler based on intent type
        if intent.intent_type == 'homework_status':
            return self._execute_homework_query(intent, admin)
        elif intent.intent_type == 'performance':
            return self._execute_performance_query(intent, admin)
        elif intent.intent_type == 'upcoming_quizzes':
            return self._execute_quiz_query(intent, admin)
        else:
            return self._execute_general_query(intent, admin)
    
    def _execute_homework_query(self, intent: QueryIntent, admin: AdminRole) -> pd.DataFrame:
        """Execute homework status query."""
        # Get homework data
        homework_df = self.data_repository.get_homework()
        
        # Apply scope filter
        homework_df = self.scope_filter.apply_scope(homework_df, admin)
        
        if homework_df.empty:
            return pd.DataFrame()
        
        # Apply status filter if specified
        if 'status' in intent.filters:
            status = intent.filters['status']
            homework_df = homework_df[homework_df['submission_status'] == status]
        
        # Get student information
        students_df = self.data_repository.get_students()
        students_df = self.scope_filter.apply_scope(students_df, admin)
        
        # Merge with student names
        result = homework_df.merge(
            students_df[['student_id', 'name']],
            on='student_id',
            how='left'
        )
        
        # Select and rename columns for display
        result = result[[
            'name', 'class', 'assignment_name', 
            'submission_status', 'due_date', 'submission_date'
        ]]
        result.columns = [
            'Student Name', 'Class', 'Assignment', 
            'Status', 'Due Date', 'Submission Date'
        ]
        
        return result
    
    def _execute_performance_query(self, intent: QueryIntent, admin: AdminRole) -> pd.DataFrame:
        """Execute performance/grades query."""
        # Get performance data
        performance_df = self.data_repository.get_performance()
        
        # Apply scope filter
        performance_df = self.scope_filter.apply_scope(performance_df, admin)
        
        if performance_df.empty:
            return pd.DataFrame()
        
        # Apply date range filter if specified
        if 'date_range' in intent.filters:
            performance_df = self._apply_date_filter(
                performance_df, 
                intent.filters['date_range'],
                'date'
            )
        
        # Get student and quiz information
        students_df = self.data_repository.get_students()
        students_df = self.scope_filter.apply_scope(students_df, admin)
        
        quizzes_df = self.data_repository.get_quizzes()
        quizzes_df = self.scope_filter.apply_scope(quizzes_df, admin)
        
        # Merge data
        result = performance_df.merge(
            students_df[['student_id', 'name']],
            on='student_id',
            how='left'
        )
        result = result.merge(
            quizzes_df[['quiz_id', 'quiz_name']],
            on='quiz_id',
            how='left'
        )
        
        # Calculate percentage
        result['percentage'] = (result['score'] / result['max_score'] * 100).round(2)
        
        # Select and rename columns
        result = result[[
            'name', 'class', 'quiz_name', 
            'score', 'max_score', 'percentage', 'date'
        ]]
        result.columns = [
            'Student Name', 'Class', 'Quiz', 
            'Score', 'Max Score', 'Percentage', 'Date'
        ]
        
        return result
    
    def _execute_quiz_query(self, intent: QueryIntent, admin: AdminRole) -> pd.DataFrame:
        """Execute upcoming quizzes query."""
        # Get quiz data
        quizzes_df = self.data_repository.get_quizzes()
        
        # Apply scope filter
        quizzes_df = self.scope_filter.apply_scope(quizzes_df, admin)
        
        if quizzes_df.empty:
            return pd.DataFrame()
        
        # Filter for upcoming quizzes (future dates)
        today = pd.Timestamp.now().normalize()
        
        if 'date_range' in intent.filters:
            date_range = intent.filters['date_range'].lower()
            if 'next week' in date_range or 'upcoming' in date_range:
                next_week = today + timedelta(days=7)
                quizzes_df = quizzes_df[
                    (quizzes_df['scheduled_date'] >= today) &
                    (quizzes_df['scheduled_date'] <= next_week)
                ]
            else:
                # Default to all future quizzes
                quizzes_df = quizzes_df[quizzes_df['scheduled_date'] >= today]
        else:
            # Default to all future quizzes
            quizzes_df = quizzes_df[quizzes_df['scheduled_date'] >= today]
        
        # Select and rename columns
        result = quizzes_df[[
            'quiz_name', 'scheduled_date', 'grade', 'class'
        ]].copy()
        result.columns = [
            'Quiz Name', 'Scheduled Date', 'Grade', 'Class'
        ]
        
        # Sort by date
        result = result.sort_values('Scheduled Date')
        
        return result
    
    def _execute_general_query(self, intent: QueryIntent, admin: AdminRole) -> pd.DataFrame:
        """Execute general query - return students in scope."""
        students_df = self.data_repository.get_students()
        students_df = self.scope_filter.apply_scope(students_df, admin)
        
        if students_df.empty:
            return pd.DataFrame()
        
        # Select and rename columns
        result = students_df[['name', 'grade', 'class', 'region']].copy()
        result.columns = ['Student Name', 'Grade', 'Class', 'Region']
        
        return result
    
    def _apply_date_filter(
        self, 
        df: pd.DataFrame, 
        date_range: str, 
        date_column: str
    ) -> pd.DataFrame:
        """
        Apply date range filter to DataFrame.
        
        Args:
            df: DataFrame to filter
            date_range: Date range string (e.g., "last week", "this month")
            date_column: Name of the date column to filter on
            
        Returns:
            pd.DataFrame: Filtered DataFrame
        """
        today = pd.Timestamp.now().normalize()
        date_range_lower = date_range.lower()
        
        if 'last week' in date_range_lower:
            start_date = today - timedelta(days=7)
            end_date = today
            df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
        elif 'this week' in date_range_lower:
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
        elif 'last month' in date_range_lower:
            start_date = today - timedelta(days=30)
            df = df[df[date_column] >= start_date]
        
        return df
