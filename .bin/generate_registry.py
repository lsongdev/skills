#!/usr/bin/env python3
"""Generate the registry.json skill index from SKILL.md files in this repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import yaml
except ImportError:
    yaml = None


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", REPO_ROOT, *args], capture_output=True, text=True
    )
    return result.stdout.strip()


def owner_repo() -> str:
    url = git("config", "--get", "remote.origin.url")
    url = url.replace("git@github.com:", "").replace("https://github.com/", "")
    return url.removesuffix(".git") or ""


def branch() -> str:
    return git("branch", "--show-current") or "master"


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    frontmatter = text.split("---", 2)[1]
    meta: dict = {}
    if yaml is not None:
        try:
            parsed = yaml.safe_load(frontmatter)
            if isinstance(parsed, dict):
                meta = parsed
        except yaml.YAMLError:
            meta = {}
    if not meta:
        for key in ("name", "description"):
            match = re.search(rf"^{key}:\s*(.+?)\s*$", frontmatter, re.M)
            if match:
                meta[key] = match.group(1)
    return meta


def read_skill(name: str, source: str, ref: str) -> dict:
    path = os.path.join(REPO_ROOT, name, "SKILL.md")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    meta = parse_frontmatter(text)

    title = name
    heading = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    if heading and heading.group(1).strip():
        title = heading.group(1).strip()
    if meta.get("name") and isinstance(meta["name"], str):
        title = title if meta["name"] == name else title

    description = meta.get("description", "")
    if isinstance(description, list):
        description = "\n".join(str(item) for item in description)
    description = str(description).strip()

    return {
        "id": name,
        "name": title,
        "description": description,
        "source": source,
        "files": [
            {
                "path": "SKILL.md",
                "url": (
                    f"https://raw.githubusercontent.com/{source}/{ref}/{name}/SKILL.md"
                ),
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o", "--output", default=os.path.join(REPO_ROOT, "registry.json")
    )
    parser.add_argument("-n", "--dry-run", action="store_true")
    parser.add_argument("--version", type=int, default=1)
    args = parser.parse_args()

    source = owner_repo()
    ref = branch()

    skills = []
    for entry in sorted(os.listdir(REPO_ROOT)):
        if entry.startswith("."):
            continue
        if not os.path.isfile(os.path.join(REPO_ROOT, entry, "SKILL.md")):
            continue
        skills.append(read_skill(entry, source, ref))

    data = {"version": args.version, "skills": skills}
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    if args.dry_run:
        print(text, end="")
    else:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(text)
        print(f"Wrote {len(skills)} skills to {args.output}")


if __name__ == "__main__":
    main()
