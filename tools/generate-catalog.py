#!/usr/bin/env python3
"""
Generate catalog.json from all metadata.yaml files in content/.

Usage:
    python3 tools/generate-catalog.py

Output:
    site/src/site/resources/catalog.json

This script walks the content/ directory tree, finds all metadata.yaml files,
parses them, and writes a JSON catalog that the catalog.html page uses for
tag-based filtering.
"""

import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

# Paths relative to repository root
REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
OUTPUT_FILE = REPO_ROOT / "site" / "src" / "site" / "resources" / "catalog.json"


def find_metadata_files(content_dir):
    """Recursively find all metadata.yaml files."""
    return sorted(content_dir.rglob("metadata.yaml"))


def parse_metadata(filepath):
    """Parse a metadata.yaml file and add computed fields."""
    with open(filepath) as f:
        data = yaml.safe_load(f)

    if not data or not data.get("title"):
        return None

    # Skip the Template itself
    if data.get("project_id") == "template":
        return None

    # Compute the relative path to the presentation
    module_dir = filepath.parent
    rel_path = module_dir.relative_to(CONTENT_DIR)

    # Convention: presentation is at presentations/{rel_path}/index.html
    # (lowercase, as built by Maven)
    presentation_path = f"presentations/{str(rel_path).lower()}/index.html"

    data["path"] = presentation_path
    data["module_dir"] = str(rel_path)

    return data


def main():
    if not CONTENT_DIR.exists():
        print(f"ERROR: Content directory not found: {CONTENT_DIR}")
        sys.exit(1)

    metadata_files = find_metadata_files(CONTENT_DIR)
    print(f"Found {len(metadata_files)} metadata.yaml files")

    catalog = []
    all_tags = set()

    for filepath in metadata_files:
        entry = parse_metadata(filepath)
        if entry:
            catalog.append(entry)
            all_tags.update(entry.get("tags", []))
            print(f"  + {entry['title']}")

    # Sort catalog alphabetically by title
    catalog.sort(key=lambda x: x["title"].lower())

    output = {
        "generated": True,
        "count": len(catalog),
        "tags": sorted(all_tags),
        "modules": catalog,
    }

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nWrote {len(catalog)} modules to {OUTPUT_FILE}")
    print(f"Tags: {', '.join(sorted(all_tags))}")


if __name__ == "__main__":
    main()
