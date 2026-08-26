# Changelog

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
