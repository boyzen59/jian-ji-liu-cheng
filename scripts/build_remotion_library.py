#!/usr/bin/env python3
"""Build a deterministic unified catalog from the five vendored Remotion sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY_ROOT = SKILL_ROOT / "assets" / "remotion-library"


SEMANTIC_RULES: dict[str, tuple[str, ...]] = {
    "explain": (
        "explain", "process", "flow", "step", "mechanism", "guide", "how", "cause", "result",
        "解释", "流程", "步骤", "机制", "因果", "如何", "原因", "结果", "汇入", "组装",
    ),
    "focus": (
        "focus", "highlight", "spotlight", "hero", "emphasis", "reveal", "zoom", "underline",
        "聚焦", "强调", "重点", "关键", "点名", "揭示", "聚光", "下划线",
    ),
    "compare": (
        "compare", "comparison", "before", "after", "versus", "split", "contrast", "slider",
        "比较", "对比", "前后", "差异", "相较", "两列", "分屏",
    ),
    "relate": (
        "relation", "connect", "network", "map", "link", "path", "timeline", "sequence", "stack",
        "关系", "连接", "网络", "路径", "时间线", "阶段", "关联", "层级", "接力",
    ),
    "quantify": (
        "data", "chart", "counter", "stat", "metric", "progress", "gauge", "number", "ranking",
        "数据", "图表", "数字", "统计", "指标", "进度", "仪表", "排名", "百分比",
    ),
    "demonstrate": (
        "demo", "ui", "cursor", "click", "input", "drag", "scroll", "modal", "notification", "interaction",
        "演示", "界面", "光标", "点击", "输入", "拖拽", "滚动", "交互", "操作", "响应",
    ),
    "transition": (
        "transition", "wipe", "cut", "push", "iris", "morph", "cross dissolve", "page turn", "whip",
        "转场", "切换", "擦除", "翻页", "藏切", "推进", "变形", "接场",
    ),
    "identity": (
        "logo", "brand", "intro", "outro", "title", "chapter", "credits", "lower third",
        "品牌", "标志", "片头", "片尾", "标题", "章节", "署名", "收尾", "开场",
    ),
    "rhythm": (
        "rhythm", "beat", "stagger", "roller", "countdown", "montage", "pulse", "typewriter", "karaoke",
        "节奏", "鼓点", "错峰", "滚动", "倒计时", "蒙太奇", "脉冲", "打字", "卡拉ok",
    ),
    "atmosphere": (
        "background", "aurora", "bokeh", "gradient", "grain", "noise", "light leak", "vignette", "ambient",
        "背景", "极光", "光斑", "渐变", "颗粒", "噪点", "漏光", "暗角", "氛围", "若隐若现",
    ),
    "delight": (
        "goo", "liquid", "confetti", "spark", "burst", "bounce", "bubble", "particle", "playful", "flourish",
        "液态", "彩纸", "火花", "爆发", "弹跳", "气泡", "粒子", "趣味", "花式", "惊喜",
    ),
}

EXPERIENCE_ROLES = {"atmosphere", "delight", "rhythm"}

CATEGORY_LAYER_HINTS = {
    "background": ["ambient"],
    "backgroundanimations": ["ambient"],
    "effectanimations": ["support", "ambient"],
    "effects": ["support", "ambient"],
    "particleanimations": ["support", "ambient"],
    "themeanimations": ["ambient", "support"],
    "liquidanimations": ["ambient", "support"],
    "goo": ["ambient", "support"],
    "transition": ["support"],
    "transitionanimations": ["support"],
    "cinematic": ["support", "ambient"],
    "cinematicanimations": ["support", "ambient"],
}

SCENES_DESCRIPTIONS = {
    "BackgroundAnimations": "Ambient backgrounds, gradients, grids, bokeh, and waves.",
    "CinematicAnimations": "Genre-aware cinematic title and mood treatments.",
    "DataAnimations": "Charts, gauges, rankings, progress, and metric cards.",
    "DemoAnimations": "UI actions such as click, drag, input, search, scroll, and modal flows.",
    "EffectAnimations": "Image and overlay treatments including glow, grain, VHS, and depth of field.",
    "LayoutAnimations": "Editorial and asymmetric layouts for arranging text, media, and numbers.",
    "LiquidAnimations": "Fluid, ink, blob, splash, drip, and morphing motion.",
    "ListAnimations": "Lists, timelines, comparisons, grids, and feature sequences.",
    "LogoAnimations": "Logo reveals, morphs, trails, masks, stamps, and rotations.",
    "ParticleAnimations": "Confetti, snow, sparks, smoke, bubbles, and other particle fields.",
    "RollerAnimations": "Rollers, slot machines, counters, typewriters, and rhythmic text changes.",
    "ShapeAnimations": "Geometric forms, rings, ripples, morphs, and spatial shape systems.",
    "TextAnimations": "Kinetic typography, counters, masks, scramble, split, and typewriter effects.",
    "ThemeAnimations": "Complete visual theme studies used as motion and layout references.",
    "TransitionAnimations": "Full-frame and element-led transitions.",
    "UIAnimations": "Reusable interface controls and state changes.",
}

CURVABLE_COMPONENTS: dict[str, tuple[str, str, str]] = {
    "bulb-bg": ("BulbBg", "background", "A rising warm dome and soft halo for an ambient background beat."),
    "cascading-text": ("CascadingText", "text", "Words cascade from the right while the camera steps outward to preserve readability."),
    "curvable-types": ("CurvableTypes", "text", "A large blurred word resolves and makes room for a typed phrase."),
    "ellipse-bloom": ("EllipseBloom", "background", "A two-layer ellipse blooms quickly from a point to fill the frame."),
    "floating-stack": ("FloatingStack", "composite", "Three 3D slabs float in an accordion wave while a cursor visits each slab."),
    "grainient-bg": ("GrainientBg", "background", "A painterly warped gradient drifts without moving a focal subject."),
    "paste-pill": ("PastePill", "text", "A word-level sentence reveal culminates in a cursor click and pill state change."),
    "prompt-input": ("PromptInput", "composite", "A cursor types into a tilted prompt dashboard, submits, and exits."),
    "slide-reveal": ("SlideReveal", "text", "An existing sentence exits while replacement words rise in from below."),
    "stats-grid": ("StatsGrid", "data", "A hero metric transforms into a frosted 2x2 card grid with charts and counters."),
    "text-hover": ("TextHover", "text", "A feathered light sweep reveals color inside outlined text."),
    "text-swap": ("TextSwap", "text", "Letters from one word disappear in pairs while the replacement word settles."),
    "two-drops-bg": ("TwoDropsBg", "background", "Two glowing teardrops travel around opposite sides of a rounded perimeter."),
    "typewriter": ("Typewriter", "text", "Characters arrive in the accent color and settle to the resting text color."),
}

PLAYGROUND_EFFECTS = {
    "GooBall": "A metaball-style goo sphere study.",
    "GooBallCSS": "A CSS implementation of the goo ball effect.",
    "GooBallDrip": "A goo ball that stretches into a drip.",
    "GooDrippings": "Multiple liquid drippings used as a tactile overlay or transition reference.",
    "GooEclipse": "A liquid eclipse and reveal experiment.",
    "GooLine": "A fluid line that merges and separates.",
    "GooWoom": "A soft organic goo expansion experiment.",
}


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def slug(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value)
    value = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value).strip("-").lower()
    return value or "untitled"


def split_name(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return value.replace("-", "_").replace("_", " ").strip()


def unique(values: Iterable[str]) -> list[str]:
    return sorted({str(value).strip().lower() for value in values if str(value).strip()})


def has_term(blob: str, term: str) -> bool:
    if re.fullmatch(r"[a-z0-9 ]+", term):
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", blob))
    return term in blob


def infer_semantics(*parts: Any) -> tuple[list[str], list[str], list[str], str]:
    blob = " ".join(str(part) for part in parts if part is not None).lower()
    roles = [role for role, needles in SEMANTIC_RULES.items() if any(has_term(blob, needle) for needle in needles)]
    if not roles:
        roles = ["explain"]
    experience = [role for role in roles if role in EXPERIENCE_ROLES]
    if set(roles).issubset(EXPERIENCE_ROLES):
        layers = ["ambient", "support"]
    elif "transition" in roles:
        layers = ["support"]
    else:
        layers = ["primary", "support"]
    high = ("high", "impact", "glitch", "explosion", "flash", "shake", "高能", "强冲击", "爆")
    low = ("low", "gentle", "soft", "slow", "minimal", "低", "安静", "克制", "舒缓")
    if any(has_term(blob, token) for token in high):
        energy = "high"
    elif any(has_term(blob, token) for token in low):
        energy = "low"
    else:
        energy = "medium"
    return unique(roles), unique(experience), unique(layers), energy


def layers_for(category: str, roles: Iterable[str]) -> list[str]:
    normalized = re.sub(r"[^a-z0-9]", "", category.lower())
    for key, hinted in CATEGORY_LAYER_HINTS.items():
        if key in normalized:
            return unique(hinted)
    role_set = set(roles)
    if "transition" in role_set:
        return ["support"]
    return ["primary", "support"]


def base_entry(
    *, source: str, kind: str, name: str, title: str, category: str, description: str,
    use: str, source_path: str, manifest: dict[str, Any], extra_tags: Iterable[str] = (),
) -> dict[str, Any]:
    semantic_roles, experience_roles, layer_fit, energy = infer_semantics(
        name, title, category, description, use, " ".join(extra_tags)
    )
    source_meta = manifest["sources"][source]
    tags = unique([source, kind, category, *extra_tags, *split_name(name).split()])
    return {
        "id": f"{source}:{slug(name)}",
        "source": source,
        "kind": kind,
        "name": name,
        "title": title,
        "category": category,
        "description": description.strip(),
        "use": use.strip(),
        "source_path": source_path,
        "tags": tags,
        "semantic_roles": semantic_roles,
        "experience_roles": experience_roles,
        "layer_fit": layers_for(category, semantic_roles),
        "energy": energy,
        "runtime_status": source_meta["runtime_status"],
        "compatibility": source_meta["compatibility"],
        "license": source_meta["license"],
    }


def match_style_demos(style_key: str, demo_paths: list[str]) -> tuple[list[str], str]:
    if len(demo_paths) <= 1:
        return demo_paths, "single" if demo_paths else "missing"
    style_slug = slug(style_key)
    exactish = [
        path for path in demo_paths
        if style_slug == slug(Path(path).stem)
        or style_slug in slug(Path(path).stem)
        or slug(Path(path).stem) in style_slug
    ]
    if exactish:
        return exactish, "name_match"
    style_tokens = {token for token in style_slug.split("-") if len(token) > 2}
    scored: list[tuple[int, str]] = []
    for path in demo_paths:
        demo_tokens = {token for token in slug(Path(path).stem).split("-") if len(token) > 2}
        scored.append((len(style_tokens & demo_tokens), path))
    best_score = max(score for score, _ in scored)
    if best_score > 0:
        return [path for score, path in scored if score == best_score], "token_match"
    return demo_paths, "unresolved_read_card"


def build_shotcraft(library_root: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    root = library_root / "sources" / "video-shotcraft"
    data = json.loads((root / "gallery" / "api" / "library.json").read_text(encoding="utf-8-sig"))
    entries: list[dict[str, Any]] = []
    preview_count = 0
    for card in data["cards"]:
        card_path = root / Path(card["source"])
        demo_dir = root / "demos" / card["category"] / card["name"]
        card_demo_paths = [rel(path, library_root) for path in sorted(demo_dir.rglob("*.tsx"))] if demo_dir.exists() else []
        for style in card.get("styles", []):
            style_key = style["key"]
            media_url = style.get("media", {}).get("url", "")
            media_name = Path(media_url.split("?", 1)[0]).name if media_url else ""
            preview = root / "gallery" / "media" / media_name if media_name else None
            if preview and preview.exists():
                preview_count += 1
            entry = base_entry(
                source="video-shotcraft",
                kind="shot_style",
                name=f"{card['name']}:{style_key}",
                title=style.get("label") or style_key,
                category=card["category"],
                description=style.get("description") or card.get("summary", ""),
                use=style.get("use") or card.get("use", ""),
                source_path=rel(card_path, library_root),
                manifest=manifest,
                extra_tags=[*card.get("tags", []), card["name"], style_key],
            )
            entry["id"] = f"video-shotcraft:{slug(card['name'])}:{slug(style_key)}"
            entry["card_name"] = card["name"]
            entry["style_key"] = style_key
            entry["duration"] = card.get("duration", "")
            entry["energy_label"] = card.get("energy", "")
            entry["intention"] = card.get("intention", "")
            matched_demos, demo_match_status = match_style_demos(style_key, card_demo_paths)
            entry["demo_paths"] = matched_demos
            entry["card_demo_paths"] = card_demo_paths
            entry["demo_match_status"] = demo_match_status
            entry["preview_path"] = rel(preview, library_root) if preview and preview.exists() else None
            entry["preview_status"] = "offline" if preview and preview.exists() else "missing"
            entry["gallery_source_path"] = f"sources/video-shotcraft/gallery/source/{card['name']}.md"
            roles, experience, layers, energy = infer_semantics(
                card.get("summary", ""), card.get("use", ""), card.get("intention", ""),
                style.get("description", ""), style.get("use", ""), card.get("energy", ""), card["category"],
            )
            entry["semantic_roles"] = roles
            entry["experience_roles"] = experience
            entry["layer_fit"] = layers_for(card["category"], roles)
            entry["energy"] = energy
            entries.append(entry)
    return entries, {"recipe_cards": len(data["cards"]), "styles": len(entries), "offline_previews": preview_count}


def parse_rve_readme(readme: str) -> list[tuple[str, str, str, str]]:
    current_category = "uncategorized"
    rows: list[tuple[str, str, str, str]] = []
    for line in readme.splitlines():
        heading = re.match(r"^###\s+(.+?)\s+\(\d+\)\s*$", line)
        if heading:
            current_category = heading.group(1).strip()
            continue
        match = re.match(r"^\|\s*([^|]+?)\s*\|\s*`([^`]+\.tsx)`\s*\|\s*([^|]+?)\s*\|$", line)
        if match and match.group(1).strip().lower() != "template":
            rows.append((current_category, match.group(1).strip(), match.group(2), match.group(3).strip()))
    return rows


def build_rve(library_root: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    root = library_root / "sources" / "rve"
    rows = parse_rve_readme((root / "README.md").read_text(encoding="utf-8-sig"))
    entries: list[dict[str, Any]] = []
    for category, title, filename, description in rows:
        path = root / "templates" / filename
        if not path.exists():
            raise FileNotFoundError(f"RVE README points to missing template: {path}")
        entry = base_entry(
            source="rve", kind="template", name=path.stem, title=title, category=category,
            description=description, use=f"Use as a focused {category.lower()} motion primitive.",
            source_path=rel(path, library_root), manifest=manifest,
        )
        entry["preview_url"] = "https://www.reactvideoeditor.com/remotion-templates"
        entries.append(entry)
    return entries, {"templates": len(entries)}


def build_scenes(library_root: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    root = library_root / "sources" / "scenes"
    scene_root = root / "src" / "scenes"
    entries: list[dict[str, Any]] = []
    for category_dir in sorted(path for path in scene_root.iterdir() if path.is_dir()):
        description = SCENES_DESCRIPTIONS.get(category_dir.name, "Remotion scene source.")
        for path in sorted(category_dir.glob("*.tsx")):
            if path.name.lower() == "index.tsx":
                continue
            title = split_name(path.stem)
            entry = base_entry(
                source="scenes", kind="scene", name=path.stem, title=title, category=category_dir.name,
                description=description, use=f"Adapt the {title} scene when the script calls for {description.lower()}",
                source_path=rel(path, library_root), manifest=manifest,
            )
            entry["shared_paths"] = [
                "sources/scenes/src/common",
                f"sources/scenes/src/scenes/{category_dir.name}/index.tsx",
            ]
            entry["preview_url"] = "https://lifeprompt-team.github.io/remotion-scenes/"
            entries.append(entry)
    return entries, {"scenes": len(entries)}


def build_curvable(library_root: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    root = library_root / "sources" / "curvable"
    entries: list[dict[str, Any]] = []
    for path in sorted((root / "src" / "components").glob("*.tsx")):
        stem = path.stem
        if stem not in CURVABLE_COMPONENTS:
            raise ValueError(f"Uncataloged Curvable component: {stem}")
        title, category, description = CURVABLE_COMPONENTS[stem]
        entry = base_entry(
            source="curvable", kind="component", name=stem, title=title, category=category,
            description=description, use="Use when its deterministic motion contract fits the script beat; replace the palette with Soft Signal tokens.",
            source_path=rel(path, library_root), manifest=manifest,
        )
        preview = root / "previews" / f"{stem}.gif"
        entry["preview_path"] = rel(preview, library_root) if preview.exists() else None
        dependencies: list[str] = []
        if stem in {"grainient-bg", "floating-stack", "prompt-input", "stats-grid"}:
            dependencies.append("ogl")
        if stem == "prompt-input":
            dependencies.extend(["@remotion/google-fonts", "canvaskit-wasm runtime assets"])
        entry["optional_dependencies"] = dependencies
        entries.append(entry)
    return entries, {"components": len(entries)}


def build_playground(library_root: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    root = library_root / "sources" / "playground"
    entries: list[dict[str, Any]] = []
    for name, description in PLAYGROUND_EFFECTS.items():
        path = root / "src" / f"{name}.jsx"
        if not path.exists():
            raise FileNotFoundError(path)
        entry = base_entry(
            source="playground", kind="effect_lab", name=name, title=split_name(name), category="goo",
            description=description,
            use="Use as a tactile visual-experience reference in a support or ambient layer after porting it to the current Remotion API.",
            source_path=rel(path, library_root), manifest=manifest, extra_tags=["goo", "liquid", "organic"],
        )
        entry["migration_required"] = True
        entries.append(entry)
    return entries, {"effects": len(entries)}


def validate_inventory(manifest: dict[str, Any], inventory: dict[str, dict[str, int]]) -> None:
    errors: list[str] = []
    for source, actual in inventory.items():
        expected = manifest["sources"][source].get("inventory_expectation", {})
        for key, value in expected.items():
            if actual.get(key) != value:
                errors.append(f"{source}.{key}: expected {value}, got {actual.get(key)}")
    if errors:
        raise ValueError("Inventory validation failed:\n" + "\n".join(errors))


def validate_entries(entries: list[dict[str, Any]], library_root: Path) -> None:
    ids = [entry["id"] for entry in entries]
    duplicates = sorted({entry_id for entry_id in ids if ids.count(entry_id) > 1})
    errors = [f"duplicate catalog id: {entry_id}" for entry_id in duplicates]
    for entry in entries:
        source_path = library_root / Path(entry["source_path"])
        if not source_path.exists():
            errors.append(f"{entry['id']}: missing source_path {entry['source_path']}")
        preview_path = entry.get("preview_path")
        if preview_path and not (library_root / Path(preview_path)).exists():
            errors.append(f"{entry['id']}: missing preview_path {preview_path}")
        for demo_path in entry.get("demo_paths", []):
            if not (library_root / Path(demo_path)).exists():
                errors.append(f"{entry['id']}: missing demo_path {demo_path}")
    if errors:
        raise ValueError("Catalog entry validation failed:\n" + "\n".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the unified Remotion motion catalog.")
    parser.add_argument("--library-root", type=Path, default=DEFAULT_LIBRARY_ROOT)
    parser.add_argument("--output", type=Path, help="Defaults to <library-root>/catalog.json")
    args = parser.parse_args()

    library_root = args.library_root.expanduser().resolve()
    manifest_path = library_root / "source-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))

    all_entries: list[dict[str, Any]] = []
    inventory: dict[str, dict[str, int]] = {}
    builders = {
        "video-shotcraft": build_shotcraft,
        "rve": build_rve,
        "scenes": build_scenes,
        "curvable": build_curvable,
        "playground": build_playground,
    }
    for source, builder in builders.items():
        entries, counts = builder(library_root, manifest)
        all_entries.extend(entries)
        inventory[source] = counts

    validate_inventory(manifest, inventory)
    all_entries.sort(key=lambda entry: entry["id"])
    validate_entries(all_entries, library_root)
    canonical = json.dumps(all_entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    revision = hashlib.sha256(canonical).hexdigest()[:16]
    catalog = {
        "schema_version": 1,
        "catalog_revision": revision,
        "path_base_from_skill_root": "assets/remotion-library",
        "snapshot_date": manifest["snapshot_date"],
        "entry_count": len(all_entries),
        "inventory": inventory,
        "sources": manifest["sources"],
        "entries": all_entries,
    }
    output = (args.output or (library_root / "catalog.json")).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"catalog": str(output), "revision": revision, "entries": len(all_entries), "inventory": inventory}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
