#!/usr/bin/env python3
"""Validate panel plan JSON with simple business checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def expected_panel_count(format_name: str) -> int | None:
    mapping = {
        "single": 1,
        "4-panel": 4,
        "6-panel": 6,
        "8-panel": 8,
        "10-panel": 10,
        "12-panel": 12,
    }
    return mapping.get(format_name)


def validate(plan: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required_top = ["story_id", "visual_form", "format", "language", "style_id", "panels"]
    for key in required_top:
        if key not in plan:
            errors.append(f"missing top-level field: {key}")

    panels = plan.get("panels", [])
    if not isinstance(panels, list) or not panels:
        errors.append("panels must be a non-empty array")
        return errors

    exp_count = expected_panel_count(plan.get("format", ""))
    if exp_count is not None and len(panels) != exp_count:
        errors.append(f"format {plan.get('format')} expects {exp_count} panels, got {len(panels)}")

    panel_ids = set()
    for idx, panel in enumerate(panels, start=1):
        for field in ["panel_id", "narrative_role", "shot", "scene", "action", "emotion", "dialogue", "must_include", "avoid"]:
            if field not in panel:
                errors.append(f"panel {idx} missing field: {field}")
        panel_id = panel.get("panel_id")
        if isinstance(panel_id, int):
            if panel_id in panel_ids:
                errors.append(f"duplicate panel_id: {panel_id}")
            panel_ids.add(panel_id)
        text_budget = panel.get("text_budget")
        if text_budget is not None and not isinstance(text_budget, int):
            errors.append(f"panel {panel_id} text_budget must be integer")
        dialogue = panel.get("dialogue", [])
        if not isinstance(dialogue, list):
            errors.append(f"panel {panel_id} dialogue must be array")
        else:
            total_chars = 0
            for line in dialogue:
                if not isinstance(line, dict) or "text" not in line:
                    errors.append(f"panel {panel_id} has invalid dialogue item")
                    continue
                total_chars += len(str(line.get("text", "")))
            if isinstance(text_budget, int) and total_chars > text_budget * 3:
                errors.append(
                    f"panel {panel_id} dialogue looks too long for text_budget={text_budget} (chars={total_chars})"
                )
        must_include = panel.get("must_include", [])
        avoid = panel.get("avoid", [])
        if not isinstance(must_include, list) or not isinstance(avoid, list):
            errors.append(f"panel {panel_id} must_include/avoid must be arrays")

    if plan.get("visual_form") == "infographic" and plan.get("format") != "single":
        errors.append("visual_form=infographic should usually use format=single")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate panel plan JSON.")
    parser.add_argument("panel_plan", help="Path to panel plan JSON")
    args = parser.parse_args()

    plan = load_json(Path(args.panel_plan))
    errors = validate(plan)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, "errors": []}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
