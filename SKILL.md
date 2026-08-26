---
name: text-to-comic
description: 将用户文字、照片说明或知识内容转化为漫画、绘本或信息图；先做结构化 storyboard/panel plan，再逐格出图、校验与拼版，适用于需要风格推荐、角色一致性和可迭代修改的视觉化任务。
metadata: { "openclaw": { "os": ["darwin","linux"], "requires": { "bins": ["python3"], "config": ["image_gen.enabled"] } } }
user-invocable: true
disable-model-invocation: false
---

# text-to-comic v2

## Purpose

Turn user-provided text, photo descriptions, dialog, diary entries, poems, or knowledge notes into a visual deliverable that fits the material best:
- multi-panel comic
- picture-book spread
- infographic
- hybrid comic + diagram page

Preserve the strong parts of v1:
- automatic content-type judgment
- visual-form selection
- style recommendation
- character consistency
- scene continuity
- clean-image assembly

Add v2 structure so results are easier to control and revise:
- style presets from `presets/styles.json`
- structured panel plan from `schemas/panel-plan.schema.json`
- per-panel render task and retry record from `schemas/render-task.schema.json`
- panel-by-panel rendering instead of one-shot full-page generation

## When to use

Use this skill when the user wants to:
- draw a story as a comic or picture book
- convert dialog into a 4-panel or short comic
- turn a concept or workflow into a visual infographic
- convert travel notes, diary entries, or photo notes into illustrated output
- iterate on style, storyboard, or single-panel fixes instead of regenerating everything

Do not use this skill when the task is mainly:
- pure text writing with no visual output
- exact imitation of a living artist's distinctive signature style
- direct reproduction of copyrighted third-party material

## Decision flow

1. Classify the input as one of:
   - narrative
   - dialog
   - knowledge
   - poetic
   - hybrid
2. Choose a visual form:
   - `comic`
   - `picture-book`
   - `infographic`
   - `hybrid`
3. Pick a default format:
   - `4-panel` for short dialog or punchline-based requests
   - `6-panel` to `8-panel` for short narrative arcs
   - `single` for infographic or single illustration
   - `webtoon` for vertical, dramatic, mobile-first storytelling
4. Pick a style preset from `presets/styles.json`.
5. Build a compact `panel plan`.
6. Render panel by panel.
7. Validate, retry if needed, then assemble the final output.

## Compatibility with v1

Keep the old experience as the default:
- If the user simply says "画成漫画" or gives a short story, still auto-select a reasonable format and style.
- Keep broad support for comics, picture books, and infographics.
- Keep the v1 ideas of storyboard confirmation, character cards, scene labels, clean-image suffixes, and PIL-based assembly.

New in v2:
- Use style IDs instead of only prose style names.
- Store storyboard as structured JSON.
- Track retries and fallbacks per panel.
- Make single-panel regeneration a first-class path.

## Core workflow

### 1. Analyze the request

Identify:
- content type
- likely visual form
- target audience
- tone
- whether the request contains a stable protagonist, multiple scenes, or mainly conceptual information

If the task is obvious, present a compact plan and continue.
Ask the user to confirm before rendering when any of the following is true:
- the content could reasonably become more than one visual form
- the style choice materially changes tone
- the story needs more than 8 panels
- the request contains private or sensitive photo material
- the user supplied copyrighted third-party source text that may need summarization first

### 2. Create the story/panel plan

Represent the visual plan with the schema in `schemas/panel-plan.schema.json`.

Requirements:
- one key beat per panel
- panel count should match narrative complexity
- the last panel should carry payoff, twist, conclusion, or CTA
- keep dialog short enough to remain readable after layout
- if scenes change, make transitions legible

For infographic mode:
- use `visual_form = infographic`
- use `format = single`
- still produce a `panels` array, usually with one major page and multiple structured sections inside the scene/action/must_include fields

### 3. Create a character bible when needed

If a stable protagonist or recurring cast exists, create a compact character bible and reuse the same visual anchors in every panel.

Minimum character anchors:
- age/gender presentation when relevant
- hair
- face shape
- eyewear if any
- outfit
- accent color
- body build or silhouette
- vibe/expression

Keep these anchors stable across all panels.

### 4. Select and compile style preset

Use `presets/styles.json` as the source of truth for supported styles.

