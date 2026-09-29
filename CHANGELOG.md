# Changelog

## 2.4.2

Released 2026-09-29. Release-metadata fix only. No file content, schema, or behavior change.

### Fixed

- Restored the ClawHub display name to `Text-to-Comic · 文字转漫画`. Publishing 2.4.0/2.4.1 without `--name` caused ClawHub to fall back to the raw slug, which drops the Chinese search surface.
- Release note: **always publish with `--name "Text-to-Comic · 文字转漫画"`.** `clawhub publish --name "Text-to-Comic · 文字转漫画" --slug text-to-comic --version <v>`.

## 2.4.1

Released 2026-09-29. Ships the character reference sheet that 2.4.0 listed as planned. No behavior change.

### Added

- `characters/protagonist-ref.png`: actual character reference sheet (front / three-quarter / side full-body views + five-expression row), watermark-free. Used only when the host image tool accepts reference images; text anchors remain the source of truth.
- `characters/protagonist.md`: new 配套参考图 section describing when and how to use the sheet.

## 2.4.0

Released 2026-09-29. Default character asset + panel-level quick commands. JSON schemas are unchanged.

### Added

- `characters/protagonist.md`: default character card (black short hair, round glasses, slim young woman). Loaded automatically when the user does not name a protagonist; its visual anchors are injected into every panel prompt, keeping the protagonist consistent across panels and across sessions. Custom protagonists write a temporary `characters/custom-<slug>.md` instead of overwriting the shipped card.
- `characters/protagonist-ref.png`: character reference sheet, used only when the host image tool accepts reference images. *(planned in 2.4.0, shipped in 2.4.1)*
- SKILL.md `Quick commands（快速指令）`:
  - `只出分镜` / `storyboard only` — stop after the panel plan, render nothing
  - `重出第 N 格` / `重出 2,5,8` / `regenerate N` — regenerate only the listed panels, reusing the panel plan and prompts
  - `换画风保留分镜` — keep the storyboard, recompile prompts with a new style preset
- SKILL.md artifact naming convention: `prompts/NN.md` + `pages/NN-<slug>.png` mapped 1:1 to the panels array, making single-panel regeneration reliable.

### Changed

- SKILL.md frontmatter `version`: 2.3.1 → 2.4.0.
- SKILL.md `description`: adds default character card coverage (character card / 角色卡) and quick-command triggers (只出分镜 / 只重出某一格 / 换主角卡).
- SKILL.md step 3: renamed to "Load or create the character bible" — default asset path first, custom path second.
- SKILL.md `Example resources`: lists `characters/protagonist.md`.

## 2.3.1

Released 2026-09-13. ClawHub discoverability fix. Skill behavior is unchanged.

### Added

- SKILL.md `How it differs` section: states plainly that this is not a one-shot image generator, not a style-cloning tool, and not a research tool.
- SKILL.md frontmatter `version` field, for repository hygiene. The published registry version is derived by ClawHub itself.

### Changed

- SKILL.md `description`: now leads with an English problem statement plus a `Not for` clause (pure text writing / imitating a living artist's signature style / reproducing copyrighted material). Chinese trigger coverage retained.
- ClawHub catalog metadata: categories set from `other` to `creative`; topics set to `comic, storyboard, infographic, visual-storytelling, picture-book`.

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
