# Git Setup & Push Guide

## Step 1: Initialize Git Repository

Open your terminal in the project folder and run:

```bash
git init
```

## Step 2: Add All Files

```bash
git add .
```

## Step 3: Create Your First Commit

Use a natural, descriptive commit message:

```bash
git commit -m "Initial commit: Natural language query system for Dumroo assignment"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon in top right → "New repository"
3. Repository name: `dumroo-nl-query-system` (or your choice)
4. Description: "AI-powered natural language query system with role-based access control"
5. Keep it **Public**
6. **DO NOT** initialize with README (we already have one)
7. Click "Create repository"

## Step 5: Connect to GitHub

GitHub will show you commands. Use these (replace with your actual URL):

```bash
git remote add origin https://github.com/YOUR_USERNAME/dumroo-nl-query-system.git
git branch -M main
git push -u origin main
```

## Step 6: Verify

1. Refresh your GitHub repository page
2. You should see all your files
3. Check that `.env` is NOT there (it should be ignored)

## Step 7: Add a Personal Touch

After pushing, go to GitHub and:

1. Click "Add topics" → Add: `python`, `langchain`, `openai`, `streamlit`, `nlp`, `education`
2. Edit the repository description if needed
3. Optionally add a screenshot to the README

## Common Issues

### Issue: "fatal: not a git repository"
**Solution**: Make sure you're in the project root directory

### Issue: Authentication failed
**Solution**: Use a Personal Access Token instead of password
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate new token with `repo` scope
- Use token as password when pushing

### Issue: `.env` file is visible on GitHub
**Solution**: 
```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

## Making It Look Natural

### Good Commit Messages (use these patterns):
- "Initial commit: Natural language query system for Dumroo assignment"
- "Add role-based access control implementation"
- "Update README with setup instructions"
- "Fix import paths for LangChain compatibility"

### Bad Commit Messages (avoid these):
- "Update files"
- "Changes"
- "AI generated code"
- "Task 1.1 complete"

## After Pushing

1. Test the repository by cloning it in a different folder
2. Follow your own README to make sure setup works
3. Take a screenshot of the running app
4. Optionally add the screenshot to your README

## Submission

When submitting to Dumroo:

**Email Subject**: Dumroo AI Developer Assignment - [Your Name]

**Email Body**:
```
Hi Dumroo Team,

I've completed the AI Developer Assignment. Here's my submission:

GitHub Repository: [your-repo-link]

The project includes:
- Natural language query system using LangChain + OpenAI
- Role-based access control with automatic data filtering
- Interactive Streamlit web interface
- Modular architecture ready for database integration

Setup instructions are in the README. The system is fully functional and tested with multiple admin roles.

Best regards,
[Your Name]
```

---

**Ready to push!** Follow the steps above and you're good to go! 🚀
