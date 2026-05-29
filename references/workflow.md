# Workflow Reference

## Report Shape

Use this order:

1. Title with date.
2. Retrieval window and source list.
3. Quick summary table, 5-8 rows.
4. Reading route, 3-5 sentences.
5. Paper index table with priority, paper, type, relevance, one-line reason.
6. Conference/top-tier dynamics.
7. arXiv new/update section.
8. Detailed paper entries.
9. Trend observations.
10. Dedupe notes.

## Ranking

Use P0 for papers that directly improve general visual representation learning or strongly affect visual foundation model training/evaluation.

Use P1 for strong adjacent work: visual tokenization, VLM/VFM efficiency, multimodal embedding, video pretraining, or high-value conference status.

Use P2/P3 for downstream adaptation, diagnostics, benchmarks, and method-adjacent work.

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
