from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import sys
import urllib.request
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("parse_paper_index", SCRIPT_DIR / "parse_paper_index.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load parse_paper_index.py")
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)


def safe_name(text: str, max_len: int = 72) -> str:
    clean = re.sub(r"[<>:\"/\\|?*\x00-\x1f]+", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip(" .")
    return (clean[:max_len].rstrip(" .") or "paper")


def is_pdf_preview_fallback(root: Path) -> bool:
    img_dir = root / "images"
    if not img_dir.exists():
        return False
    image_files = [p for p in img_dir.iterdir() if p.is_file()]
    if len(image_files) != 1 or image_files[0].name != "page_preview.jpg":
        return False
    content = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in root.glob("*content_list.json"))
    return "First-page visual preview" in content or "full figure extraction is pending" in content


def remove_preview_fallbacks(papers: list[dict[str, str]], mineru_root: Path) -> int:
    root_resolved = mineru_root.resolve()
    removed = 0
    for paper in papers:
        paper_root = mineru_root / paper["arxiv_id"]
        if not paper_root.exists() or not is_pdf_preview_fallback(paper_root):
            continue
        resolved = paper_root.resolve()
        if root_resolved not in resolved.parents:
            raise RuntimeError(f"Refusing to remove unexpected path: {resolved}")
        shutil.rmtree(resolved)
        removed += 1
    return removed


def clean_staging(papers: list[dict[str, str]], staging_dir: Path) -> list[Path]:
    staging_dir.mkdir(parents=True, exist_ok=True)
    expected = {
        staging_dir / f"{paper['arxiv_id']} - {safe_name(paper['title'])}.pdf"
        for paper in papers
    }
    for existing in staging_dir.glob("*.pdf"):
        if existing not in expected:
            existing.unlink(missing_ok=True)
    return sorted(expected)


def download_missing(papers: list[dict[str, str]], staging_dir: Path) -> int:
    downloaded = 0
    for paper in papers:
        path = staging_dir / f"{paper['arxiv_id']} - {safe_name(paper['title'])}.pdf"
        if path.exists() and path.stat().st_size > 100_000:
            continue
        url = f"https://arxiv.org/pdf/{paper['arxiv_id']}"
        request = urllib.request.Request(url, headers={"User-Agent": "visual-ssl-digest-skill/1.0"})
        with urllib.request.urlopen(request, timeout=90) as response:
            path.write_bytes(response.read())
        downloaded += 1
    return downloaded


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a clean PDF batch for MinerU extraction.")
    parser.add_argument("--report", required=True, help="Digest Markdown with a paper index table.")
    parser.add_argument("--staging-dir", required=True, help="Directory that should contain only indexed PDFs.")
    parser.add_argument("--mineru-root", required=True, help="MinerU output root containing per-arXiv-ID directories.")
    parser.add_argument("--download", action="store_true", help="Download missing PDFs from arXiv.")
    args = parser.parse_args()

    report = Path(args.report)
    staging_dir = Path(args.staging_dir)
    mineru_root = Path(args.mineru_root)

    papers = parser_module.parse_paper_index(report.read_text(encoding="utf-8"))
    if not papers:
        raise SystemExit("No arXiv papers found in the report index.")

    expected = clean_staging(papers, staging_dir)
    removed = remove_preview_fallbacks(papers, mineru_root)
    downloaded = download_missing(papers, staging_dir) if args.download else 0
    missing = [str(path) for path in expected if not path.exists()]

    print(f"indexed_papers={len(papers)}")
    print(f"removed_preview_fallbacks={removed}")
    print(f"downloaded_pdfs={downloaded}")
    print(f"missing_pdfs={len(missing)}")
    for path in missing:
        print(f"MISSING\t{path}")
    if missing:
        sys.exit(2)


if __name__ == "__main__":
    main()
