"""
Release Builder for Chrome Extensions
======================================

This script automates the creation of release packages for distribution.

PURPOSE:
    Generate ZIP archives ready for upload to:
    1. Chrome Web Store (Developer Console)
    2. GitHub Releases

OUTPUTS:
    Creates two ZIP files in the 'releases' folder:
    
    - {name}-v{version}-store.zip
        Minimal package for Chrome Web Store submission.
        Contains only essential extension files.
        
    - {name}-v{version}.zip
        Full package for GitHub Release.
        Contains extension files plus documentation.

USAGE:
    python scripts/build_release.py              # Build current version
    python scripts/build_release.py --bump patch # Bump 1.2.1 -> 1.2.2
    python scripts/build_release.py --bump minor # Bump 1.2.1 -> 1.3.0
    python scripts/build_release.py --bump major # Bump 1.2.1 -> 2.0.0

NOTES:
    - All metadata is read from manifest.json
    - Extension name is converted to slug format (lowercase, hyphenated)
    - The 'releases' folder will be created if it doesn't exist
    - The folder will open automatically after build completes

WORKFLOW:
    1. Run with --bump to increment version
    2. Commit and push changes
    3. Upload -store.zip to Chrome Developer Console
    4. Upload .zip to GitHub Release
"""

import os
import json
import zipfile
import re
import argparse


class Manifest:
    """Represents the extension manifest.json file."""
    
    def __init__(self, path):
        """Load manifest from file."""
        self.path = path
        self._data = self._load()
    
    def _load(self):
        """Read and parse manifest.json."""
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save(self):
        """Write manifest.json back to disk."""
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=4)
    
    @property
    def name(self):
        """Extension name."""
        return self._data.get('name', 'extension')
    
    @property
    def slug(self):
        """URL-friendly name (lowercase, hyphenated)."""
        name = self.name.lower()
        name = re.sub(r'[^a-z0-9]+', '-', name)
        return name.strip('-')
    
    @property
    def version(self):
        """Extension version."""
        return self._data.get('version', '0.0.0')
    
    @version.setter
    def version(self, value):
        """Set extension version and save."""
        self._data['version'] = value
        self._save()
    
    @property
    def description(self):
        """Extension description."""
        return self._data.get('description', '')
    
    def get(self, key, default=None):
        """Get any manifest property."""
        return self._data.get(key, default)
    
    def bump_version(self, bump_type='patch'):
        """
        Increment version number.
        
        Args:
            bump_type: 'major', 'minor', or 'patch'
        
        Returns:
            Tuple of (old_version, new_version)
        """
        old_version = self.version
        parts = old_version.split('.')
        
        # Ensure we have 3 parts
        while len(parts) < 3:
            parts.append('0')
        
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        new_version = f'{major}.{minor}.{patch}'
        self.version = new_version
        
        return old_version, new_version


