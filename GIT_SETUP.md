# 🐙 GIT WORKFLOW GUIDE - SIDDHI CONSTRUCTION WEBSITE

This guide explains how to use Git to manage your website code with push/pull functionality.

---

## 📋 Prerequisites

1. **Git installed** - Download from https://git-scm.com/
2. **GitHub account** - Create at https://github.com/
3. **SSH key configured** (optional but recommended)

---

## 🚀 First Time Setup (One Time Only)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `siddhi-construction-website`
3. Description: `Professional 3D construction company website`
4. Choose **Public** (so you can share the link)
5. Click "Create repository"

### Step 2: Initialize Local Git Repository

```bash
# Navigate to your project folder
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website

# Initialize Git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial SIDDHI website commit"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/siddhi-construction-website.git

# Push to GitHub (main branch)
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 📝 Regular Workflow (Day-to-Day)

### Making Changes

1. **Edit files** in your project
2. **Check status:**
   ```bash
   git status
   ```

3. **Add changes:**
   ```bash
   git add .
   ```

4. **Commit changes:**
   ```bash
   git commit -m "feat: Description of changes"
   ```

5. **Push to GitHub:**
   ```bash
   git push origin main
   ```

### Example Workflow

```bash
# Update projects in code
# Edit siddhi-construction-website.jsx

# Check what changed
git status

# Stage changes
git add siddhi-construction-website.jsx

# Commit with message
git commit -m "feat: Add new luxury residential complex project"

# Push to GitHub
git push origin main
```

---

## 🔄 Pulling Latest Changes

If you work on multiple devices or collaborate with others:

```bash
# Navigate to your project
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website

# Pull latest changes
git pull origin main
```

---

## 📊 Useful Git Commands

### View History
```bash
# See all commits
git log --oneline

# See commits from last 5 days
git log --since="5 days ago"

# See who changed what
git log -p
```

### Undo Changes
```bash
# Undo uncommitted changes
git checkout -- filename.txt

# Undo last commit (keep changes)
git reset HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Branching (Optional)
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branch
git checkout main

# Merge branch
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
```

---

## ⚙️ Configuration

### Set Your Git Name & Email
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Verify Configuration
```bash
git config --list
```

---

## 🔐 SSH Setup (Optional but Recommended)

SSH allows you to push/pull without entering your password every time.

### Generate SSH Key
```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

### Add to GitHub

1. Copy the public key: `cat ~/.ssh/id_ed25519.pub`
2. Go to GitHub → Settings → SSH and GPG keys
3. Click "New SSH key"
4. Paste the key

### Update Remote URL
```bash
# Change from HTTPS to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/siddhi-construction-website.git
```

---

## 🌲 .gitignore File

The `.gitignore` file is already configured to exclude:
- `node_modules/` (dependencies)
- `.DS_Store` (Mac files)
- `*.log` (log files)
- `dist/` (build output)

You don't need to commit these files.

---

## 📱 Commit Message Guidelines

Use clear, descriptive commit messages:

### Good Examples
```
feat: Add new commercial project to portfolio
fix: Fix 3D animation performance issue
docs: Update README with deployment instructions
style: Update orange color to brighter shade
refactor: Simplify contact form validation
test: Add unit tests for form submission
```

### Format
```
type: short description (50 chars max)

Longer explanation if needed.
Explain WHY the change was made, not just WHAT.
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (no logic change)
- `refactor:` Code refactoring
- `test:` Adding/updating tests
- `chore:` Maintenance tasks

---

## 🚨 Common Issues & Solutions

### Issue: Permission denied when pushing
```bash
# Solution: Verify SSH key is added to GitHub
ssh -T git@github.com
# Should show: "Hi username! You've successfully authenticated"
```

### Issue: "fatal: not a git repository"
```bash
# Solution: Make sure you're in the right directory
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website
git status
```

### Issue: Accidentally committed large file
```bash
# Solution: Remove from history
git rm --cached filename.txt
git commit --amend
git push origin main --force
```

### Issue: Merge conflicts
```bash
# When pulling, if there are conflicts:
# 1. Edit the conflicted file (look for <<<< and >>>>)
# 2. Keep the changes you want
# 3. Remove conflict markers
# 4. Stage and commit
git add .
git commit -m "fix: resolve merge conflict"
git push origin main
```

---

## 📚 Resources

- **GitHub Docs:** https://docs.github.com/
- **Git Documentation:** https://git-scm.com/doc
- **Interactive Git Learning:** https://learngitbranching.js.org/

---

## ✅ Quick Reference

### First Time
```bash
cd C:\Users\Admin\Desktop\PROJECTS\active\Construction_Website
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/siddhi-construction-website.git
git branch -M main
git push -u origin main
```

### Regular Workflow
```bash
# Make changes...
git status              # Check what changed
git add .               # Stage changes
git commit -m "message" # Commit
git push origin main    # Push to GitHub
```

### Get Latest
```bash
git pull origin main
```

---

## 🎯 Next Steps

1. Create GitHub account (if not already done)
2. Create repository on GitHub
3. Initialize local Git (see "First Time Setup")
4. Make first commit and push
5. Continue with regular workflow for future changes

---

**Good luck with your SIDDHI Construction website!** 🚀

For any Git issues, visit: https://github.com/git-tips/tips
