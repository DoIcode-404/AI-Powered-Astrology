"""
Fix all import paths in route files
Changes relative imports to absolute imports with server. prefix
"""

from pathlib import Path
import re

def fix_imports_in_file(filepath):
    """Fix imports in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # List of patterns to fix
    replacements = [
        # pydantic_schemas imports
        (r'from pydantic_schemas\.', 'from server.pydantic_schemas.'),
        (r'import pydantic_schemas', 'import server.pydantic_schemas'),

        # services imports
        (r'from services\.', 'from server.services.'),
        (r'import services', 'import server.services'),

        # utils imports
        (r'from utils\.', 'from server.utils.'),
        (r'import utils', 'import server.utils'),

        # middleware imports
        (r'from middleware\.', 'from server.middleware.'),
        (r'import middleware', 'import server.middleware'),

        # ml imports
        (r'from ml\.', 'from server.ml.'),
        (r'import ml', 'import server.ml'),

        # rule_engine imports
        (r'from rule_engine\.', 'from server.rule_engine.'),
        (r'import rule_engine', 'import server.rule_engine'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix all route files."""
    project_root = Path(__file__).parent
    server_dir = project_root / "server"

    # Files to fix
    files_to_fix = [
        server_dir / "routes" / "export.py",
        server_dir / "routes" / "kundali.py",
        server_dir / "routes" / "auth.py",
        server_dir / "routes" / "transits.py",
        server_dir / "routes" / "ml_predictions.py",
        server_dir / "main.py",
    ]

    print("Fixing imports in all files...\n")

    for filepath in files_to_fix:
        if filepath.exists():
            if fix_imports_in_file(filepath):
                print(f"✅ Fixed: {filepath.name}")
            else:
                print(f"⏭️  Skipped: {filepath.name} (no changes needed)")
        else:
            print(f"❌ Not found: {filepath.name}")

    print("\n✅ Import fixes complete!")

if __name__ == "__main__":
    main()