class ReleaseBuilder:
    """Handles the creation of release packages for Chrome extensions."""
    
    # Core extension files (required for Chrome Web Store)
    STORE_FILES = [
        'manifest.json',
        'icons',
        'src',
    ]
    
    # Documentation files (added for GitHub release)
    DOCS_FILES = [
        'README.md',
        'PRIVACY.md',
        'LICENSE',
        'CHANGELOG.md',
    ]
    
    # Patterns to exclude from all packages
    EXCLUDE_PATTERNS = [
        '__pycache__',
        '.git',
        '.gitignore',
        '.gitattributes',
        'node_modules',
        'releases',
        'docs',
        'scripts',
        '.vscode',
        '.idea',
        '*.zip',
        '*.pyc',
        '.DS_Store',
        'Thumbs.db',
    ]
    
    def __init__(self, project_root=None):
        """Initialize builder with project root directory."""
        # Script is in scripts/, so go up one level for project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = project_root or os.path.dirname(script_dir)
        self.output_dir = os.path.join(self.project_root, 'releases')
        
        # Load manifest
        manifest_path = os.path.join(self.project_root, 'manifest.json')
        self.manifest = Manifest(manifest_path)
    
    def _should_exclude(self, path):
        """Check if a path should be excluded from the package."""
        name = os.path.basename(path)
        for pattern in self.EXCLUDE_PATTERNS:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern == name or pattern in path.split(os.sep):
                return True
        return False
    
    def _add_to_zip(self, zipf, source, arcname=None):
        """Add a file or directory to the ZIP archive."""
        if arcname is None:
            arcname = os.path.basename(source)
        
        if os.path.isfile(source):
            if not self._should_exclude(source):
                zipf.write(source, arcname)
        elif os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                dirs[:] = [d for d in dirs if not self._should_exclude(d)]
                for file in files:
                    if self._should_exclude(file):
                        continue
                    file_path = os.path.join(root, file)
                    arc_path = os.path.join(arcname, os.path.relpath(file_path, source))
                    zipf.write(file_path, arc_path)
    
    def _create_package(self, files, suffix=''):
        """Create a ZIP package with the specified files."""
        filename = f'{self.manifest.slug}-v{self.manifest.version}{suffix}.zip'
        filepath = os.path.join(self.output_dir, filename)
        
        # Try to remove existing file if it exists
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except PermissionError:
                print(f"\n  Error: Cannot overwrite {filename}")
                print("  The file may be open in another program.")
                print("  Close the file and try again.\n")
                raise SystemExit(1)
        
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in files:
                source = os.path.join(self.project_root, item)
                if os.path.exists(source):
                    self._add_to_zip(zipf, source, item)
        
        return filepath
    
    def _get_existing_files(self, file_list):
        """Filter file list to only existing files."""
        existing = []
        for item in file_list:
            path = os.path.join(self.project_root, item)
            if os.path.exists(path):
                existing.append(item)
        return existing
    
    def build_store_package(self):
        """Create minimal package for Chrome Web Store."""
        files = self._get_existing_files(self.STORE_FILES)
        return self._create_package(files, '-store')
    
    def build_github_package(self):
        """Create full package for GitHub Release."""
        store_files = self._get_existing_files(self.STORE_FILES)
        docs_files = self._get_existing_files(self.DOCS_FILES)
        return self._create_package(store_files + docs_files)
    
    def build_all(self):
        """Build all release packages and return results."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        return {
            'name': self.manifest.name,
            'slug': self.manifest.slug,
            'version': self.manifest.version,
            'description': self.manifest.description,
            'store': self.build_store_package(),
            'github': self.build_github_package(),
            'output_dir': self.output_dir,
        }
    
    @staticmethod
    def format_size(bytes_size):
        """Format file size in human readable format."""
        if bytes_size < 1024:
            return f"{bytes_size} B"
        elif bytes_size < 1024 * 1024:
            return f"{bytes_size / 1024:.1f} KB"
        else:
            return f"{bytes_size / (1024 * 1024):.1f} MB"
    
    def print_summary(self, result):
        """Print build summary to console."""
        width = 55
        print("=" * width)
        print(f"  {result['name']} - Release Builder")
        print("=" * width)
        print(f"\n  Version:     {result['version']}")
        print(f"  Description: {result['description'][:40]}...")
        print("\n  Packages:")
        print(f"    Chrome Store: {os.path.basename(result['store'])}")
        print(f"                  {self.format_size(os.path.getsize(result['store']))}")
        print(f"    GitHub:       {os.path.basename(result['github'])}")
        print(f"                  {self.format_size(os.path.getsize(result['github']))}")
        print(f"\n  Output: {result['output_dir']}")
        print("=" * width)


def main():
    """Entry point for the release builder."""
    parser = argparse.ArgumentParser(
        description='Build release packages for Chrome extension'
    )
    parser.add_argument(
        '--bump',
        choices=['major', 'minor', 'patch'],
        help='Bump version before building (major, minor, or patch)'
    )
    parser.add_argument(
        '--no-open',
        action='store_true',
        help='Do not open output folder after build'
    )
    
    args = parser.parse_args()
    
    builder = ReleaseBuilder()
    
    # Bump version if requested
    if args.bump:
        old_ver, new_ver = builder.manifest.bump_version(args.bump)
        print(f"Version bumped: {old_ver} -> {new_ver}\n")
    
    # Build packages
    result = builder.build_all()
    builder.print_summary(result)
    
    # Open output folder (Windows)
    if not args.no_open and os.name == 'nt':
        os.startfile(result['output_dir'])


if __name__ == '__main__':
    main()
