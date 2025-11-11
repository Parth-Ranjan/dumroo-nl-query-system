# Development Notes

## Implementation Approach

Started with the data layer to ensure clean separation of concerns. The abstract repository pattern makes it easy to swap JSON with a real database later.

## Challenges & Solutions

**Challenge**: LangChain version compatibility  
**Solution**: Updated to latest versions and adjusted imports from `langchain.prompts` to `langchain_core.prompts`

**Challenge**: Ensuring proper access control  
**Solution**: Implemented ScopeFilter that applies at the data layer, preventing any data leakage

## Design Decisions

- Used LangChain for query parsing instead of building custom NLP to leverage existing AI capabilities
- Chose Streamlit over Gradio for faster prototyping and cleaner UI
- Kept data models simple with dataclasses for clarity
- Added confidence scoring to help debug query parsing issues

## Testing Notes

Tested with different admin roles to verify access control:
- John Admin (Grade 8) - correctly filters to only Grade 8 students
- Sarah Manager (Classes 8A, 8B) - shows only those classes
- Mike Regional (North) - regional filtering works as expected

## Future Improvements

- Add conversation history for multi-turn queries
- Implement caching for frequently asked questions
- Add data visualization for performance metrics
- Consider adding query suggestions based on admin role
