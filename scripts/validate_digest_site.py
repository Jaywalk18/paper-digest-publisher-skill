from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("parse_paper_index", SCRIPT_DIR / "parse_paper_index.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load parse_paper_index.py")
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)


def count_images(root: Path) -> int:
    img_dir = root / "images"
    return len([p for p in img_dir.glob("*") if p.is_file()]) if img_dir.exists() else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a paper digest static site build.")
    parser.add_argument("--site-root", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--report", help="Optional Markdown report; enables per-paper asset checks.")
    parser.add_argument("--require-no-preview", action="store_true", help="Fail if page_preview.jpg is referenced.")
    args = parser.parse_args()

    site_root = Path(args.site_root)
    issue = site_root / "issues" / f"{args.date}.html"
    index = site_root / "index.html"
    catalog = site_root / "pages" / "catalog.html"
    problems: list[str] = []

    if not issue.exists():
        problems.append(f"Missing issue page: {issue}")
    if not index.exists():
        problems.append(f"Missing homepage: {index}")
    if not catalog.exists():
        problems.append(f"Missing catalog page: {catalog}")

    public_text = ""
    for path in [issue, index, catalog]:
        if path.exists():
            public_text += "\n" + path.read_text(encoding="utf-8", errors="ignore")
    if '<figure class="hero-figure"><img' not in public_text and index.exists():
        problems.append("Homepage/issue output does not include a hero figure marker.")
    if args.require_no_preview and "page_preview.jpg" in public_text:
        problems.append("Public HTML still references page_preview.jpg fallback images.")

    checked = []
    if args.report:
        papers = parser_module.parse_paper_index(Path(args.report).read_text(encoding="utf-8"))
        for paper in papers:
            root = site_root / "assets" / "mineru" / paper["arxiv_id"]
            image_count = count_images(root)
            content_count = len(list(root.glob("*content_list.json"))) if root.exists() else 0
            preview = (root / "images" / "page_preview.jpg").exists()
            checked.append(
                {
                    "arxiv_id": paper["arxiv_id"],
                    "priority": paper["priority"],
                    "images": image_count,
                    "content_json": content_count,
                    "preview": preview,
                }
            )
            if image_count == 0:
                problems.append(f"No images for {paper['arxiv_id']}")
            if content_count == 0:
                problems.append(f"No content_list JSON for {paper['arxiv_id']}")
            if args.require_no_preview and preview:
                problems.append(f"Preview fallback remains for {paper['arxiv_id']}")

    result = {"ok": not problems, "problems": problems, "checked": checked}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
