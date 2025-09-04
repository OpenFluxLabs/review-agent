# Git setup commands for OpenFluxLabs organization

# 1. Initialize git repository
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: Review Agent MVP with LangChain and voice input"

# 4. Add GitHub remote for OpenFluxLabs organization
git remote add origin https://github.com/OpenFluxLabs/review-agent.git

# 5. Push to GitHub
git branch -M main
git push -u origin main