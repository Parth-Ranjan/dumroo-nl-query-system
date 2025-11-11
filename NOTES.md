# Development Notes

## Implementation Approach

Built this system with a focus on modularity and clean architecture. Started with the data layer using an abstract repository pattern, which makes it straightforward to swap JSON with a real database later.

## Key Design Decisions

- **LangChain Integration**: Used LangChain for query parsing instead of building custom NLP. This leverages existing AI capabilities and makes the system more maintainable.

- **Role-Based Access Control**: Implemented filtering at the data layer to ensure no data leakage. The ScopeFilter applies restrictions before data reaches the query executor.

- **Streamlit for UI**: Chose Streamlit over Gradio for faster prototyping and a cleaner interface. The component-based approach made it easy to iterate.

## Challenges Faced

**Challenge**: LangChain version compatibility issues  
**Solution**: Updated to latest versions and adjusted imports from `langchain.prompts` to `langchain_core.prompts`

**Challenge**: Ensuring proper access control across different admin scopes  
**Solution**: Created comprehensive test scenarios with different admin roles to verify filtering works correctly

## Testing

Tested with multiple admin roles to verify access control:
- John Admin (Grade 8 only) - correctly shows only Grade 8 students
- Sarah Manager (Classes 8A, 8B) - filters to specific classes
- Mike Regional (North region) - regional filtering works as expected

## Future Improvements

- Add conversation history for multi-turn queries
- Implement caching for frequently asked questions
- Add data visualization for performance metrics
- Consider query suggestions based on admin role and common patterns
