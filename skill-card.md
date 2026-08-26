## Description:

text-to-comic 2.0.0 turns user-provided stories, dialog, diary entries, poems, travel notes, photos, or knowledge summaries into comics, picture-book pages, infographics, or hybrid visual outputs.

Compared with the original 1.0.0 release, this version keeps the same creator-friendly product direction while adding a structured planning layer:
- style presets
- panel-plan JSON
- render-task JSON
- per-panel retry and fallback
- single-panel repair workflow

This skill is suitable for creators who want stronger controllability, repeatability, and easier iteration before publishing visual content.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

Use this skill to:
- turn a diary entry into a multi-panel comic
- convert dialog into a 4-panel strip
- turn a poem into a picture-book-like visual sequence
- convert a concept or framework into an infographic
- iterate on a single weak panel without rerendering the whole page

## Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text, reference images, or photo descriptions may be processed by the configured image-generation provider.

Mitigation: Avoid submitting private or sensitive material unless the user is comfortable with that processing.

Risk: Generated panels may contain inconsistent characters, visual artifacts, or style drift.

Mitigation: Use the panel plan, render task records, and bounded retry/fallback workflow to review outputs before release.

Risk: Third-party copyrighted material may lead to derivative outputs if used directly.

Mitigation: Prefer original, summarized, or rights-cleared source material and avoid direct transformation of copyrighted works.

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, Files]

**Output Format:** [Storyboard summaries, JSON intermediate artifacts, prompts, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output assembled PNG or JPEG pages; requires python3 and image generation to be enabled.]

## Skill Version(s):

2.0.0 (proposed next release)

## Ethical Considerations:

Users should review all generated images, prompts, and intermediate artifacts before release, and should apply their own safety, legal, privacy, and compliance standards.
