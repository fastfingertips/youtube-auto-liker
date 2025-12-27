# Release Workflow

## Overview
Semantic versioning (MAJOR.MINOR.PATCH) with Keep a Changelog format.

## Steps

### 1. Update Changelog
Ask AI: "Releasing v{VERSION}, update changelog"

AI will:
1. Run `git log --oneline $(git describe --tags --abbrev=0)..HEAD`
2. Categorize commits (Added, Changed, Fixed, Removed)
3. Update CHANGELOG.md

### 2. Bump Version and Build
```bash
python scripts/build_release.py --bump patch
```
This updates manifest.json AND creates ZIP packages.

### 3. Commit and Tag
```bash
git add .
git commit -m "chore: release v{VERSION}"
git tag v{VERSION}
git push origin main --tags
```

### 4. Publish
- **GitHub**: Create release with tag, attach `.zip` file
- **Chrome Web Store**: Upload `-store.zip` to Developer Dashboard

## Changelog Format
```markdown
## [X.X.X] - YYYY-MM-DD

### Added
### Changed
### Fixed
### Removed
```

## Commit Convention
| Prefix | Category |
|--------|----------|
| `feat:` | Added |
| `fix:` | Fixed |
| `refactor:` | Changed |
| `docs:` | Changed |
| `chore:` | (skip) |
