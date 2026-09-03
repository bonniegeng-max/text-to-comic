# Changelog

## 2.3.0

Released 2026-09-04. Document-level Chinese typography and layout hardening plus a zh-CN example. JSON schemas are unchanged.

### Added

- `examples/chinese-webtoon-demo.json`: a zh-CN diary / slice-of-life webtoon example (black short hair + round glasses + slim female protagonist), following the same field structure as `examples/four-panel-demo.json`

### Changed

- SKILL.md `Hard constraints`: new "Chinese dialogue and layout (中文对白与排版约束)" subsection with concrete readability limits:
  - per speech bubble ≤ 16 characters, per-panel dialogue ≤ 40 characters, per-panel caption ≤ 25 characters
  - full-width Chinese punctuation requirements
  - short-line / split-gutter layout advice for bubbles
  - vertical-text handling guidance (assembly-layer only)
  - Chinese title-area suggestion during assembly (≤ 12 characters, matching CJK font family)
- SKILL.md `Example resources`: added pointer to `examples/chinese-webtoon-demo.json`

### Compatibility notes

- Slug remains `text-to-comic`
- `schemas/panel-plan.schema.json` and `schemas/render-task.schema.json` are unchanged; the new rules live at the document/planning level only
- Existing v1/v2 outputs remain valid

## 2.2.0

Released 2026-09-01. 新增 topics 与中英双语 description（含触发词），修复 README 版本/目录树问题。

## 2.0.0

This release upgrades the installed ClawHub release `1.0.0` into a publish-ready, structured v2 package.

### Added

- Structured `style preset` registry in `presets/styles.json`
- Structured `panel plan` schema in `schemas/panel-plan.schema.json`
- Structured `render task` schema in `schemas/render-task.schema.json`
- Example payloads in:
  - `examples/four-panel-demo.json`
  - `examples/infographic-demo.json`
- GitHub/ClawHub-oriented bilingual `README.md`
- Updated publishable `skill-card.md`
- `RELEASE_NOTES_2.0.0.md`
- `.gitignore` for local install artifacts
- Helper scripts:
  - `scripts/compile_prompt.py`
  - `scripts/validate_panel_plan.py`

### Changed

- Reframed the skill from a mainly prose-driven visual-director prompt into a staged workflow:
  - analyze
  - plan
  - style compile
  - render
  - validate
  - retry
  - assemble
- Preserved the original broad scope across comics, picture books, infographics, and hybrid outputs
- Preserved the original emphasis on:
  - content-type judgment
  - storyboarding
  - character consistency
  - scene continuity
  - clean-image composition
- Converted legacy style names into stable `style_id` values for repeatable behavior

### Compatibility notes

- Slug remains `text-to-comic`
- Frontmatter remains compatible with the current OpenClaw metadata expectations
- Simple natural-language requests still work without requiring users to provide JSON
- Structured JSON artifacts are additive, not mandatory for end users

### Expected benefits

- More stable output across retries
- Easier single-panel regeneration
- Better publishing review because intermediate artifacts are inspectable
- Less style drift because presets are explicit and reusable
- Easier future split into multiple specialized skills
