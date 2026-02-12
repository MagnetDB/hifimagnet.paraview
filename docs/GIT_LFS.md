# Git LFS Setup - Quick Reference

This document provides quick reference for Git LFS operations with this repository.

## What is tracked by Git LFS?

The following files are tracked with Git LFS (configured in `.gitattributes`):

- **Mesh files**: `*.msh`, `*.med`
- **Simulation outputs**: `*.sos`, `*.geo`, `*.vec`, `*.scl` (and variants)
- **Other large data**: `*.h5`
- **Test data**: `test/data.tar.gz` (20MB archive)

## Quick Commands

### Verify LFS is set up
```bash
git lfs version
git lfs env
```

### List LFS-tracked files
```bash
git lfs ls-files
```

### Check a specific file
```bash
git lfs ls-files | grep data.tar.gz
```

### Pull LFS files after clone
```bash
git lfs pull
```

### Get LFS object info
```bash
git lfs status
```

## For New Contributors

When cloning the repository:

```bash
# Install Git LFS first
sudo apt-get install git-lfs  # Ubuntu/Debian
brew install git-lfs          # macOS

# Initialize (one-time per user)
git lfs install

# Clone repository (LFS files download automatically)
git clone https://github.com/MagnetDB/hifimagnet.paraview.git
```

## Working with Test Data

### Downloading test data
Test data is automatically downloaded when you clone the repository with Git LFS enabled.

### Updating test data
If you need to update `test/data.tar.gz`:

```bash
# Create new archive
cd test
tar -czf data.tar.gz cases/ models/ Pictures/

# Add and commit (Git LFS handles it automatically)
git add data.tar.gz
git commit -m "Update test data"
git push
```

Git LFS will automatically handle the large file storage.

## Troubleshooting

### Files not downloading
```bash
# Force pull of all LFS files
git lfs pull

# Or for specific file
git lfs pull --include="test/data.tar.gz"
```

### Check if file is LFS pointer or actual file
```bash
# LFS pointer files are small text files (132 bytes)
ls -lh test/data.tar.gz

# If it shows ~132 bytes, it's a pointer. Download with:
git lfs pull
```

### Migrate existing file to LFS
```bash
# Use the migration script
./scripts/migrate-to-lfs.sh

# Or manually:
git rm --cached test/data.tar.gz
git add test/data.tar.gz
git commit -m "Migrate to Git LFS"
```

## CI/CD Integration

GitHub Actions automatically handles Git LFS when you use:

```yaml
- uses: actions/checkout@v4
  with:
    lfs: true
```

See `.github/workflows/tests.yml` for complete example.

## Storage Limits

GitHub provides 1GB of free LFS storage and 1GB/month of bandwidth. For larger needs:
- GitHub Pro: 2GB storage, 2GB bandwidth
- Additional packs available: 50GB for $5/month

Current LFS usage can be checked at:
https://github.com/MagnetDB/hifimagnet.paraview/settings

## References

- [Git LFS Documentation](https://git-lfs.github.com/)
- [GitHub LFS Guide](https://docs.github.com/en/repositories/working-with-files/managing-large-files)
- [Git LFS Tutorial](https://github.com/git-lfs/git-lfs/wiki/Tutorial)
