# Paper Digest Publisher Skill / 论文速递发布 Skill

**中文**：一个开源 Codex skill，用来生成任意研究主题的论文速递。它覆盖主题配置、来源分层、去重、优先级排序、Markdown 日报、可选 MinerU 图文抽取、静态网页模板和 GitHub Pages 发布检查。

**English**: An open Codex skill for building topic-specific research paper digests. It covers topic configuration, source tiers, deduplication, priority ranking, Markdown reports, optional MinerU figure extraction, static web templates, and GitHub Pages validation.

**中文**：它不局限于视觉自监督。你可以定义一个主题画像，然后把同一套流程用于视觉、NLP、Agent、机器人、系统、评测基准或其他研究方向。

**English**: It is not limited to visual self-supervised learning. Define a topic profile, then reuse the workflow for vision, NLP, agents, robotics, systems, benchmarks, or any other research area.

![Example digest site / 论文速递网站示例](assets/readme/visual-ssl-digest-example.png)

**中文**：上图是用这个流程生成的视觉自监督论文速递网站示例。这个 skill 本身是通用的，示例主题可以替换。

**English**: The screenshot shows an example digest site generated for a visual self-supervised learning topic. The skill itself is generic, and the example topic can be replaced.

## 可配置内容 / What You Can Configure

| 配置项 / Area | 中文说明 | English |
| --- | --- | --- |
| 主题 / Topic | 例如通用视觉预训练、LLM Agent、扩散模型、AI 系统、检索、评测基准 | General visual pretraining, LLM agents, diffusion models, AI systems, retrieval, evaluation benchmarks |
| 纳入范围 / Scope include | 方法、会议、关键词、作者、任务、项目页、代码发布 | Methods, venues, keywords, authors, tasks, project pages, code releases |
| 排除范围 / Scope exclude | 过窄垂直应用、弱相关论文、重复性 benchmark 更新 | Narrow vertical domains, weakly related applications, repeated benchmark-only updates |
| 来源分层 / Source tiers | arXiv、OpenReview、会议官网、workshop 页面、接收列表、项目页 | arXiv, OpenReview, conference pages, workshop pages, official accepted-paper lists, project pages |
| 优先级规则 / Priority rubric | 自定义 P0/P1/P2/P3/扫读 在当前主题下的含义 | Custom meaning of P0/P1/P2/P3/scan-only for the topic |
| 报告结构 / Report shape | 快速摘要、阅读路线、论文索引、趋势观察、详细条目 | Summary table, reading route, paper index, trend notes, detailed entries |
| 发布目标 / Publishing | 本地 Markdown、飞书/Lark Markdown、静态 HTML、GitHub Pages | Local Markdown, Feishu/Lark Markdown sync, static HTML, GitHub Pages |
| 网页风格 / Website style | 使用已有站点构建器，或改造 `assets/web-template/` | Use an existing site builder or adapt `assets/web-template/` |

## 主题画像示例 / Topic Profile Example

**中文**：下面是一个“通用视觉预训练”主题画像。换主题时，主要改 `topic_name`、纳入/排除范围、来源分层和优先级定义。

**English**: This is a topic profile for "General Vision Pretraining". To switch topics, change `topic_name`, include/exclude scope, source tiers, and the priority rubric.

```yaml
topic_name: "General Vision Pretraining"
retrieval_window: "last 24-48 hours"
scope_include:
  - image/video pretraining
  - vision foundation models
  - masked modeling
  - contrastive learning
  - distillation and representation learning
scope_exclude:
  - medical-only applications
  - remote-sensing-only applications
  - industrial inspection unless the method transfers
source_tiers:
  - conference and workshop pages
  - OpenReview
  - arXiv new and updated papers
priority_rubric:
  P0: "Read first; directly changes the core topic"
  P1: "Strong adjacent or high-signal status change"
  P2: "Useful but less urgent"
  P3: "Record or scan"
outputs:
  markdown_dir: "path/to/reports"
  site_dir: "path/to/static-site"
  github_pages: true
```

## 仓库结构 / Repository Layout

| 路径 / Path | 中文说明 | English |
| --- | --- | --- |
| `SKILL.md` | Codex skill 入口和核心流程 | Codex skill entry point and core workflow |
| `references/workflow.md` | 报告结构、去重、排序、MinerU 和发布检查细节 | Detailed reporting, dedupe, ranking, MinerU, and publishing checks |
| `references/security.md` | 公开仓库禁止提交的内容 | What must never be committed |
| `scripts/parse_paper_index.py` | 从报告索引中提取优先级、标题、类型和 arXiv ID | Extract priorities, titles, types, and arXiv IDs from a report index |
| `scripts/prepare_mineru_batch.py` | 准备索引中的 PDF，并清理旧的预览 fallback 资产 | Prepare indexed PDFs and clear stale preview fallback assets before MinerU |
| `scripts/validate_digest_site.py` | 验证静态站点输出和图片覆盖情况 | Validate static site output and image coverage |
| `scripts/scan_for_secrets.py` | 发布前扫描明显 token 和 secret 模式 | Scan for obvious token and secret patterns before publishing |
| `assets/web-template/` | 可复制改造的 HTML/CSS/JS 论文速递网站模板 | Copyable HTML/CSS/JS template for a paper digest site |

## 网页模板 / Website Template

**中文**：`assets/web-template/` 是一个轻量静态站点模板，AI agent 可以直接复制到目标项目后改造。它包含：

**English**: `assets/web-template/` is a small static site template that an AI agent can copy into a target project and adapt. It includes:

- 中文：首页、主推论文区域、优先级/主题筛选、卡片搜索、趋势与归档区、样例 `data/papers.json`、占位论文图。
- English: digest homepage, featured paper hero area, priority/topic filters, card search, trend/archive sections, sample `data/papers.json`, and a placeholder paper figure.

**中文**：适配时，把 `assets/web-template/data/papers.json` 替换为生成后的论文数据，并把图片路径替换为 MinerU 抽取图、论文图或稳定公开图片。

**English**: To adapt it, replace `assets/web-template/data/papers.json` with generated digest data and swap image paths for MinerU-extracted figures, paper figures, or other stable public assets.

## 安全发布规则 / Safe Publishing Rules

**中文**：公开仓库不要提交以下内容：

**English**: Never commit the following to a public repository:

- API keys or GitHub tokens / API key 或 GitHub token
- MinerU JWTs or local MinerU config / MinerU JWT 或本地 MinerU 配置
- Feishu/Lark app secrets, access tokens, refresh tokens, or file tokens / 飞书/Lark app secret、access token、refresh token 或 file token
- generated paper PDFs / 生成或下载的论文 PDF
- private reports / 私有日报或内部报告
- MinerU extraction outputs from private runs / 私有任务产生的 MinerU 抽取结果

**中文**：公开发布前建议运行：

**English**: Before pushing a public repo, run:

```bash
python scripts/scan_for_secrets.py --root .
git status --short
git diff --cached --stat
```

## 示例 Prompt / Example Prompt

```text
Use $paper-digest-publisher-skill to generate and publish a paper digest for
LLM agents for software engineering. Focus on the last 48 hours, prioritize
papers with reusable agentic coding methods, downgrade narrow product-only
case studies, and publish a Markdown report plus a static website.
```

```text
使用 $paper-digest-publisher-skill 生成并发布一个“软件工程方向 LLM Agent”
论文速递。关注最近 48 小时，优先推荐可复用的 agentic coding 方法，
降低只面向单一产品场景的案例研究优先级，并同时发布 Markdown 报告和静态网站。
```

## 许可证 / License

MIT
