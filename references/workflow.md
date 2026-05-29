# Workflow Reference

## Topic Profile

Start by turning the user's request into a compact profile:

| Field | Purpose |
| --- | --- |
| Topic name | Human title for the digest and site. |
| Include | Core methods, venues, keywords, tasks, and adjacent areas. |
| Exclude | Vertical domains or weakly related areas to filter or downgrade. |
| Source tiers | Examples: conference pages, OpenReview, arXiv, project pages, code releases. |
| Priority rubric | Topic-specific meaning of P0/P1/P2/P3/scan-only. |
| Outputs | Markdown path, sync target, website path, public URL. |

Example: for a general visual self-supervised learning digest, include image/video pretraining, masked modeling, contrastive learning, distillation, VLM/VFM pretraining, and representation evaluation; downgrade medical, remote sensing, inspection, and other vertical applications unless the method transfers.

## Report Shape

Use this order:

1. Title with date.
2. Retrieval window and source list.
3. Quick summary table, 5-8 rows.
4. Reading route, 3-5 sentences.
5. Paper index table with priority, paper, type, relevance, one-line reason.
6. High-signal source dynamics, such as conference/OpenReview/official status changes.
7. Preprint new/update section, such as arXiv or other configured sources.
8. Detailed paper entries.
9. Trend observations.
10. Dedupe notes.

## Ranking

Adapt the priority labels to the topic. Keep the labels stable inside one digest so filtering and trend tracking remain usable.

Use P0 for papers that directly change the user's core topic, introduce a broadly reusable method, or deserve immediate deep reading.

Use P1 for strong adjacent work, high-value status changes, practical methods, benchmarks, or resources likely to influence the topic soon.

Use P2/P3 for diagnostics, downstream adaptation, specialized applications, incremental variants, or papers worth recording but not urgent.

Use scan-only for useful but narrow items.

## Dedupe

Prefer IDs in this order:

1. arXiv ID
2. OpenReview ID
3. DOI
4. normalized title

Normalize titles by lowercasing, removing punctuation, collapsing whitespace, and dropping version/status words. Merge arXiv and conference evidence into one item.

## MinerU Guardrails

Do not treat a directory with only `images/page_preview.jpg` as successful MinerU extraction. That is a PDF preview fallback.

Before a real MinerU run:

1. Remove stale PDFs from the staging directory.
2. Remove preview fallback directories for the indexed IDs.
3. Run MinerU.
4. Verify `*_content_list.json` and non-preview images exist for every indexed paper.

## Publishing Checks

Before pushing:

- local issue HTML exists
- homepage has a hero figure
- P0/P1 papers have extracted images
- no public HTML references `page_preview.jpg` after true MinerU extraction
- catalog priority and topic filters work
- git status is clean after commit/push
- online homepage, issue, and catalog return 200 with `?v=<commit>`

## Web Template

Use `assets/web-template/` when a project has no existing site:

1. Copy the directory to the target site workspace.
2. Replace `data/papers.json` with the digest's topic, issue metadata, filters, and paper cards.
3. Replace hero image paths with generated or extracted paper figures.
4. Keep credentials and private local paths out of the data file.
5. Validate filtering, card layout, issue links, and GitHub Pages responses before reporting success.
