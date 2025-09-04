#!/bin/bash

# OpenFluxLabs Review Agent - Quick Deploy Script
# This script sets up the repository for immediate GitHub deployment

echo "🚀 OpenFluxLabs Review Agent - Quick Deploy"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "review_agent/agent.py" ]; then
    echo "❌ Error: Please run this script from the review-agent project root directory"
    exit 1
fi

# Make sure git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git branch -M main
fi

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Adding GitHub remote for OpenFluxLabs..."
    git remote add origin https://github.com/OpenFluxLabs/review-agent.git
else
    echo "🔗 Updating GitHub remote for OpenFluxLabs..."
    git remote set-url origin https://github.com/OpenFluxLabs/review-agent.git
fi

# Stage all files
echo "📦 Staging all files..."
git add .

# Create commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Review Agent MVP by OpenFluxLabs

🎤 AI-powered review management system featuring:
- Voice input processing with LangChain integration
- Multi-platform review posting (Google, Yelp, TripAdvisor)
- AI-generated authentic reviews using OpenAI
- Modular architecture for easy platform integration
- Complete demo scripts and comprehensive documentation
- Professional GitHub setup with CI/CD

Built by OpenFluxLabs - The future of automated review management.
"

echo "✅ Repository ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Create repository at: https://github.com/organizations/OpenFluxLabs/repositories/new"
echo "2. Repository name: review-agent" 
echo "3. Then run: git push -u origin main"
echo ""
echo "🌟 Your AI review automation platform is ready to launch!"

# Quick status check
echo ""
echo "📊 Project Status:"
echo "   Files: $(find . -name '*.py' | wc -l) Python files"
echo "   Platforms: $(ls review_agent/platforms/*.py | wc -l) platform integrations"
echo "   Demos: $(ls *demo*.py | wc -l) working demo scripts"
echo "   Docs: Complete (README, CONTRIBUTING, LICENSE)"
echo ""
echo "Repository: https://github.com/OpenFluxLabs/review-agent"