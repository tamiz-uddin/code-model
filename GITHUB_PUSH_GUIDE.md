# GitHub Push Guide

## Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `code-model` (or your preferred name)
3. Description: `Universal AI Coding Model - Multi-Language Training`
4. Choose: **Public** (for sharing) or **Private** (for personal use)
5. Click **Create repository**

---

## Step 2: Initialize Git (First Time Only)

```bash
cd c:\Users\tamiz\Desktop\AI_Model_Plans\code-model

# Initialize git
git init

# Add .gitignore (already created)
git add .gitignore

# Configure git (first time)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Or globally:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 3: Add Files to Git

```bash
# Add all files (respects .gitignore)
git add .

# Or add specific files
git add notebooks/
git add config-phase3*.yaml
git add PHASE3_*.md
git add .gitignore
git add README.md
```

---

## Step 4: Create First Commit

```bash
git commit -m "Initial commit: Phase 3 multi-language training setup

- Add Phase 3A-3D Colab notebooks
- Add configuration files for each phase
- Add comprehensive documentation
- Add .gitignore for large files
- Support for 10+ programming languages"
```

---

## Step 5: Add Remote Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/code-model.git

# Or if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/code-model.git
```

---

## Step 6: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main

# Or if main already exists:
git push origin main
```

---

## Step 7: Verify on GitHub

1. Go to **https://github.com/YOUR_USERNAME/code-model**
2. Verify all files are there
3. Check that large files are NOT included (models, data)

---

## What Gets Pushed

### ✅ Included (Code & Documentation)
```
notebooks/
├── phase3a_foundation.ipynb
├── phase3b_frontend.ipynb
├── phase3c_fullstack.ipynb
└── phase3d_extended_languages.ipynb

config-phase3a.yaml
config-phase3b.yaml
config-phase3c.yaml
config-phase3d.yaml

PHASE3_MULTILANG.md
PHASE3_QUICK_START.md
PHASE3_COMPLETE.md

scripts/
└── phase3d_colab.py

.gitignore
README.md
```

### ❌ Excluded (Large Files)
```
outputs/models/*.pt (445 MB each)
data/phase3a/ (500 MB)
data/phase3b/ (200 MB)
data/phase3c/ (200 MB)
data/phase3d/ (1 GB)
```

---

## After Training: Push Models

After each phase, you can optionally push models using Git LFS (Large File Storage):

```bash
# Install Git LFS
# Windows: https://git-lfs.github.com/
# Mac: brew install git-lfs
# Linux: apt-get install git-lfs

# Track model files
git lfs install
git lfs track "*.pt"
git add .gitattributes

# Add model
git add outputs/models/foundation-model-v1.pt
git commit -m "Add Phase 3A model checkpoint"
git push origin main
```

---

## Updating Repository

After each phase, push updates:

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Phase 3B: Frontend stack training complete

- Add frontend-model-v1.pt checkpoint
- Update documentation with Phase 3B results
- Add training metrics and benchmarks"

# Push
git push origin main
```

---

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# View changes
git diff

# Undo changes
git checkout -- filename

# Remove file from git (but keep locally)
git rm --cached filename

# View remote
git remote -v

# Pull latest changes
git pull origin main
```

---

## GitHub README Template

Create `README.md`:

```markdown
# AI Code Model - Universal Coding Support

A multi-language AI model trained on 200K+ code samples supporting 10+ programming languages and frameworks.

## Features

- **Multi-Language Support:** JavaScript, Python, TypeScript, Java, Go, Rust, C#, HTML, CSS, SQL
- **Framework Knowledge:** React, Vue, Angular, Express, Django, Flask
- **Database Support:** SQL, MongoDB
- **API Patterns:** REST, GraphQL, JWT
- **Model Size:** 111.2M parameters, 445 MB

## Training Phases

- **Phase 3A:** Foundation (JavaScript + Python)
- **Phase 3B:** Frontend (HTML + CSS)
- **Phase 3C:** Full-Stack (Frameworks + Databases)
- **Phase 3D:** Extended Languages (TypeScript, Java, Go, Rust, C#, SQL)

## Quick Start

1. Open Google Colab: https://colab.research.google.com
2. Change runtime to GPU (T4)
3. Run Phase 3A notebook: `notebooks/phase3a_foundation.ipynb`
4. Download model: `foundation-model-v1.pt`

## Documentation

- [Phase 3 Guide](PHASE3_MULTILANG.md)
- [Quick Start](PHASE3_QUICK_START.md)
- [Complete Setup](PHASE3_COMPLETE.md)

## Training Timeline

- Week 1-2: Phase 3A (20-30 GPU hours)
- Week 3: Phase 3B (10-15 GPU hours)
- Week 4: Phase 3C (10-15 GPU hours)
- Week 5-6: Phase 3D (20-30 GPU hours)

## Model Architecture

- Parameters: 111.2M
- Layers: 12
- Attention Heads: 12
- Embedding Dimension: 768
- Vocabulary: 32,000 tokens
- Max Sequence Length: 2,048

## License

MIT License

## Status

Phase 3: Multi-Language Training ✅
```

---

## Troubleshooting

### "fatal: not a git repository"
```bash
cd c:\Users\tamiz\Desktop\AI_Model_Plans\code-model
git init
```

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/code-model.git
```

### "Permission denied (publickey)"
Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/code-model.git
```

### "Large files warning"
Files over 100 MB will trigger warnings. Use Git LFS for models.

---

## Summary

1. ✅ Create GitHub repository
2. ✅ Initialize git locally
3. ✅ Add files (respects .gitignore)
4. ✅ Create commit
5. ✅ Add remote
6. ✅ Push to GitHub
7. ✅ Verify on GitHub

---

**Your code is now backed up on GitHub! 🎉**
