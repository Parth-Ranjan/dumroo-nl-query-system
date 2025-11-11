"""
Natural Language Query Parser - Uses LangChain and OpenAI to parse queries
"""
import os
import json
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.models.query_intent import QueryIntent


class NLQueryParser:
    """
    Parses natural language queries using LangChain and OpenAI.
    Extracts intent and filters from user questions.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the NL query parser.
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided and not found in environment")
        
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=0
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a query parser for an educational admin system.
Your job is to parse natural language questions and extract structured information.

Parse the question and identify:
1. Intent type: Choose ONE from these options:
   - "homework_status": Questions about homework submissions, who submitted, who didn't submit
   - "performance": Questions about grades, scores, quiz results, academic performance
   - "upcoming_quizzes": Questions about scheduled quizzes, upcoming tests
   - "general": Any other questions

2. Filters: Extract any of these if mentioned:
   - grade: Grade level (e.g., 6, 7, 8, 9, 10)
   - class: Class name (e.g., "8A", "9B")
   - region: Region name (e.g., "North", "South")
   - status: Submission status ("submitted", "not_submitted", "pending")
   - date_range: Time period mentioned (e.g., "last week", "next week", "upcoming")
   - student_name: Specific student name if mentioned

Return ONLY a valid JSON object with this exact structure:
{{
  "intent_type": "one of the intent types above",
  "filters": {{
    "key": "value"
  }},
  "confidence": 0.95
}}

Do not include any explanation, just the JSON."""),
            ("user", "{question}")
        ])
    
    def parse_query(self, question: str) -> QueryIntent:
        """
        Parse a natural language question into a QueryIntent.
        
        Args:
            question: The natural language question
            
        Returns:
            QueryIntent: Parsed intent with filters
            
        Raises:
            Exception: If parsing fails or API error occurs
        """
        try:
            # Create the prompt
            messages = self.prompt_template.format_messages(question=question)
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            
            # Parse the JSON response
            result = json.loads(response.content)
            
            # Create QueryIntent object
            intent = QueryIntent(
                intent_type=result.get('intent_type', 'general'),
                filters=result.get('filters', {}),
                confidence=result.get('confidence', 0.8)
            )
            
            return intent
            
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return a general intent
            return QueryIntent(
                intent_type='general',
                filters={},
                confidence=0.3
            )
        except Exception as e:
            # For any other error, re-raise with context
            raise Exception(f"Error parsing query: {str(e)}")
