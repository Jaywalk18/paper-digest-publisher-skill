from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def strip_md(text: str) -> str:
    text = re.sub(r"!\[[^\]]*]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)]\(([^)]+)\)", r"\1", text)
    return text.replace("**", "").replace("`", "").strip()


def split_md_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_paper_index(markdown: str) -> list[dict[str, str]]:
    start = markdown.find("## 论文索引")
    if start < 0:
        start = markdown.lower().find("## paper index")
    if start < 0:
        return []

    rows: list[list[str]] = []
    in_table = False
    for line in markdown[start:].splitlines():
        if line.strip().startswith("|"):
            parts = split_md_row(line)
            if all(re.fullmatch(r":?-{3,}:?", p or "") for p in parts):
                in_table = True
                continue
            rows.append(parts)
            in_table = True
        elif in_table:
            break

    papers: list[dict[str, str]] = []
    for row in rows[1:]:
        if len(row) < 2:
            continue
        priority = strip_md(row[0])
        if "过滤" in priority.lower() or "filter" in priority.lower():
            continue
        match = re.search(
            r"\[([^\]]+)]\((https://arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?)\)",
            row[1],
        )
        if not match:
            continue
        title, url, arxiv_id = match.groups()
        papers.append(
            {
                "arxiv_id": arxiv_id,
                "title": strip_md(title),
                "url": url,
                "priority": priority,
                "type": strip_md(row[2]) if len(row) > 2 else "",
                "relevance": strip_md(row[3]) if len(row) > 3 else "",
                "reason": strip_md(row[4]) if len(row) > 4 else "",
            }
        )
    return papers


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse the paper index table from a digest Markdown file.")
    parser.add_argument("--report", required=True, help="Markdown digest path.")
    parser.add_argument("--format", choices=["json", "table"], default="json")
    args = parser.parse_args()

    papers = parse_paper_index(Path(args.report).read_text(encoding="utf-8"))
    if args.format == "json":
        print(json.dumps(papers, ensure_ascii=False, indent=2))
    else:
        for paper in papers:
            print("\t".join([paper["priority"], paper["arxiv_id"], paper["title"], paper["type"]]))


if __name__ == "__main__":
    main()
