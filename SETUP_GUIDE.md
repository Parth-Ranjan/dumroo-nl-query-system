# Setup Guide - Dumroo AI NL Query System

## Step-by-Step Installation

### 1. Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9 or higher installed
- ✅ pip (Python package manager)
- ✅ OpenAI API key (get one at https://platform.openai.com/api-keys)

Check your Python version:
```bash
python --version
```

### 2. Project Setup

#### Download/Clone the Project
```bash
# If using git
git clone <repository-url>
cd DumrooAI

# Or extract the ZIP file and navigate to the folder
cd DumrooAI
```

#### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- langchain (AI framework)
- langchain-openai (OpenAI integration)
- openai (OpenAI API client)
- pandas (data manipulation)
- streamlit (web UI)
- python-dotenv (environment variables)

### 3. Configure OpenAI API Key

#### Create .env file
```bash
# Copy the example file
copy .env.example .env
```

#### Edit .env file
Open `.env` in any text editor and add your API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

**Important**: Never share or commit your `.env` file!

### 4. Run the Application

#### Option 1: Quick Start (Windows)
```bash
run.bat
```

#### Option 2: Using Streamlit
```bash
streamlit run src\ui\streamlit_app.py
```

#### Option 3: Using Python
```bash
python main.py
```

The app will automatically open in your browser at `http://localhost:8501`

### 5. First Time Usage

1. **Select an Admin Role** from the sidebar
   - Try "John Admin" (Grade 8 access only)
   
2. **Ask a Question** in the text box
   - Example: "Which students haven't submitted their homework yet?"
   
3. **View Results** displayed in a table below

4. **Try Different Roles** to see access control in action
   - Switch to "Mike Regional" (North region access)
   - Ask the same question and see different results

## Troubleshooting

### Issue: "OpenAI API key not found"
**Solution**: Make sure your `.env` file exists and contains a valid API key

### Issue: "Module not found" errors
**Solution**: 
1. Ensure virtual environment is activated (you should see `(venv)` in terminal)
2. Run `pip install -r requirements.txt` again

### Issue: Port 8501 already in use
**Solution**: 
1. Close any other Streamlit apps
2. Or specify a different port: `streamlit run src\ui\streamlit_app.py --server.port 8502`

### Issue: Import errors
**Solution**: Make sure you're running from the project root directory (DumrooAI folder)

## Testing the System

### Test 1: Homework Queries
```
Admin: John Admin (Grade 8)
Query: "Which students haven't submitted their homework yet?"
Expected: Shows Grade 8 students with not_submitted status
```

### Test 2: Performance Queries
```
Admin: Sarah Manager (Classes 8A, 8B)
Query: "Show me performance data for Grade 8 from last week"
Expected: Shows quiz scores for students in 8A and 8B only
```

### Test 3: Quiz Queries
```
Admin: Mike Regional (North region)
Query: "List all upcoming quizzes scheduled for next week"
Expected: Shows upcoming quizzes for North region only
```

### Test 4: Access Control
```
Admin: John Admin (Grade 8 only)
Query: "Show me all students"
Expected: Shows only Grade 8 students, not Grade 7, 9, or 10
```

## Project Structure Overview

```
DumrooAI/
├── data/                    # Sample data (JSON files)
├── src/                     # Source code
│   ├── models/             # Data classes
│   ├── services/           # Business logic
│   ├── ui/                 # Streamlit app
│   ├── config.py           # Settings
│   └── utils.py            # Helper functions
├── .env                     # Your API key (create this)
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## Next Steps

1. ✅ Complete the setup above
2. ✅ Test with example queries
3. ✅ Try different admin roles
4. ✅ Explore the code structure
5. ✅ Read the full README.md for more details

## Getting Help

- Check the main README.md for detailed documentation
- Review the spec files in `.kiro/specs/nl-query-system/`
- Ensure all dependencies are installed correctly

## Development Notes

### To modify the data:
- Edit `data/school_data.json` for student/homework/quiz data
- Edit `data/admin_roles.json` for admin configurations

### To extend functionality:
- The code is modular and well-documented
- Each component has clear interfaces
- Easy to swap JSON with a real database

---

**Ready to start?** Run `run.bat` and start querying! 🚀
