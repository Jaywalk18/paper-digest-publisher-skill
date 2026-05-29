---
name: paper-digest-publisher-skill
description: Create, validate, and publish open research paper digests for any user-defined topic. Use when Codex needs to run a recurring or one-off paper roundup with configurable scope, source tiers, dedupe, priority ranking, MinerU/PDF figure extraction, Markdown reports, optional Feishu/Lark Markdown sync, reusable static web templates, or GitHub Pages publishing without leaking tokens.
---

# Paper Digest Publisher

Use this skill to produce a reproducible research paper digest for a topic the user defines, then publish it safely as Markdown and optionally as a static website. Keep the workflow source-controlled, but never commit local reports, PDFs, extracted paper assets, API tokens, Feishu/Lark file tokens, or private workspace paths.

## Topic Profile

Before collecting papers, establish a topic profile from the user's request or automation memory:

- `topic_name`: human-readable title, such as "General Vision Pretraining" or "LLM Agents for Software Engineering".
- `scope_include`: methods, venues, keywords, source lists, and adjacent areas to prioritize.
- `scope_exclude`: vertical domains or weakly related work to downgrade or filter.
- `source_tiers`: conference/OpenReview/official pages, preprints, project pages, datasets, code releases, or other sources.
- `priority_rubric`: how to assign P0/P1/P2/P3/scan-only for this topic.
- `report_shape`: required sections, language, local archive paths, and sync targets.
- `web_style`: whether to use an existing site builder or copy/adapt `assets/web-template/`.

If the topic is underspecified, infer a conservative profile, state the assumptions in the report, and avoid broadening into unrelated domains.

## Workflow

1. **Collect sources**
   - Search the source tiers in the topic profile for the target time window.
   - Prefer stable IDs: arXiv ID, OpenReview ID, DOI.
   - Apply the include/exclude rules before ranking. Downgrade narrow vertical work unless it clearly transfers to the topic's core problem.
   - Keep source categories separate when the user cares about status changes: accepted papers, workshop/oral/spotlight items, OpenReview updates, arXiv new papers, and arXiv replacements.

2. **Deduplicate**
   - Deduplicate first by stable ID.
   - Fall back to normalized titles: lowercase, remove punctuation, version labels, and status words.
   - If a paper appears in both arXiv and a conference page, merge into one item and list both sources.
   - Treat replacement-only updates as status changes, not new recommendations.

3. **Write the report**
   - Start with a short summary table, reading route, and paper index.
   - Split source categories according to the topic profile, such as conference dynamics and arXiv new/update items.
   - For each selected paper include title, authors, source, date/status, core method, contribution, experiment highlights, limitations, and relevance to the configured topic.
   - Avoid copying abstracts. Paraphrase.

4. **Prepare MinerU extraction**
   - Use `scripts/parse_paper_index.py` to confirm which arXiv IDs are in the index.
   - Use `scripts/prepare_mineru_batch.py` before a real MinerU run. It removes stale PDFs and clears `page_preview.jpg` fallback directories that would otherwise make batch scripts skip real extraction.
   - Run the user's MinerU batch client separately. Tokens must come from environment variables or local config outside the repository.
   - Only use PDF preview fallbacks when MinerU fails or exceeds a reasonable wait. Label preview fallbacks honestly.

5. **Publish and validate**
   - Build the static site from the Markdown report and extracted figure assets. If no site builder exists, copy and adapt `assets/web-template/`.
   - Run `scripts/validate_digest_site.py` before pushing.
   - Verify local issue page exists, homepage has a hero figure, no `page_preview.jpg` remains after true extraction, P0/P1 papers have images when figures are expected, and git status is clean after publishing.
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
- Use `assets/web-template/` as a generic HTML/CSS/JS template for a topic digest site when no project-specific site exists.
