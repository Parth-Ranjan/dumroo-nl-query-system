"""
Configuration settings for the NL Query System
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'

# Data file paths
SCHOOL_DATA_PATH = DATA_DIR / 'school_data.json'
ADMIN_ROLES_PATH = DATA_DIR / 'admin_roles.json'

# OpenAI configuration
# Try Streamlit secrets first, then fall back to environment variables
try:
    import streamlit as st
    if "OPENAI_API_KEY" in st.secrets:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
        OPENAI_MODEL = st.secrets.get("OPENAI_MODEL", "gpt-3.5-turbo")
    else:
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
except Exception:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

# Supported intent types
INTENT_TYPES = [
    'homework_status',
    'performance',
    'upcoming_quizzes',
    'general'
]

# Example queries for UI
EXAMPLE_QUERIES = [
    "Which students haven't submitted their homework yet?",
    "Show me performance data for Grade 8 from last week",
    "List all upcoming quizzes scheduled for next week",
    "Who submitted the Math Chapter 5 assignment?",
    "Show me all students in my scope",
    "What are the quiz scores for my classes?"
]
