#!/usr/bin/env python3
"""Compile panel prompts from a panel plan and a style preset registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def summarize_character_bible(character_bible: List[Dict[str, Any]]) -> str:
    if not character_bible:
        return ""
    chunks: List[str] = []
    for character in character_bible:
        appearance = character.get("appearance", {})
        ordered = [
            appearance.get("age_presentation"),
            appearance.get("hair"),
            appearance.get("face"),
            appearance.get("eyewear"),
            appearance.get("outfit"),
            appearance.get("accent_color"),
            appearance.get("build"),
            appearance.get("vibe"),
        ]
        text = ", ".join([x for x in ordered if x])
        keep = ", ".join(character.get("must_keep", []))
        if keep:
            text = f"{character.get('name', 'character')}: {text}; must keep: {keep}"
        else:
            text = f"{character.get('name', 'character')}: {text}"
        chunks.append(text.strip())
    return " | ".join(chunks)


def build_style_index(styles_doc: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {style["style_id"]: style for style in styles_doc.get("styles", [])}


def compile_panel_prompt(panel_plan: Dict[str, Any], style: Dict[str, Any], panel: Dict[str, Any], clean_suffix: str) -> Dict[str, Any]:
    character_summary = summarize_character_bible(panel_plan.get("character_bible", []))
    must_include = ", ".join(panel.get("must_include", []))
    avoid = ", ".join(panel.get("avoid", []))
    dialogue_lines = []
    for item in panel.get("dialogue", []):
        speaker = item.get("speaker", "")
        text = item.get("text", "")
        if text:
            dialogue_lines.append(f"{speaker}: {text}".strip())
    dialogue_text = " | ".join(dialogue_lines)

    parts = [
        style.get("positive_prompt_template", ""),
        f"visual form: {panel_plan.get('visual_form', '')}",
        f"format: {panel_plan.get('format', '')}",
        f"shot: {panel.get('shot', '')}",
        f"scene: {panel.get('scene', '')}",
        f"scene tag: {panel.get('scene_tag', '')}",
        f"action: {panel.get('action', '')}",
        f"emotion: {panel.get('emotion', '')}",
    ]
    if character_summary:
        parts.append(f"character bible: {character_summary}")
    if must_include:
        parts.append(f"must include: {must_include}")
    if avoid:
        parts.append(f"avoid: {avoid}")
    if dialogue_text:
        parts.append(f"dialogue reference: {dialogue_text}")
    if clean_suffix:
        parts.append(clean_suffix)

    prompt = ", ".join([p for p in parts if p])
    negative = style.get("negative_prompt_template", "")
    return {
        "panel_id": panel["panel_id"],
        "style_id": style["style_id"],
        "prompt": prompt,
        "negative_prompt": negative,
        "fallback_style_id": style.get("fallback_style_id"),
        "stability_rank": style.get("stability_rank"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile prompts from panel plan JSON.")
    parser.add_argument("panel_plan", help="Path to panel plan JSON")
    parser.add_argument("--styles", default="presets/styles.json", help="Path to styles.json")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    panel_plan = load_json(Path(args.panel_plan))
    styles_doc = load_json(Path(args.styles))
    style_index = build_style_index(styles_doc)

    style_id = panel_plan.get("style_id")
    if style_id not in style_index:
        print(f"Unknown style_id: {style_id}", file=sys.stderr)
        return 2

    style = style_index[style_id]
    clean_suffix = styles_doc.get("global_clean_image_suffix", "")
    compiled = [
        compile_panel_prompt(panel_plan, style, panel, clean_suffix)
        for panel in panel_plan.get("panels", [])
    ]

    output = {
        "story_id": panel_plan.get("story_id"),
        "style_id": style_id,
        "compiled_panels": compiled,
    }
    if args.pretty:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
