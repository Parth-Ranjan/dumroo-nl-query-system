"""
Streamlit UI for the Natural Language Query System
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import (
    SCHOOL_DATA_PATH, 
    ADMIN_ROLES_PATH, 
    OPENAI_API_KEY,
    OPENAI_MODEL,
    EXAMPLE_QUERIES
)
from src.services.json_data_repository import JSONDataRepository
from src.services.role_manager import RoleManager
from src.services.nl_query_parser import NLQueryParser
from src.services.query_executor import QueryExecutor
from src.utils import format_dataframe_for_display


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'selected_admin' not in st.session_state:
        st.session_state.selected_admin = None
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []


def load_components():
    """Load and cache application components."""
    if 'data_repository' not in st.session_state:
        st.session_state.data_repository = JSONDataRepository(str(SCHOOL_DATA_PATH))
    
    if 'role_manager' not in st.session_state:
        st.session_state.role_manager = RoleManager(str(ADMIN_ROLES_PATH))
    
    if 'query_parser' not in st.session_state:
        if not OPENAI_API_KEY:
            st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
            st.stop()
        st.session_state.query_parser = NLQueryParser(OPENAI_API_KEY, OPENAI_MODEL)
    
    if 'query_executor' not in st.session_state:
        st.session_state.query_executor = QueryExecutor(st.session_state.data_repository)


def main():
    """Main Streamlit application."""
    # Page configuration
    st.set_page_config(
        page_title="Dumroo Admin Panel - NL Query System",
        page_icon="🎓",
        layout="wide"
    )
    
    # Initialize
    initialize_session_state()
    load_components()
    
    # Header
    st.title("🎓 Dumroo Admin Panel")
    st.subheader("Natural Language Query System")
    st.markdown("---")
    
    # Sidebar for admin selection and examples
    with st.sidebar:
        st.header("Admin Selection")
        
        # Get all admins
        admins = st.session_state.role_manager.get_all_admins()
        admin_options = {f"{admin.name} ({admin.admin_id})": admin for admin in admins}
        
        selected_admin_key = st.selectbox(
            "Select Admin Role",
            options=list(admin_options.keys()),
            index=0
        )
        
        st.session_state.selected_admin = admin_options[selected_admin_key]
        
        # Display admin scope
        st.info(f"""
        **Current Admin:** {st.session_state.selected_admin.name}  
        **Scope Type:** {st.session_state.selected_admin.scope_type.title()}  
        **Scope Values:** {', '.join(st.session_state.selected_admin.scope_values)}
        """)
        
        st.markdown("---")
        
        # Example queries
        st.header("Example Queries")
        st.markdown("Try asking questions like:")
        for example in EXAMPLE_QUERIES:
            st.markdown(f"• {example}")
    
    # Main content area
    if st.session_state.selected_admin:
        render_query_interface()
    else:
        st.warning("Please select an admin role from the sidebar.")


def render_query_interface():
    """Render the query input and results interface."""
    # Query input
    st.header("Ask a Question")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Enter your question:",
            placeholder="e.g., Which students haven't submitted their homework?",
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.button("Submit Query", type="primary", use_container_width=True)
    
    # Process query
    if submit_button and query:
        process_query(query)
    
    # Display results
    if st.session_state.query_history:
        st.markdown("---")
        display_latest_result()


def process_query(query: str):
    """
    Process a natural language query.
    
    Args:
        query: The natural language question
    """
    with st.spinner("Processing your query..."):
        try:
            # Parse the query
            intent = st.session_state.query_parser.parse_query(query)
            
            # Execute the query
            results = st.session_state.query_executor.execute(
                intent,
                st.session_state.selected_admin
            )
            
            # Store in history
            st.session_state.query_history.append({
                'query': query,
                'intent': intent,
                'results': results
            })
            
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")


def display_latest_result():
    """Display the most recent query result."""
    if not st.session_state.query_history:
        return
    
    latest = st.session_state.query_history[-1]
    
    st.header("Results")
    
    # Display query info
    with st.expander("Query Details", expanded=False):
        st.write(f"**Question:** {latest['query']}")
        st.write(f"**Intent Type:** {latest['intent'].intent_type}")
        st.write(f"**Filters:** {latest['intent'].filters}")
        st.write(f"**Confidence:** {latest['intent'].confidence:.2f}")
    
    # Display results
    results_df = latest['results']
    
    if results_df.empty:
        st.info("No results found for your query. Try adjusting your question or check your access scope.")
    else:
        # Format and display
        formatted_df = format_dataframe_for_display(results_df)
        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
        
        st.success(f"Found {len(results_df)} result(s)")


if __name__ == "__main__":
    main()
