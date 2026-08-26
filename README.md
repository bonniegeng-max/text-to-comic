# text-to-comic v2.0.0

中文 | [English](#english)

## 中文

基于已安装的 `@bonniegeng-max/text-to-comic` 真实 `1.0.0` 版本整理出的 **2.0.0 发布级草案**。

这个版本保留了原版 skill 的产品方向：
- 自动判断内容类型
- 自动选择视觉形式
- 推荐风格
- 关注主角一致性与场景连续性
- 支持漫画 / 绘本 / 信息图 / 混合视觉表达

同时补上了更适合发布、复用和扩展的结构化能力：
- `style preset` 注册表
- `panel plan` schema
- `render task` schema
- per-panel retry / fallback
- 示例输入文件
- 最小脚本工具

### 为什么做 2.0.0

已安装的 `1.0.0` 版本在“产品思路”上已经很成熟，但在“发布级工程结构”上还有几个明显缺口：

- 风格能力主要靠 prose 描述，不够结构化
- storyboard 没有统一 JSON 中间层
- retry / fallback 是经验规则，不是显式机制
- 单格修复没有标准任务格式
- 不方便未来拆分为多个 skill

2.0.0 的目标不是推翻旧版，而是把旧版中有效的导演式工作流，沉淀成更稳定、更可复用的结构。

### 本仓库建议提交/发布的内容

```text
SKILL.md
README.md
CHANGELOG.md
skill-card.md
RELEASE_NOTES_2.0.0.md
presets/
schemas/
examples/
scripts/
```

以下目录不建议发布：
- `skills/`（安装快照）
- `.clawhub/`
- `.clawhub-cli/`

### 目录说明

```text
.
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── skill-card.md
├── RELEASE_NOTES_2.0.0.md
├── .gitignore
├── presets/
│   └── styles.json
├── schemas/
│   ├── panel-plan.schema.json
│   └── render-task.schema.json
├── examples/
│   ├── four-panel-demo.json
│   └── infographic-demo.json
└── scripts/
    ├── compile_prompt.py
    └── validate_panel_plan.py
```

### 2.0.0 的核心升级

#### 1. 风格结构化
把 v1 的 11 种风格，改造成可发布的 preset：
- `style_id`
- `legacy_name_zh`
- `positive_prompt_template`
- `negative_prompt_template`
- `use_cases`
- `avoid_cases`
- `fallback_style_id`
- `stability_rank`

#### 2. 分镜结构化
用 `schemas/panel-plan.schema.json` 统一描述：
- `visual_form`
- `format`
- `style_id`
- `character_bible`
- `panels[]`
- `assembly`

#### 3. 重试机制显式化
用 `schemas/render-task.schema.json` 表达：
- 每格的 prompt
- negative prompt
- attempt 次数
- validation 结果
- retry / fallback 决策

#### 4. 单格修复成为一等能力
2.0.0 默认优先：
- 单格修复
- 风格微调
- 保留已成功格子
- 避免整页重来

### 默认行为

如果用户只说：
> 把这段日记画成漫画

2.0.0 默认会：
- 判断为 narrative / dialog / hybrid 中的合理类型
- 选择 `comic` 视觉形式
- 选择 `4-panel` 或 `6-panel`
- 默认使用稳定风格（如 `slice-of-life-color`）
- 先生成 compact storyboard，再逐格渲染

### 重试策略

默认 retry ladder：
1. 缩短对白或把文字移出图内
2. 减少背景复杂度
3. 改成更稳镜头（如 `medium`）
4. 减少配角
5. fallback 到更稳的 style preset

### 示例

- `examples/four-panel-demo.json`：四格梗图示例
- `examples/infographic-demo.json`：信息图示例

### 最小工具脚本

- `scripts/compile_prompt.py`
  - 从 `panel plan + style preset` 编译每格 prompt
- `scripts/validate_panel_plan.py`
  - 校验 `panel plan` 是否符合 schema 与基本业务规则

### 发布建议

发布到 GitHub / ClawHub 前，建议先确认：
1. 版本号使用 `2.0.0`
2. 是否继续保持 `text-to-comic` 这个 slug
3. 是否下一步拆为两个 skill：
   - `text-to-comic`
   - `text-to-infographic` 或 `text-to-visual`
4. 是否要补一版更贴近 ClawHub 展示风格的英文短说明

### 下一步建议

高优先级：
- 用真实任务跑 1~2 次 `compile_prompt.py`
- 用你自己的典型输入补 2~3 个 examples
- 根据实际效果收缩部分风格 preset 的 use case

中期建议：
- 补一个 panel-level QA script
- 增加 webtoon 示例
- 未来拆 skill

---

## English

A **publish-ready 2.0.0 draft** rebuilt from the real installed `1.0.0` release of `@bonniegeng-max/text-to-comic`.

This version preserves the strong product direction of the original skill:
- automatic content-type classification
- automatic visual-form selection
- style recommendation
- strong emphasis on character consistency and scene continuity
- support for comics, picture books, infographics, and hybrid visual outputs

At the same time, it adds structure that makes the skill easier to publish, reuse, validate, and extend:
- a `style preset` registry
- a `panel plan` schema
- a `render task` schema
- per-panel retry / fallback
- example payloads
- minimal helper scripts

### Why 2.0.0

The installed `1.0.0` version already has a strong “visual director” product shape, but it lacks several publish-grade engineering pieces:

- style behavior is mostly prose-driven
- storyboard artifacts are not normalized as JSON
- retry and fallback are implied rather than formalized
- single-panel repair is not represented as a first-class task
- the package is harder to evolve into multiple specialized skills later

The goal of `2.0.0` is not to replace the old workflow, but to make that workflow more structured, stable, and reusable.

### Recommended publishable contents

```text
SKILL.md
README.md
CHANGELOG.md
skill-card.md
RELEASE_NOTES_2.0.0.md
presets/
schemas/
examples/
scripts/
```

Do not publish local install artifacts such as:
- `skills/`
- `.clawhub/`
- `.clawhub-cli/`

### Repository layout

```text
.
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── skill-card.md
├── RELEASE_NOTES_2.0.0.md
├── .gitignore
├── presets/
│   └── styles.json
├── schemas/
│   ├── panel-plan.schema.json
│   └── render-task.schema.json
├── examples/
│   ├── four-panel-demo.json
│   └── infographic-demo.json
└── scripts/
    ├── compile_prompt.py
    └── validate_panel_plan.py
```

### Key upgrades in 2.0.0

#### 1. Structured styles
The original 11 style families are preserved, but turned into explicit presets with:
- `style_id`
- `legacy_name_zh`
- `positive_prompt_template`
- `negative_prompt_template`
- `use_cases`
- `avoid_cases`
- `fallback_style_id`
- `stability_rank`

#### 2. Structured storyboarding
`schemas/panel-plan.schema.json` provides a normalized structure for:
- `visual_form`
- `format`
- `style_id`
- `character_bible`
- `panels[]`
- `assembly`

#### 3. Formal retry model
`schemas/render-task.schema.json` captures:
- prompt
- negative prompt
- attempt count
- validation result
- retry / fallback decision

#### 4. Single-panel repair as a first-class path
The default revision flow prefers:
- panel-level repair
- style tuning
- keeping successful panels
- avoiding full-page reruns when the problem is local

### Default behavior

If a user simply says:
> Turn this diary entry into a comic.

The skill will usually:
- classify the request as narrative / dialog / hybrid
- choose `comic` as the visual form
- choose `4-panel` or `6-panel`
- default to a stable style such as `slice-of-life-color`
- create a compact storyboard before panel-by-panel rendering

### Retry behavior

Default retry ladder:
1. shorten or externalize text
2. simplify background
3. switch to a more stable shot such as `medium`
4. reduce side characters
5. fall back to a more stable preset

### Examples

- `examples/four-panel-demo.json`: 4-panel comic example
- `examples/infographic-demo.json`: infographic example

### Minimal helper scripts

- `scripts/compile_prompt.py`
  - compiles per-panel prompts from a panel plan and style preset registry
- `scripts/validate_panel_plan.py`
  - validates panel plan JSON against schema and basic business rules

### Recommended next steps

High priority:
- run 1–2 real tasks through `compile_prompt.py`
- add 2–3 more examples based on your most common user inputs
- refine style use cases based on actual output quality

Mid-term:
- add panel-level QA tooling
- add a webtoon example
- split the skill into multiple focused skills later
