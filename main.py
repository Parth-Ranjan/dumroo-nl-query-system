"""
Main entry point for the Dumroo NL Query System
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    
    # Path to the Streamlit app
    app_path = Path(__file__).parent / "src" / "ui" / "streamlit_app.py"
    
    # Run Streamlit
    sys.argv = ["streamlit", "run", str(app_path)]
    sys.exit(stcli.main())
