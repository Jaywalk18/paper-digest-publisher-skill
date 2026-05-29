---
name: visual-ssl-digest-skill
description: Create, validate, and publish open visual self-supervised learning paper digests. Use when Codex needs to run a daily paper roundup for visual SSL, vision foundation models, image/video pretraining, JEPA/MAE/contrastive/distillation methods, arXiv/OpenReview/conference dedupe, MinerU figure extraction, Markdown reports, optional Feishu Markdown sync, or GitHub Pages publishing without leaking tokens.
---

# Visual SSL Digest

Use this skill to produce a reproducible visual self-supervised learning paper digest and publish it safely. Keep the workflow source-controlled, but never commit local reports, PDFs, extracted paper assets, API tokens, Feishu file tokens, or private workspace paths.

## Workflow

1. **Collect sources**
   - Search recent arXiv listings and conference/OpenReview pages.
   - Prefer stable IDs: arXiv ID, OpenReview ID, DOI.
   - Filter for general visual SSL and representation learning: image/video pretraining, visual foundation models, masked modeling, contrastive learning, JEPA/data2vec, distillation, tokenizer/visual token efficiency, vision-language or multimodal pretraining.
   - Downgrade medical, remote sensing, industrial inspection, robotics, autonomous driving, agriculture, and other vertical domains unless the method clearly transfers to generic visual representation learning.

2. **Deduplicate**
   - Deduplicate first by stable ID.
   - Fall back to normalized titles: lowercase, remove punctuation, version labels, and status words.
   - If a paper appears in both arXiv and a conference page, merge into one item and list both sources.
   - Treat replacement-only updates as status changes, not new recommendations.

3. **Write the report**
   - Start with a short summary table, reading route, and paper index.
   - Split conference/top-tier dynamics from arXiv new/update items.
   - For each selected paper include title, authors, source, date/status, core method, contribution, experiment highlights, limitations, and relevance to general visual SSL.
   - Avoid copying abstracts. Paraphrase.

4. **Prepare MinerU extraction**
   - Use `scripts/parse_paper_index.py` to confirm which arXiv IDs are in the index.
   - Use `scripts/prepare_mineru_batch.py` before a real MinerU run. It removes stale PDFs and clears `page_preview.jpg` fallback directories that would otherwise make batch scripts skip real extraction.
   - Run the user's MinerU batch client separately. Tokens must come from environment variables or local config outside the repository.
   - Only use PDF preview fallbacks when MinerU fails or exceeds a reasonable wait. Label preview fallbacks honestly.

5. **Publish and validate**
   - Build the static site from the Markdown report and extracted figure assets.
   - Run `scripts/validate_digest_site.py` before pushing.
   - Verify local issue page exists, homepage has a hero figure, no `page_preview.jpg` remains after true extraction, P0/P1 papers have images, and git status is clean after publishing.
   - Check GitHub Pages URLs with a commit cache-buster.

6. **Sync optional destinations**
   - Feishu Markdown sync is optional. Keep file tokens and app credentials out of git.
   - Run `scripts/scan_for_secrets.py` before committing or publishing the skill/repo.

## Script Use

- `scripts/parse_paper_index.py --report path/to/YYYY-MM-DD.md --format table`
  extracts arXiv IDs, titles, priorities, and types from the report index.
- `scripts/prepare_mineru_batch.py --report path/to/report.md --staging-dir path/to/staging --mineru-root path/to/assets/mineru --download`
  prepares only the indexed PDFs and removes PDF-preview fallback directories.
- `scripts/validate_digest_site.py --site-root path/to/site --date YYYY-MM-DD --report path/to/report.md`
  validates issue HTML, hero images, image coverage, and preview leakage.
- `scripts/scan_for_secrets.py --root path/to/repo`
  scans for obvious token/secret patterns before publishing.

## References

- Read `references/workflow.md` for report structure, ranking, dedupe, and publishing checks.
- Read `references/security.md` before committing, pushing, or making a repository public.
