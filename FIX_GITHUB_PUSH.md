# Fix GitHub Push Error - Large Files

## Problem

GitHub has a 100 MB file size limit. Your model file is 424 MB.

```
File outputs/models/code-model-phase2/model.safetensors is 424.23 MB
GitHub limit: 100 MB
```

## Solution: Remove Large Files from Git

### Step 1: Remove the Large File from Git History

```bash
cd c:\Users\tamiz\Desktop\AI_Model_Plans\code-model

# Remove the large file from git tracking
git rm --cached outputs/models/code-model-phase2/model.safetensors

# Or remove entire outputs directory
git rm --cached -r outputs/

# Verify it's removed
git status
```

### Step 2: Update .gitignore

The .gitignore already excludes model files, but let's verify:

```bash
# Check .gitignore
cat .gitignore | grep -E "\.pt|\.safetensors|outputs/models"
```

Should show:
```
outputs/models/*.pt
outputs/models/*.pth
outputs/models/*.onnx
```

### Step 3: Commit the Changes

```bash
cd c:\Users\tamiz\Desktop\AI_Model_Plans\code-model

# Add the updated .gitignore
git add .gitignore

# Commit
git commit -m "Remove large model files from tracking

- Remove outputs/models/ from git
- Keep .gitignore to prevent future large files
- Models should be downloaded from training, not stored in repo"

# Verify status
git status
```

### Step 4: Force Push (Reset Remote)

Since the push was rejected, you need to reset:

```bash
# Option 1: Force push (if you're the only one)
git push -u origin main --force

# Option 2: Reset remote and push
git push -u origin main
```

---

## Complete Fix Commands

Run these in order:

```bash
cd c:\Users\tamiz\Desktop\AI_Model_Plans\code-model

# 1. Remove large files from git
git rm --cached -r outputs/

# 2. Verify .gitignore is correct
echo "outputs/models/*.pt" >> .gitignore
echo "outputs/models/*.safetensors" >> .gitignore

# 3. Add changes
git add .gitignore

# 4. Commit
git commit -m "Remove large model files from tracking"

# 5. Push
git push -u origin main --force
```

---

## Verify Success

After pushing:

```bash
# Check remote
git log --oneline

# Verify files on GitHub
# Go to: https://github.com/tamiz-uddin/code-model
# Should NOT see outputs/models/ directory
```

---

## For Future Phases

### Option 1: Use Git LFS (Recommended)

```bash
# Install Git LFS
# Windows: https://git-lfs.github.com/
# Mac: brew install git-lfs
# Linux: apt-get install git-lfs

# Initialize LFS
git lfs install

# Track model files
git lfs track "*.pt"
git lfs track "*.safetensors"
git lfs track "*.onnx"

# Add .gitattributes
git add .gitattributes

# Commit
git commit -m "Add Git LFS for large model files"

# Push
git push origin main
```

### Option 2: Use GitHub Releases

Upload models as release assets instead of storing in repo:

```bash
# Create a release tag
git tag -a v0.3.0 -m "Phase 3A: Foundation model"

# Push tag
git push origin v0.3.0

# Then upload model file to GitHub Releases manually
```

### Option 3: Use External Storage

- Google Drive
- AWS S3
- Hugging Face Model Hub
- Dropbox

---

## What to Do Now

### Quick Fix (Recommended)

```bash
cd c:\Users\tamiz\Desktop\AI_Model_Plans\code-model

# Remove large files
git rm --cached -r outputs/

# Commit
git add .gitignore
git commit -m "Remove large model files from tracking"

# Push
git push -u origin main --force
```

### Verify

```bash
# Check status
git status

# Should show: nothing to commit, working tree clean
```

---

## After Fix

Your GitHub repo will have:
- ✅ All code files
- ✅ All notebooks
- ✅ All documentation
- ✅ Configuration files
- ❌ NO large model files (424 MB)

Model files will be:
- Downloaded from training in Colab
- Stored locally on your computer
- NOT in GitHub

---

## Summary

| Step | Command |
|------|---------|
| 1 | `git rm --cached -r outputs/` |
| 2 | `git add .gitignore` |
| 3 | `git commit -m "Remove large files"` |
| 4 | `git push -u origin main --force` |

---

**Run the commands above to fix the push error! 🚀**