Each render prompt should combine:
- style positive template
- character-bible summary
- panel scene
- panel action
- shot type
- emotion
- must-include list
- avoid list
- global clean-image suffix

If the user gives a reference style image or a very specific style direction:
- preserve the selected `style_id`
- add a short reference-derived modifier instead of replacing the whole preset
- do not promise exact style cloning

### 5. Render panel by panel

Do not render the full page in one shot unless the request is explicitly a single illustration or infographic.

For comics or picture books:
- generate each panel independently
- keep output paths and retry records separate
- prefer clean images without embedded panel numbering
- if in-image text is unavoidable, keep it short and in English for image generation reliability
- add Chinese captions, narration, or labels during assembly when possible

### 6. Validate each panel

Validate against these priorities:
- character consistency
- scene continuity
- clean image without watermark/signature/panel numbering
- readable composition
- dialog within `text_budget`
- no obviously broken face or limb rendering

If a panel fails validation, retry with a bounded mutation ladder.

### 7. Retry policy

Use `schemas/render-task.schema.json` for retry bookkeeping.

Retry ladder:
1. shorten dialog or move text out of the image
2. simplify background and reduce secondary props
3. switch to a more stable shot such as `medium`
4. reduce side characters
5. fall back to a more stable style preset when appropriate

Stop conditions:
- default maximum 2 retries per panel unless the user explicitly wants more
- if the panel still fails after fallback, return the best valid storyboard plus the strongest attempt rather than silently looping

### 8. Assemble final output

Assembly defaults:
- `4-panel`: 2x2 grid
- `6-panel` or `8-panel`: balanced grid with consistent gutters
- `webtoon`: vertical stack
- `single`: single page or single image

Assembly rules preserved from v1:
- crop to target ratio before final resize
- avoid panel numbering inside generated images
- keep a clean margin and readable caption area
- use warm off-white backgrounds for comic boards unless the chosen style clearly calls for another background

## Hard constraints

### Character consistency

If the story has a main character, every panel should clearly look like the same person.
Reuse the same core descriptors and avoid drifting outfit, hair, face shape, or accent color.

### Language separation

Prefer:
- English for minimal in-image text if generation quality depends on it
- Chinese for captions, narration, or post-assembly overlay

If the user explicitly wants all-Chinese bubbles, try it, but still favor readability and brevity.

### Scene continuity

Use clear indoor/outdoor/street/home/office/etc. tags in planning when scene continuity matters.
Add a transition panel if a major scene jump would feel abrupt.

### Clean image rule

Use a clean-image suffix equivalent to:
- no border
- no panel frame
- no watermark
- no AI signature
- no accidental page numbering
- edge-to-edge composition

### Copyright boundary

Allowed:
- user-owned stories
- user summaries of ideas or experiences
- original educational reframing

Disallowed:
- direct transformation of substantial copyrighted text or art into near-derivative output
- exact imitation of a protected living artist's signature style

## Output contract

Default user-facing output should include:
- a compact explanation of chosen visual form and style
- a short storyboard summary
- final image(s) or assembled page
- concise notes if any panel required retries or fallback

Internally keep these artifacts whenever useful:
- `panel_plan.json`
- per-panel render task records
- retry notes

Do not force raw JSON on the user unless they ask for it or the task benefits from editable intermediate output.

## Style system

Supported style presets live in `presets/styles.json`.

v2 keeps the spirit of the v1 style library while making it easier to render and retry:
- bright cute cartoon
- warm watercolor picture book
- Japanese shonen manga
- colorful slice-of-life manga
- Chinese gongbi comic
- ink wash comic
- 3D cartoon animation
- claymation
- sci-fi future comic
- vintage watercolor travelogue
- doodle sketch comic

When a request is ambiguous, recommend 2 to 3 styles instead of forcing a single one.

## Example resources

If you need a concrete starting point, read:
- `examples/four-panel-demo.json`
- `presets/styles.json`
- `schemas/panel-plan.schema.json`
- `schemas/render-task.schema.json`

## Revision behavior

When the user asks for changes:
- prefer single-panel repair when the issue is local
- change style preset only if the issue is stylistic, not compositional
- change the storyboard only if the problem is narrative
- carry forward the validated character bible and successful panels whenever possible
