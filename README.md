# Dumroo AI - Natural Language Query System

A natural language query system for educational admin panels. Built for the Dumroo AI assignment, this system lets admins query student data using plain English while enforcing role-based access control.

## Features

- Natural language query processing using LangChain + OpenAI
- Role-based access control (grade/class/region scoping)
- Interactive Streamlit web interface
- Modular architecture for easy database integration
- Sample dataset with students, homework, quizzes, and performance data

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd DumrooAI
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure OpenAI API Key**

Create a `.env` file in the project root:
```bash
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### Running the Application

**Option 1: Using the batch file (Windows)**
```bash
run.bat
```

**Option 2: Using Streamlit directly**
```bash
streamlit run src\ui\streamlit_app.py
```

**Option 3: Using the main entry point**
```bash
python main.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage

### Example Queries

- "Which students haven't submitted their homework yet?"<img width="1913" height="916" alt="image" src="https://github.com/user-attachments/assets/fb0c33f6-096a-4a5c-a123-87da3495d71b" />

- "Show me performance data for Grade 8 from last week"<img width="1918" height="907" alt="image" src="https://github.com/user-attachments/assets/5306f296-539c-476f-982d-51d076cb35c1" />

- "List all upcoming quizzes scheduled for next week"<img width="1918" height="906" alt="image" src="https://github.com/user-attachments/assets/11f15e86-4388-4875-beeb-143f95e29ba7" />

- "Show me all students in my scope"<img width="1917" height="912" alt="image" src="https://github.com/user-attachments/assets/b1ef1ef1-c126-43c2-ab00-ecddf054d69f" />


### Admin Roles

The system includes sample admin roles with different access scopes:

- **John Admin**: Access to Grade 8 only
- **Sarah Manager**: Access to Classes 8A and 8B
- **Mike Regional**: Access to North region
- **Lisa South Admin**: Access to South region
- **Tom Multi-Grade**: Access to Grades 7, 8, and 9

Select an admin role from the sidebar to see how access control works.

## Project Structure

```
DumrooAI/
├── data/                          # Data files
│   ├── school_data.json          # Student, homework, quiz, and performance data
│   └── admin_roles.json          # Admin role configurations
├── src/                          # Source code
│   ├── models/                   # Data models
│   │   ├── admin_role.py        # AdminRole data class
│   │   └── query_intent.py      # QueryIntent data class
│   ├── services/                 # Business logic
│   │   ├── data_repository.py   # Abstract data repository
│   │   ├── json_data_repository.py  # JSON implementation
│   │   ├── role_manager.py      # Admin role management
│   │   ├── scope_filter.py      # Access control filtering
│   │   ├── nl_query_parser.py   # Natural language parser
│   │   └── query_executor.py    # Query execution engine
│   ├── ui/                       # User interface
│   │   └── streamlit_app.py     # Streamlit web app
│   ├── config.py                 # Configuration settings
│   └── utils.py                  # Utility functions

├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
├── main.py                       # Main entry point
├── run.bat                       # Windows run script
└── README.md                     # This file
```

## Architecture

The system follows a layered architecture:

### 1. Data Access Layer
- **DataRepository**: Abstract interface for data access
- **JSONDataRepository**: Concrete implementation for JSON files
- Easily replaceable with database implementations

### 2. Access Control Layer
- **AdminRole**: Defines admin scope (grade, class, or region)
- **RoleManager**: Loads and manages admin roles
- **ScopeFilter**: Applies role-based filtering to data

### 3. Query Processing Layer
- **NLQueryParser**: Uses LangChain + OpenAI to parse natural language
- **QueryIntent**: Structured representation of parsed queries
- **QueryExecutor**: Executes queries and returns filtered results

### 4. UI Layer
- **Streamlit App**: Interactive web interface
- Admin role selector
- Query input and results display

## Testing

The system includes comprehensive sample data:
- 26 students across grades 6-10
- Multiple classes (A, B, C) and regions (North, South)
- Homework submissions with various statuses
- Quiz schedules (past and upcoming)
- Performance records with scores

## Security & Access Control

- Admins can only access data within their assigned scope
- No access to platform-wide user or admin data
- Scope filtering applied at the data layer
- All queries automatically filtered by admin role

## Future Enhancements

- **Database Integration**: Replace JSON with PostgreSQL/MySQL
- **Multi-turn Conversations**: Context-aware follow-up questions
- **Data Visualization**: Charts and graphs for performance data
- **Export Functionality**: Download results as CSV/Excel
- **Audit Logging**: Track all queries for compliance
- **Advanced Analytics**: Trend analysis and predictions

## Technical Stack

- **Python 3.9+**: Core language
- **LangChain**: LLM orchestration framework
- **OpenAI API**: Natural language understanding
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web UI framework
- **JSON**: Data storage (easily replaceable)

## About

Built as part of the Dumroo AI Developer Assignment to demonstrate AI integration, natural language processing, and role-based access control in educational technology.

---

**Note**: Make sure to keep your `.env` file secure and never commit it to version control. The `.gitignore` file is configured to exclude it automatically.
