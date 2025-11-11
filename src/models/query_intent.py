"""
Query Intent - Data class for parsed natural language query intent
"""
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class QueryIntent:
    """
    Represents the parsed intent from a natural language query.
    
    Attributes:
        intent_type: Type of query (homework_status, performance, upcoming_quizzes, general)
        filters: Dictionary of filter criteria extracted from the query
        confidence: Confidence score of the parsing (0.0 to 1.0)
    """
    intent_type: str
    filters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    
    def __str__(self) -> str:
        """String representation of the query intent."""
        return f"Intent: {self.intent_type}, Filters: {self.filters}, Confidence: {self.confidence:.2f}"
