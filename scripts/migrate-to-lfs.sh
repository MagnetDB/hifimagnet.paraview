#!/bin/bash
# Git LFS Migration Script for hifimagnet.paraview
#
# This script helps migrate the test data archive to Git LFS.
# Run this script from the repository root.

set -e

echo "================================================"
echo "Git LFS Migration for hifimagnet.paraview"
echo "================================================"
echo ""

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS is not installed."
    echo ""
    echo "Please install Git LFS first:"
    echo "  Ubuntu/Debian: sudo apt-get install git-lfs"
    echo "  macOS:         brew install git-lfs"
    echo "  Windows:       Download from https://git-lfs.github.com/"
    echo ""
    exit 1
fi

echo "✓ Git LFS is installed: $(git lfs version)"
echo ""

# Check if Git LFS is initialized
if ! git lfs env &> /dev/null; then
    echo "→ Initializing Git LFS for your user..."
    git lfs install
    echo "✓ Git LFS initialized"
else
    echo "✓ Git LFS is already initialized"
fi
echo ""

# Verify .gitattributes is set up
if ! grep -q "test/data.tar.gz.*filter=lfs" .gitattributes; then
    echo "❌ .gitattributes does not have the LFS configuration for test/data.tar.gz"
    echo "   Please run: git lfs track 'test/data.tar.gz'"
    exit 1
fi

echo "✓ .gitattributes is configured for Git LFS"
echo ""

# Check current status of test data file
if [ ! -f "test/data.tar.gz" ]; then
    echo "⚠️  test/data.tar.gz not found"
    echo "   This might be expected if it hasn't been created yet."
    exit 0
fi

FILE_SIZE=$(du -h test/data.tar.gz | cut -f1)
echo "→ Found test/data.tar.gz (${FILE_SIZE})"
echo ""

# Check if file is already in Git
if git ls-files --error-unmatch test/data.tar.gz &> /dev/null; then
    echo "⚠️  test/data.tar.gz is already tracked by Git"
    echo ""
    echo "To migrate to LFS, you need to:"
    echo "  1. git rm --cached test/data.tar.gz"
    echo "  2. git add test/data.tar.gz"
    echo "  3. git commit -m 'Migrate test data to Git LFS'"
    echo ""
    read -p "Do you want to proceed with migration? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git rm --cached test/data.tar.gz
        git add test/data.tar.gz
        echo "✓ File staged for LFS commit"
        echo ""
        echo "Next steps:"
        echo "  git commit -m 'Migrate test data to Git LFS'"
        echo "  git push"
    fi
else
    # File is untracked, just add it
    echo "→ Adding test/data.tar.gz to Git LFS..."
    git add test/data.tar.gz
    echo "✓ File staged for LFS commit"
    echo ""
    echo "Next steps:"
    echo "  git commit -m 'Add test data with Git LFS'"
    echo "  git push"
fi

echo ""
echo "================================================"
echo "Migration Complete!"
echo "================================================"
echo ""
echo "Verify with: git lfs ls-files"
