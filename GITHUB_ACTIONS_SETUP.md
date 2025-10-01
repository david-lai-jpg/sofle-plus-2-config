# 🚀 GitHub Actions Auto-Build Setup

This guide explains how to set up automatic firmware compilation using GitHub Actions.

## 🎯 What You Get

- ✅ **Automatic builds** on every code change
- ✅ **Downloadable UF2 files** from GitHub
- ✅ **No local toolchain required** for simple changes
- ✅ **Build history** and artifact management
- ✅ **Pull request builds** for testing changes

## 📋 Prerequisites

1. **GitHub account** (free tier works fine)
2. **Fork or create** a repository with your firmware source
3. **Push your code** to the main/master branch

## ⚙️ Setup Instructions

### 1. Repository Setup

```bash
# Clone your firmware repo
git clone https://github.com/YOUR_USERNAME/your-firmware-repo.git
cd your-firmware-repo

# Ensure you have the workflow file
ls -la .github/workflows/build-firmware.yml
```

### 2. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. GitHub will automatically detect the workflow
4. Click **"I understand my workflows, go ahead and enable them"**

### 3. Make Your First Build

```bash
# Make any small change (or just commit an empty change)
git commit --allow-empty -m "Trigger first build"
git push origin main
```

### 4. Monitor the Build

1. Go to **Actions** tab in your GitHub repo
2. Click on the running workflow
3. Watch the build progress in real-time
4. Build takes ~5-10 minutes on first run

### 5. Download Your Firmware

1. After build completes, scroll down to **Artifacts**
2. Download `sofleplus2-tps65-yaxis-fix-firmware`
3. Extract the UF2 file
4. Flash to your keyboard!

## 🔧 Customizing the Workflow

### Build on Different Branches

Edit `.github/workflows/build-firmware.yml`:

```yaml
on:
  push:
    branches: [main, master, develop] # Add your branch here
```

### Build Only Specific Files

```yaml
on:
  push:
    paths:
      - 'keymaps/tps65-403d/**' # Only TPS65 changes
      - '*.c'
      - '*.h'
```

### Matrix Builds (Multiple Keymaps)

```yaml
strategy:
  matrix:
    keymap: [tps65-403d, tps43-403d, custom-keymap]
```

## 📊 Understanding Build Results

### ✅ Successful Build

- **Green checkmark** in Actions tab
- **Artifacts available** for download
- **Build summary** shows firmware size and instructions

### ❌ Failed Build

- **Red X** in Actions tab
- **Click on the build** to see error logs
- Common issues:
  - Syntax errors in keymap.c
  - Missing dependencies
  - Invalid configuration

### ⚠️ Build Warnings

- **Yellow triangle** - build succeeded with warnings
- Usually safe to ignore PRODUCT redefinition warnings
- Check logs for any real issues

## 🛠️ Troubleshooting

### Build Fails with "arm-none-eabi-gcc not found"

The workflow should install this automatically. If it fails:

1. Check if the Ubuntu package names changed
2. Update the workflow dependencies section

### Workflow Doesn't Trigger

1. Check you're pushing to the correct branch
2. Verify the workflow file is in `.github/workflows/`
3. Check GitHub Actions are enabled for your repo

### Artifacts Don't Appear

1. Build must complete successfully first
2. Artifacts expire after 30 days by default
3. Check you have the upload-artifact step in your workflow

### Out of GitHub Actions Minutes

- **Free tier**: 2000 minutes/month
- **Each build**: ~10 minutes
- **Solution**: Use local builds or upgrade to Pro

## 🚀 Advanced Features

### Conditional Builds

```yaml
# Only build TPS43 if files changed
if: contains(github.event.head_commit.modified, 'tps43')
```

### Release Automation

```yaml
# Auto-create releases on version tags
if: startsWith(github.ref, 'refs/tags/v')
```

### Slack/Discord Notifications

```yaml
- name: Notify Discord
  if: always() # Run even if build fails
  uses: sarisia/actions-status-discord@v1
```

### Multiple Keyboard Support

```yaml
strategy:
  matrix:
    keyboard: [sofleplus2, crkbd, lily58]
    keymap: [default, via]
```

## 📈 Monitoring and Maintenance

### Build History

- **Actions tab** shows all builds
- **Click any build** to see detailed logs
- **Filter by branch, status, or date**

### Artifact Management

- **Artifacts auto-expire** after retention period
- **Download before expiration** if you need them
- **Adjust retention** in workflow file:

```yaml
retention-days: 90 # Keep for 3 months
```

### Workflow Updates

- **Watch QMK/Vial repos** for dependency changes
- **Update Ubuntu packages** if build tools change
- **Test workflow changes** in feature branches first

## 💡 Tips and Best Practices

### 1. Use Draft Pull Requests

```yaml
# Test changes without affecting main branch
if: github.event.pull_request.draft == false
```

### 2. Cache Dependencies

```yaml
# Speeds up builds significantly
uses: actions/cache@v4
with:
  path: vial-qmk
  key: vial-qmk-${{ hashFiles('**/workflow.yml') }}
```

### 3. Parallel Builds

```yaml
# Build multiple keymaps simultaneously
strategy:
  matrix:
    keymap: [tps65-403d, tps43-403d]
  max-parallel: 2
```

### 4. Semantic Versioning

```bash
# Tag releases for easy tracking
git tag -a v1.0.0 -m "Y-axis fix release"
git push origin v1.0.0
```

### 5. Environment Secrets

```yaml
# Store sensitive data in GitHub Secrets
env:
  DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
```

## 📊 Build Status Badge

Add a build status badge to your README to show build status:

```markdown
[![Build Firmware](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/build-firmware.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/build-firmware.yml)
```

**Replace:**

- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO` with your repository name

The badge will show:

- ✅ **Green "passing"** - Build successful
- ❌ **Red "failing"** - Build failed
- 🟡 **Yellow "running"** - Build in progress

## 🎉 You're All Set!

Your firmware will now build automatically whenever you:

- 📝 Push code changes
- 🔀 Create pull requests
- 🚀 Manually trigger builds
- 🏷️ Create new releases

**Next Steps:**

1. Make a small change to test the build
2. Customize the workflow for your needs
3. Add the build status badge to your README
4. Set up notifications if desired
5. Share your automated setup with others!

Happy building, you magnificent automated bastard! 🤖✨
