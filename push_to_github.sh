#!/bin/bash
# Push AI Code Model to GitHub

# Configuration
REPO_NAME="code-model"
GITHUB_USERNAME="YOUR_USERNAME"  # Replace with your GitHub username
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "=========================================="
echo "Pushing to GitHub"
echo "=========================================="

# Step 1: Initialize git (if not already done)
if [ ! -d ".git" ]; then
    echo "1. Initializing git repository..."
    git init
    echo "   ✓ Git initialized"
else
    echo "1. Git repository already initialized"
fi

# Step 2: Configure git (if not already done)
if [ -z "$(git config user.name)" ]; then
    echo "2. Configuring git..."
    read -p "   Enter your name: " GIT_NAME
    read -p "   Enter your email: " GIT_EMAIL
    git config user.name "$GIT_NAME"
    git config user.email "$GIT_EMAIL"
    echo "   ✓ Git configured"
else
    echo "2. Git already configured"
fi

# Step 3: Add .gitignore
echo "3. Adding .gitignore..."
git add .gitignore
echo "   ✓ .gitignore added"

# Step 4: Add all files
echo "4. Adding files..."
git add .
echo "   ✓ Files added"

# Step 5: Create commit
echo "5. Creating commit..."
git commit -m "Initial commit: Phase 3 multi-language training setup

- Add Phase 3A-3D Colab notebooks
- Add configuration files for each phase
- Add comprehensive documentation
- Add .gitignore for large files
- Support for 10+ programming languages"
echo "   ✓ Commit created"

# Step 6: Add remote
echo "6. Adding remote repository..."
if git remote | grep -q origin; then
    echo "   Remote already exists"
else
    git remote add origin "$REPO_URL"
    echo "   ✓ Remote added: $REPO_URL"
fi

# Step 7: Push to GitHub
echo "7. Pushing to GitHub..."
git branch -M main
git push -u origin main
echo "   ✓ Pushed to GitHub"

echo ""
echo "=========================================="
echo "✅ Successfully pushed to GitHub!"
echo "=========================================="
echo ""
echo "Repository: $REPO_URL"
echo ""
echo "Next steps:"
echo "1. Go to $REPO_URL"
echo "2. Verify all files are there"
echo "3. Start Phase 3A training"
echo ""
