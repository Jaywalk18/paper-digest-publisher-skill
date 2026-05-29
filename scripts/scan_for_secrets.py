from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = {
    "github_token": re.compile(r"\b(?:gho|ghp|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"),
    "github_pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "bearer_token": re.compile(r"(?i)\bAuthorization\s*:\s*Bearer\s+[A-Za-z0-9._-]{20,}"),
    "mineru_token_assignment": re.compile(r"(?i)\bMINERU_TOKEN\s*=\s*['\"]?[A-Za-z0-9._-]{20,}"),
    "lark_secret": re.compile(r"(?i)\b(?:app_secret|tenant_access_token|user_access_token|refresh_token)\b\s*[:=]\s*['\"]?[A-Za-z0-9._-]{16,}"),
}

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".mypy_cache", ".pytest_cache"}
SKIP_FILES = {"scan_for_secrets.py"}
TEXT_EXTS = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".py", ".js", ".ts", ".tsx",
    ".css", ".html", ".toml", ".ini", ".cfg", ".gitignore", ""
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.name in SKIP_FILES:
            continue
        if path.suffix.lower() not in TEXT_EXTS and path.name != ".gitignore":
            continue
        yield path


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a repo for obvious token patterns before public release.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings: list[str] = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                rel = path.relative_to(root)
                findings.append(f"{rel}: {name} at character {match.start()}")

    if findings:
        print("Potential secrets found:")
        for item in findings:
            print(f"- {item}")
        raise SystemExit(1)
    print("No obvious secrets found.")


if __name__ == "__main__":
    main()
