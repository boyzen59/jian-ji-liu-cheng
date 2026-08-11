#!/usr/bin/env python3
"""Validate workflow gates without modifying the project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


STATUS_ORDER = {
    "INTAKE": 0,
    "POSITIONED": 1,
    "TEXT_REVIEW": 2,
    "PRODUCTION_RELEASED": 3,
    "IMPLEMENTING": 4,
    "QA": 5,
    "DELIVERED": 6,
}
BLOCKING_TEXT = {"必须修改", "待确认"}
EXPECTED_THEME = {
    "name": "Soft Signal",
    "label_zh": "亲密 · 温暖",
    "accent": "#E8734A",
    "design_language": "Apple-inspired warmth",
    "material": "frosted-glass",
}
PROGRAMMATIC_CARRIERS = {"remotion", "hyperframes", "lottie", "d3", "blender", "manim"}
LEGACY_PROGRAMMATIC_CARRIERS = PROGRAMMATIC_CARRIERS | {"ppt_image"}
PRESENTER_CARRIERS = {
    "presenter", "presenter_full", "presenter_pip", "presenter_pip_lower_right",
    "presenter_pip_lower_right_circle", "presenter_opening_full", "presenter_closing_full",
    "presenter_pip_content_aware_circle_raised", "presenter_pip_lower_left_circle",
}
ALLOWED_MATERIALS = {"glass_thin", "glass_regular", "glass_thick", "none"}
ALLOWED_BACKGROUND_VISIBILITY = {"faint", "subtle", "evidence", "none"}
ALLOWED_ANIMATION_INTENTS = {
    "explain", "focus", "compare", "relate", "quantify", "demonstrate",
    "transition", "identity", "rhythm", "atmosphere", "delight",
}
ALLOWED_MOTION_ROLES = {"primary", "support", "ambient", "mixed"}
ALLOWED_SCENE_TYPES = {
    "chapter_title", "chart", "screenshot", "data", "key_text", "image_explainer", "archive", "map",
    "relationship", "environment", "presenter", "argument_bridge",
}
ALLOWED_SCENE_FUNCTIONS = {
    "introduce_chapter", "explain_causality", "provide_evidence", "provide_atmosphere",
    "emphasize_turn", "presenter_connection", "explain_image", "summarize", "bridge_argument",
}
EXPECTED_OUTPUT = {
    "width": 2560,
    "height": 1440,
    "fps": 60,
    "frame_rate_mode": "CFR",
    "container": "mp4",
    "video_codec": "h264",
    "video_profile": "high",
    "pixel_format": "yuv420p",
    "color_primaries": "bt709",
    "color_transfer": "bt709",
    "color_matrix": "bt709",
    "audio_mode": "no_audio_stream",
    "burned_in_captions": False,
}
ALLOWED_PROGRAMMATIC_OPPORTUNITIES = {"preferred", "support", "not_suitable"}
MEDIA_KINDS = {"image", "video"}
OPENING_CHAPTERS = {"", "开场", "片头", "opening", "intro"}
ALLOWED_ENGINES = {"remotion", "hyperframes", "lottie", "d3", "blender", "manim"}
ALLOWED_VARIATION_MODES = {"changed", "slower", "not_applicable"}
ALLOWED_DURATION_FILL_STRATEGIES = {
    "not_needed", "extend_internal_choreography", "new_semantic_page",
}
MOTION_SIGNATURE_FIELDS = {"layout", "direction", "build_order", "easing", "pace_class"}
APPLE_LOGIC_FIELDS = {
    "purpose", "focal_hierarchy", "spatial_origin", "material_response",
    "continuity", "settle_state", "delight",
}
IMAGE_MOTIONS = {
    "slow_push", "pan", "focus_relay", "parallax_2_5d", "evidence_zoom", "before_after",
}
IMAGE_MOTIONS_V7 = {
    "slow_push", "pan", "vertical_pan", "focus_relay", "parallax_2_5d",
    "mask_reveal", "evidence_push", "before_after", "spatial_handoff",
}
ENGINE_SELECTION_FIELDS = {
    "semantic_accuracy", "subject_safety", "render_stability", "visual_impact",
    "near_tie", "selected_engine", "reason",
}


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        errors.append(f"missing: {path}")
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid JSON {path}: {exc}")
    return {}


def parse_tc(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    parts = str(value).replace(",", ".").split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        return float(parts[0])
    except (ValueError, IndexError):
        raise ValueError(f"invalid timecode: {value}")


def parse_aspect_ratio(value) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().lower().replace("：", ":")
    if ":" in text:
        left, right = text.split(":", 1)
        try:
            denominator = float(right)
            return float(left) / denominator if denominator else None
        except ValueError:
            return None
    try:
        return float(text)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a jian-ji-liu-cheng project.")
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()

    root = args.project_root.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    project = load_json(root / "project.json", errors)
    status = str(project.get("status", "INTAKE"))
    if status not in STATUS_ORDER:
        errors.append(f"unsupported project status: {status}")
        level = 0
    else:
        level = STATUS_ORDER[status]

    catalog_path = Path(__file__).resolve().parents[1] / "assets" / "remotion-library" / "catalog.json"
    catalog = load_json(catalog_path, errors)
    catalog_revision = str(catalog.get("catalog_revision", ""))
    catalog_by_id = {str(entry.get("id")): entry for entry in catalog.get("entries", []) if entry.get("id")}
    catalog_ids = set(catalog_by_id)
    if not catalog_revision or not catalog_ids:
        errors.append("bundled Remotion catalog has no revision or entries")
    project_library = project.get("remotion_library", {})
    try:
        schema_version = int(project.get("schema_version", 1) or 1)
    except (TypeError, ValueError):
        schema_version = 1
        errors.append("project.schema_version must be an integer")
    if schema_version >= 2:
        if project_library.get("catalog_revision") != catalog_revision:
            errors.append("project.remotion_library.catalog_revision must match the bundled catalog")
    if schema_version >= 3:
        output_spec = project.get("spec", {})
        for key, value in EXPECTED_OUTPUT.items():
            if output_spec.get(key) != value:
                errors.append(f"project.spec.{key} must be {value!r}")
        if str(output_spec.get("video_codec", "")).lower() in {"h265", "hevc"}:
            errors.append("H.265/HEVC is not allowed by the fixed master spec")
    if schema_version >= 4:
        render_policy = project.get("render_policy", {})
        expected_render = {
            "prefer_gpu": True,
            "hardware_acceleration": "if-possible",
            "cpu_fallback": True,
            "max_segment_seconds": 300,
            "progress_report_interval_seconds": 300,
        }
        for key, value in expected_render.items():
            if render_policy.get(key) != value:
                errors.append(f"project.render_policy.{key} must be {value!r}")
        music_policy = project.get("music_policy", {})
        if music_policy.get("voice_priority") != "highest":
            errors.append("project.music_policy.voice_priority must be 'highest'")
        sources = set(map(str, music_policy.get("preferred_sources", [])))
        if not {"ai_original_light_music", "youtube_studio_audio_library"}.issubset(sources):
            errors.append("project.music_policy must include AI light music and YouTube Studio Audio Library")
        if music_policy.get("ordinary_youtube_channels_allowed") is not False:
            errors.append("ordinary YouTube channels must not be treated as licensed free-music sources")
    if schema_version >= 5:
        render_policy = project.get("render_policy", {})
        expected_monitoring = {
            "progress_heartbeat_required_without_progress": True,
            "resource_sample_interval_seconds": 15,
            "low_utilization_window_seconds": 90,
            "stall_diagnostic_seconds": 180,
            "hard_stall_seconds": 300,
            "automatic_stall_diagnostic": True,
            "adaptive_concurrency": True,
            "parallel_encoding": True,
            "target_cpu_percent": [75, 95],
            "target_gpu_percent_when_eligible": [65, 95],
            "target_ram_percent": [55, 78],
            "ram_hard_cap_percent": 85,
            "vram_hard_cap_percent": 92,
        }
        for key, value in expected_monitoring.items():
            if render_policy.get(key) != value:
                errors.append(f"project.render_policy.{key} must be {value!r}")
    if schema_version >= 8:
        if schema_version != 8:
            warnings.append(f"validator was authored for schema_version 8; got {schema_version}")

    theme = project.get("fixed_theme", {})
    for key, value in EXPECTED_THEME.items():
        if theme.get(key) != value:
            errors.append(f"fixed_theme.{key} must be {value!r}")
    theme_file = root / "06_remotion" / "src" / "theme-soft-signal.ts"
    if not theme_file.exists():
        errors.append(f"missing theme file: {theme_file}")
    else:
        theme_text = theme_file.read_text(encoding="utf-8")
        for token in [
            "#FFF8F0", "#3D3028", "#E8734A", "Soft Signal",
            "Apple-inspired warmth", "frosted-glass", "materials", "glassRegular",
            "backgroundPatternOpacity", "contrastBody", "springStandard",
            "chapterDisplayMin", "chapterDisplayMax", "presenterPip", "diameter: 360",
            "subtitleSafe", "bottomExclusion: 220", "minimum: {body: 42",
        ]:
            if token not in theme_text:
                errors.append(f"theme file missing token {token}")

    brief = root / "01_brief" / "project-brief.md"
    if level >= STATUS_ORDER["POSITIONED"] and (not brief.exists() or "[READY" in brief.read_text(encoding="utf-8")):
        errors.append("POSITIONED status requires a completed project brief")

    review_path = root / "03_review" / "text-review.json"
    review: dict = {}
    if level >= STATUS_ORDER["TEXT_REVIEW"]:
        review = load_json(review_path, errors)
        rows = review.get("rows", [])
        if schema_version >= 7:
            if review.get("review_mode") != "delta_only":
                errors.append("text-review review_mode must be delta_only")
            if review.get("baseline_existing_text_approved") is not True:
                errors.append("text-review baseline_existing_text_approved must be true")
            delta_rows = [row for row in rows if row.get("change_kind") in {"new", "changed"}]
            invalid_change_rows = [
                row.get("id", "?") for row in rows
                if row.get("change_kind") not in {"unchanged_approved", "layout_only", "new", "changed"}
            ]
            if invalid_change_rows:
                errors.append("text-review rows have invalid change_kind: " + ", ".join(map(str, invalid_change_rows)))
        else:
            delta_rows = rows
            if not rows:
                errors.append("TEXT_REVIEW status requires at least one review row")
        blockers = [
            row.get("id", "?") for row in delta_rows
            if row.get("status", "待确认") in BLOCKING_TEXT
        ]
        if schema_version >= 3:
            unapproved = [
                row.get("id", "?") for row in delta_rows
                if not row.get("approval_version") or not row.get("approval_source")
            ]
            if level >= STATUS_ORDER["PRODUCTION_RELEASED"] and unapproved:
                errors.append("text-review rows lack user approval evidence: " + ", ".join(map(str, unapproved)))
        if level >= STATUS_ORDER["PRODUCTION_RELEASED"] and blockers:
            errors.append("text-review blockers remain: " + ", ".join(map(str, blockers)))
        docx = root / "03_review" / "动效文字执行手册.docx"
        legacy_docx = root / "03_review" / "时间码与屏显文字审阅表.docx"
        if delta_rows and not docx.exists() and not legacy_docx.exists():
            errors.append(f"missing text-review Word gate: {docx}")
        if level >= STATUS_ORDER["PRODUCTION_RELEASED"] and delta_rows and not project.get("text_review_release"):
            errors.append("PRODUCTION_RELEASED requires project.text_review_release")
    elif review_path.exists():
        warnings.append("text-review template exists but project has not reached TEXT_REVIEW")

    spec_path = root / "04_spec" / "video-spec.json"
    spec: dict = {}
    if level >= STATUS_ORDER["PRODUCTION_RELEASED"]:
        outline = load_json(root / "04_spec" / "outline-scene-types.json", errors)
        outline_rows = outline.get("segments", [])
        seen_outline: set[str] = set()
        if not isinstance(outline_rows, list) or not outline_rows:
            errors.append("PRODUCTION_RELEASED requires a non-empty outline-scene-types.json")
        else:
            for row in outline_rows:
                row_id = str(row.get("id", ""))
                if not row_id:
                    errors.append("outline segment requires id")
                elif row_id in seen_outline:
                    errors.append(f"outline duplicate id: {row_id}")
                seen_outline.add(row_id)
                if row.get("scene_type") not in ALLOWED_SCENE_TYPES:
                    errors.append(f"outline {row_id or '?'}: unsupported scene_type {row.get('scene_type')!r}")
                if row.get("function") not in ALLOWED_SCENE_FUNCTIONS:
                    errors.append(f"outline {row_id or '?'}: unsupported function {row.get('function')!r}")
                for field in ["source_range", "viewer_should_notice", "viewer_should_understand"]:
                    if not row.get(field):
                        errors.append(f"outline {row_id or '?'}: {field} is required")
        spec = load_json(spec_path, errors)
        scenes = spec.get("scenes", [])
        if not scenes:
            errors.append("PRODUCTION_RELEASED requires at least one scene")
        visual = spec.get("visual_system", {})
        expected_visual = {
            "theme": "Soft Signal",
            "design_language": "Apple-inspired warmth",
            "default_material": "glass_regular",
            "default_background_visibility": "faint",
        }
        for key, value in expected_visual.items():
            if visual.get(key) != value:
                errors.append(f"video-spec visual_system.{key} must be {value!r}")
        try:
            contrast_target = float(visual.get("contrast_ratio_target", 0))
        except (TypeError, ValueError):
            contrast_target = 0
        if contrast_target < 4.5:
            errors.append("video-spec visual_system.contrast_ratio_target must be at least 4.5")
        if schema_version >= 3:
            spec_output = spec.get("output", {})
            for key, value in EXPECTED_OUTPUT.items():
                if spec_output.get(key) != value:
                    errors.append(f"video-spec output.{key} must be {value!r}")
            presenter_policy = spec.get("presenter_policy", {})
            if presenter_policy.get("max_ratio_exclusive") != 0.20:
                errors.append("video-spec presenter_policy.max_ratio_exclusive must be 0.20")
            expected_presenter_default = (
                "presenter_pip_content_aware_circle_raised"
                if schema_version >= 6 else
                ("presenter_pip_lower_right_circle" if schema_version >= 4 else "presenter_pip_lower_right")
            )
            if presenter_policy.get("after_opening_default") != expected_presenter_default:
                errors.append(
                    "video-spec presenter_policy.after_opening_default must be "
                    + expected_presenter_default
                )
        if schema_version >= 4:
            presenter_policy = spec.get("presenter_policy", {})
            if presenter_policy.get("pip_shape") != "circle":
                errors.append("video-spec presenter_policy.pip_shape must be 'circle'")
            if presenter_policy.get("pip_diameter_px") != 360:
                errors.append("video-spec presenter_policy.pip_diameter_px must be 360")
            if presenter_policy.get("pip_diameter_range_px") != [340, 380]:
                errors.append("video-spec presenter_policy.pip_diameter_range_px must be [340, 380]")
            chapter_policy = spec.get("chapter_policy", {})
            chapter_expected = {
                "required": True,
                "scene_type": "chapter_title",
                "fullscreen": True,
                "bilingual": True,
                "title_font_px_range": [156, 220] if schema_version >= 6 else [132, 180],
                "overview_item_count_range": [2, 4],
                "sound_emphasis": True,
                "chapter_hard_cut_allowed": False,
            }
            for key, value in chapter_expected.items():
                if chapter_policy.get(key) != value:
                    errors.append(f"video-spec chapter_policy.{key} must be {value!r}")
            if set(map(str, chapter_policy.get("carrier", []))) != {"remotion", "hyperframes"}:
                errors.append("video-spec chapter_policy.carrier must contain remotion and hyperframes")
            caption_policy = spec.get("caption_policy", {})
            if caption_policy.get("burned_in") is not False:
                errors.append("video-spec caption_policy.burned_in must be false")
            if caption_policy.get("delivery") != "sidecar_srt_ass":
                errors.append("video-spec caption_policy.delivery must be sidecar_srt_ass")
            motion_policy = spec.get("motion_policy", {})
            for key in [
                "prefer_remotion_hyperframes", "assess_every_scene",
                "chapter_transition_required", "hard_cut_requires_reason",
            ]:
                if motion_policy.get(key) is not True:
                    errors.append(f"video-spec motion_policy.{key} must be true")
            media_policy = spec.get("media_policy", {})
            media_expected = {
                "image_duration_seconds": [5, 10],
                "adjacent_same_master_forbidden": True,
                "video_loop_to_fill_forbidden": True,
                "non_16_9_treatment": (
                    "image_fullscreen_contain_solid_matte" if schema_version >= 7 else
                    ("image_fullscreen_contain_ambient_extension" if schema_version >= 6 else "contain_left_bilingual_right")
                ),
                "provenance_labels_on_canvas": False,
            }
            for key, value in media_expected.items():
                if media_policy.get(key) != value:
                    errors.append(f"video-spec media_policy.{key} must be {value!r}")
        if schema_version >= 6:
            presenter_policy = spec.get("presenter_policy", {})
            presenter_expected = {
                "opening_fullscreen_allowed": True,
                "opening_fullscreen_max_seconds": 15.0,
                "opening_side_overlay_count_range": [2, 4],
                "intermediate_fullscreen_forbidden": True,
                "closing_fullscreen_summary_required": True,
                "closing_side_overlay_count_range": [2, 4],
                "pip_bottom_clearance_px": 220,
            }
            if schema_version >= 8:
                presenter_expected.update({
                    "opening_programmatic_overlays_required": True,
                    "closing_programmatic_overlays_required": True,
                    "closing_fullscreen_must_reach_final_frame": True,
                    "pip_default_anchor": "lower-right-raised",
                    "pip_alternate_requires_user_approval": True,
                })
            else:
                presenter_expected.update({
                    "opening_hyperframes_side_overlays_required": True,
                    "closing_hyperframes_side_overlays_required": True,
                    "pip_anchor_options": ["lower-right-raised", "lower-left-raised"],
                })
            for key, value in presenter_expected.items():
                if presenter_policy.get(key) != value:
                    errors.append(f"video-spec presenter_policy.{key} must be {value!r}")
            caption_policy = spec.get("caption_policy", {})
            if caption_policy.get("bottom_exclusion_px") != 220:
                errors.append("video-spec caption_policy.bottom_exclusion_px must be 220")
            if caption_policy.get("overlays_must_stay_above_exclusion") is not True:
                errors.append("video-spec caption_policy.overlays_must_stay_above_exclusion must be true")
            motion_policy = spec.get("motion_policy", {})
            motion_expected = {
                "adjacent_identical_motion_signature_forbidden": True,
                "adjacent_same_visual_page_forbidden": True,
                "adjacent_same_content_fingerprint_forbidden": True,
                "repeat_page_to_fill_duration_forbidden": True,
                "internal_phases_min_when_extending": 3,
                "same_family_changed_dimensions_min": 2,
                "same_family_slow_variant_multiplier_range": [1.25, 1.60],
                "motion_families_per_chapter_short_min": 2,
                "motion_families_per_chapter_over_60s_min": 3,
            }
            for key, value in motion_expected.items():
                if motion_policy.get(key) != value:
                    errors.append(f"video-spec motion_policy.{key} must be {value!r}")
            media_policy = spec.get("media_policy", {})
            if schema_version >= 8:
                motion_expected_v7 = {
                    "engine_selection_peer_level": True,
                    "engine_selection_criteria": ["semantic_accuracy", "hierarchy_clarity", "subject_safety", "render_stability", "visual_impact"],
                    "near_tie_prefer": "hyperframes",
                    "engine_usage_quota_enforced": False,
                    "video_shotcraft_pass_required": True,
                    "motion_coverage_for_media_gaps_required": True,
                }
                for key, value in motion_expected_v7.items():
                    if motion_policy.get(key) != value:
                        errors.append(f"video-spec motion_policy.{key} must be {value!r}")
                media_expected_current = {
                    "asset_assignment_mode": "user_verified_manifest_locked",
                    "reassess_locked_asset_match": False,
                    "image_default_treatment": "image_fullscreen_clear_local_text_glass",
                    "evidence_material_classes": ["archive_evidence", "book_evidence"],
                    "historical_treatment": "historical_evidence_split_title_source_plus_large_image",
                    "evidence_bilingual": ["zh-CN", "en"],
                    "dynamic_reasoning_forbidden_over_evidence": True,
                    "media_body_blur_px": 0,
                    "media_text_overlay_engine": "selected_per_scene",
                    "video_duration_policy": "natural_full_if_at_least_5_else_hold_last_frame_to_5",
                    "video_max_duration_seconds": None,
                    "video_muted": True,
                }
            else:
                media_expected_current = {
                    "image_default_treatment": "image_fullscreen_glass_points",
                    "archive_treatment": "archive_split_image_left_source_file_right",
                    "split_layout_archive_only": True,
                }
            for key, value in media_expected_current.items():
                if media_policy.get(key) != value:
                    errors.append(f"video-spec media_policy.{key} must be {value!r}")
            if schema_version >= 7:
                bridge_expected = {
                    "engine": "hyperframes", "target_ratio": [0.04, 0.06], "hard_max_ratio": 0.06,
                    "max_per_chapter": 1, "adjacent_forbidden": True,
                    "right_item_count_range": [2, 4], "only_when_media_or_concrete_diagram_insufficient": True,
                }
                for key, value in bridge_expected.items():
                    if spec.get("argument_bridge_policy", {}).get(key) != value:
                        errors.append(f"video-spec argument_bridge_policy.{key} must be {value!r}")
            if visual.get("subtitle_exclusion_bottom_px") != 220:
                errors.append("video-spec visual_system.subtitle_exclusion_bottom_px must be 220")
            expected_fonts = {
                "chapter": [156, 220],
                "conclusion": [104, 148],
                "body": [42, 54],
                "support_min": 32,
                "source_meta_min": 26,
            }
            for key, value in expected_fonts.items():
                if visual.get("font_px", {}).get(key) != value:
                    errors.append(f"video-spec visual_system.font_px.{key} must be {value!r}")
        animation_path = root / "04_spec" / "animation-plan.json"
        animation_plan = load_json(animation_path, errors)
        if animation_plan.get("catalog_revision") != catalog_revision:
            errors.append("animation-plan catalog_revision must match the bundled catalog")
        if schema_version >= 6:
            engine_policy = animation_plan.get("engine_policy", {})
            expected_engine_policy = {
                "remotion_master_timeline": True,
                "adjacent_identical_signature_forbidden": True,
                "adjacent_same_visual_page_forbidden": True,
                "repeat_page_to_fill_duration_forbidden": True,
            }
            for key, value in expected_engine_policy.items():
                if engine_policy.get(key) != value:
                    errors.append(f"animation-plan engine_policy.{key} must be {value!r}")
            if schema_version >= 8:
                engine_expected_v7 = {
                    "engine_selection_peer_level": True,
                    "engine_selection_criteria": ["semantic_accuracy", "hierarchy_clarity", "subject_safety", "render_stability", "visual_impact"],
                    "near_tie_prefer": "hyperframes",
                    "engine_usage_quota_enforced": False,
                    "opening_and_closing_presenter_overlays": "selected_per_scene",
                    "video_shotcraft_pass_required": True,
                }
                for key, value in engine_expected_v7.items():
                    if engine_policy.get(key) != value:
                        errors.append(f"animation-plan engine_policy.{key} must be {value!r}")
        animation_rows = animation_plan.get("scenes", [])
        if not isinstance(animation_rows, list):
            errors.append("animation-plan scenes must be a list")
            animation_rows = []
        animation_by_scene: dict[str, dict] = {}
        for row in animation_rows:
            scene_id = str(row.get("scene_id", ""))
            if not scene_id:
                errors.append("animation-plan row requires scene_id")
                continue
            if scene_id in animation_by_scene:
                errors.append(f"animation-plan duplicate scene_id: {scene_id}")
            animation_by_scene[scene_id] = row
            for field in ["viewer_should_notice", "viewer_should_understand", "subject_safe_zones"]:
                if not row.get(field):
                    errors.append(f"animation-plan {scene_id}: {field} is required")
            try:
                if float(row.get("duration_seconds", 0)) <= 0:
                    errors.append(f"animation-plan {scene_id}: duration_seconds must be positive")
            except (TypeError, ValueError):
                errors.append(f"animation-plan {scene_id}: duration_seconds must be numeric")
            if row.get("reading_load") not in {"low", "medium", "high"}:
                errors.append(f"animation-plan {scene_id}: reading_load must be low, medium, or high")
            intents = row.get("animation_intent", [])
            if not isinstance(intents, list) or not intents:
                errors.append(f"animation-plan {scene_id}: animation_intent must be a non-empty list")
            else:
                unknown = sorted(set(map(str, intents)) - ALLOWED_ANIMATION_INTENTS)
                if unknown:
                    errors.append(f"animation-plan {scene_id}: unsupported animation intents {unknown}")
            if row.get("motion_role") not in ALLOWED_MOTION_ROLES:
                errors.append(f"animation-plan {scene_id}: unsupported motion_role {row.get('motion_role')!r}")
            if schema_version >= 6:
                engine = str(row.get("engine", "")).lower()
                if engine not in ALLOWED_ENGINES:
                    errors.append(f"animation-plan {scene_id}: engine must be one of {sorted(ALLOWED_ENGINES)}")
                if schema_version >= 7:
                    decision = row.get("engine_selection")
                    if not isinstance(decision, dict):
                        errors.append(f"animation-plan {scene_id}: engine_selection is required")
                    else:
                        missing_decision = sorted(field for field in ENGINE_SELECTION_FIELDS if field not in decision)
                        if missing_decision:
                            errors.append(f"animation-plan {scene_id}: engine_selection missing {missing_decision}")
                        score_fields = ["semantic_accuracy", "subject_safety", "render_stability", "visual_impact"]
                        if schema_version >= 8:
                            score_fields.insert(1, "hierarchy_clarity")
                        for score_field in score_fields:
                            try:
                                score = float(decision.get(score_field, -1))
                            except (TypeError, ValueError):
                                score = -1
                            if not 0 <= score <= 5:
                                errors.append(
                                    f"animation-plan {scene_id}: engine_selection.{score_field} must be 0..5"
                                )
                        if str(decision.get("selected_engine", "")).lower() != engine:
                            errors.append(
                                f"animation-plan {scene_id}: engine_selection.selected_engine must match engine"
                            )
                        if not isinstance(decision.get("near_tie"), bool):
                            errors.append(f"animation-plan {scene_id}: engine_selection.near_tie must be boolean")
                        elif decision.get("near_tie") and engine != "hyperframes":
                            errors.append(
                                f"animation-plan {scene_id}: near-tie Remotion/HyperFrames selection must prefer HyperFrames"
                            )
                    if schema_version >= 8:
                        shotcraft_pass = row.get("shotcraft_pass")
                        if not isinstance(shotcraft_pass, dict):
                            errors.append(f"animation-plan {scene_id}: shotcraft_pass is required")
                        else:
                            for field in ["semantic_segment_id", "source_range", "cognitive_action", "selected_engine", "selected_grammar"]:
                                if not shotcraft_pass.get(field):
                                    errors.append(f"animation-plan {scene_id}: shotcraft_pass.{field} is required")
                            candidates = shotcraft_pass.get("candidates")
                            if not isinstance(candidates, list) or len(candidates) < 2:
                                errors.append(f"animation-plan {scene_id}: shotcraft_pass requires at least two candidates")
                            elif not any(item.get("decision") == "selected" for item in candidates if isinstance(item, dict)):
                                errors.append(f"animation-plan {scene_id}: shotcraft_pass needs one selected candidate")
                        if not decision.get("reason"):
                            errors.append(f"animation-plan {scene_id}: engine_selection.reason is required")
                if not row.get("motion_family"):
                    errors.append(f"animation-plan {scene_id}: motion_family is required")
                for field in ["visual_page_id", "content_fingerprint"]:
                    if not row.get(field):
                        errors.append(f"animation-plan {scene_id}: {field} is required")
                fill_strategy = row.get("duration_fill_strategy")
                if fill_strategy not in ALLOWED_DURATION_FILL_STRATEGIES:
                    errors.append(
                        f"animation-plan {scene_id}: duration_fill_strategy must be not_needed, extend_internal_choreography, or new_semantic_page"
                    )
                if row.get("repeat_page_to_fill_duration") is not False:
                    errors.append(
                        f"animation-plan {scene_id}: repeat_page_to_fill_duration must be false"
                    )
                if fill_strategy == "extend_internal_choreography":
                    phases = row.get("internal_phases")
                    if not isinstance(phases, list) or len(phases) < 3:
                        errors.append(
                            f"animation-plan {scene_id}: extended HyperFrames duration requires at least three internal_phases"
                        )
                    if engine != "hyperframes":
                        errors.append(
                            f"animation-plan {scene_id}: extend_internal_choreography must use HyperFrames"
                        )
                signature = row.get("motion_signature")
                if not isinstance(signature, dict):
                    errors.append(f"animation-plan {scene_id}: motion_signature is required")
                else:
                    missing_signature = sorted(MOTION_SIGNATURE_FIELDS - set(signature))
                    if missing_signature or any(not signature.get(field) for field in MOTION_SIGNATURE_FIELDS):
                        errors.append(
                            f"animation-plan {scene_id}: motion_signature missing values {missing_signature or sorted(MOTION_SIGNATURE_FIELDS)}"
                        )
                variation = row.get("variation_from_previous")
                if not isinstance(variation, dict) or variation.get("mode") not in ALLOWED_VARIATION_MODES:
                    errors.append(
                        f"animation-plan {scene_id}: variation_from_previous.mode must be changed, slower, or not_applicable"
                    )
                apple_logic = row.get("apple_logic")
                if not isinstance(apple_logic, dict):
                    errors.append(f"animation-plan {scene_id}: apple_logic is required")
                else:
                    missing_apple = sorted(
                        field for field in APPLE_LOGIC_FIELDS if not apple_logic.get(field)
                    )
                    if missing_apple:
                        errors.append(f"animation-plan {scene_id}: apple_logic missing {missing_apple}")
                try:
                    if float(row.get("subtitle_exclusion_bottom_px", 0)) < 220:
                        errors.append(
                            f"animation-plan {scene_id}: subtitle_exclusion_bottom_px must be at least 220"
                        )
                except (TypeError, ValueError):
                    errors.append(f"animation-plan {scene_id}: subtitle_exclusion_bottom_px must be numeric")
                if engine == "hyperframes" and not row.get("hyperframes_recipe"):
                    errors.append(f"animation-plan {scene_id}: HyperFrames scene requires hyperframes_recipe")
            if schema_version >= 4 and row.get("programmatic_opportunity") not in ALLOWED_PROGRAMMATIC_OPPORTUNITIES:
                errors.append(
                    f"animation-plan {scene_id}: programmatic_opportunity must be preferred, support, or not_suitable"
                )
            for candidate in row.get("candidates", []):
                if candidate not in catalog_ids:
                    errors.append(f"animation-plan {scene_id}: unknown candidate id {candidate!r}")
            primary = row.get("primary_selection")
            if not isinstance(primary, dict):
                errors.append(f"animation-plan {scene_id}: primary_selection is required")
            else:
                selected_id = primary.get("id")
                if selected_id == "custom":
                    for field in ["custom_reason", "motion_grammar"]:
                        if not primary.get(field):
                            errors.append(f"animation-plan {scene_id}: custom primary requires {field}")
                elif selected_id not in catalog_ids:
                    errors.append(f"animation-plan {scene_id}: unknown primary id {selected_id!r}")
                if not primary.get("why_now"):
                    errors.append(f"animation-plan {scene_id}: primary_selection.why_now is required")
                if not isinstance(primary.get("includes_ambient_motion"), bool):
                    errors.append(
                        f"animation-plan {scene_id}: primary_selection.includes_ambient_motion must be boolean"
                    )
            if not row.get("fallback"):
                errors.append(f"animation-plan {scene_id}: fallback is required")
            ambient = row.get("ambient_selection")
            if ambient is not None:
                if not isinstance(ambient, dict):
                    errors.append(f"animation-plan {scene_id}: ambient_selection must be an object or null")
                else:
                    ambient_id = ambient.get("id")
                    if ambient_id not in catalog_ids:
                        errors.append(f"animation-plan {scene_id}: unknown ambient id {ambient_id!r}")
                    elif "ambient" not in catalog_by_id[ambient_id].get("layer_fit", []):
                        errors.append(f"animation-plan {scene_id}: selected ambient id is not cataloged for ambient layer")
                    protection = ambient.get("subject_protection")
                    for field in ["visual_experience_gain", "why_keep"]:
                        if not ambient.get(field):
                            errors.append(f"animation-plan {scene_id}: ambient {field} is required")
                    if not isinstance(protection, dict):
                        errors.append(f"animation-plan {scene_id}: ambient subject_protection is required")
                    else:
                        if not protection.get("safe_zones"):
                            errors.append(f"animation-plan {scene_id}: ambient safe_zones are required")
                        try:
                            max_opacity = float(protection.get("max_opacity"))
                            if not 0 <= max_opacity <= 0.24:
                                errors.append(f"animation-plan {scene_id}: ambient max_opacity must be 0..0.24")
                        except (TypeError, ValueError):
                            errors.append(f"animation-plan {scene_id}: ambient max_opacity must be numeric")
                        for field in ["reading_behavior", "qa_frame"]:
                            if not protection.get(field):
                                errors.append(f"animation-plan {scene_id}: ambient {field} is required")
            if isinstance(primary, dict) and primary.get("includes_ambient_motion") and ambient is not None:
                errors.append(
                    f"animation-plan {scene_id}: ambient_selection must be null when primary already includes ambient motion"
                )

        previous_end = None
        presenter_seconds = 0.0
        attention_reset_times: list[float] = []
        seen_chapters: set[str] = set()
        previous_master_ids: set[str] = set()
        previous_media_kind = ""
        previous_manifest_order = 0
        previous_programmatic: dict | None = None
        programmatic_by_chapter: dict[str, int] = {}
        hyperframes_by_chapter: dict[str, int] = {}
        motion_families_by_chapter: dict[str, set[str]] = {}
        chapter_time_bounds: dict[str, list[float]] = {}
        remotion_visible_scenes = 0
        hyperframes_visible_scenes = 0
        hyperframes_non_title = False
        opening_full_presenter_scenes: list[str] = []
        closing_full_presenter_scenes: list[str] = []
        argument_bridge_seconds = 0.0
        argument_bridge_by_chapter: dict[str, int] = {}
        previous_was_argument_bridge = False
        review_ids = {str(row.get("id")) for row in review.get("rows", [])}
        for scene_index, scene in enumerate(scenes):
            sid = scene.get("id", "?")
            try:
                start, end = parse_tc(scene.get("start")), parse_tc(scene.get("end"))
            except (ValueError, TypeError) as exc:
                errors.append(f"scene {sid}: {exc}")
                continue
            if end <= start:
                errors.append(f"scene {sid}: end must be after start")
            scene_duration = end - start
            if previous_end is not None and abs(start - previous_end) > 0.101:
                errors.append(f"scene {sid}: timeline gap/overlap {start - previous_end:+.3f}s")
            previous_end = end
            scene_type = scene.get("scene_type")
            scene_function = scene.get("function")
            if scene_type not in ALLOWED_SCENE_TYPES:
                errors.append(f"scene {sid}: unsupported scene_type {scene_type!r}")
            if scene_function not in ALLOWED_SCENE_FUNCTIONS:
                errors.append(f"scene {sid}: unsupported function {scene_function!r}")
            outline_id = str(scene.get("outline_id", sid))
            if seen_outline and outline_id not in seen_outline:
                errors.append(f"scene {sid}: outline_id {outline_id!r} not found in outline")
            text_id = scene.get("text_id")
            if text_id:
                if schema_version >= 7:
                    change_kind = scene.get("text_change_kind")
                    if change_kind not in {"unchanged_approved", "layout_only", "new", "changed"}:
                        errors.append(f"scene {sid}: text_change_kind is required")
                    elif change_kind in {"new", "changed"} and str(text_id) not in review_ids:
                        errors.append(f"scene {sid}: new/changed text_id {text_id} not in delta review")
                elif str(text_id) not in review_ids:
                    errors.append(f"scene {sid}: text_id {text_id} not in released review")
            carrier = str(scene.get("carrier", "")).lower()
            programmatic_carriers = (
                PROGRAMMATIC_CARRIERS if schema_version >= 6 else LEGACY_PROGRAMMATIC_CARRIERS
            )
            if schema_version >= 6 and carrier == "ppt_image":
                errors.append(
                    f"scene {sid}: ppt_image carrier is forbidden; ordinary images must use the full-screen image explainer"
                )
            chapter_name = str(scene.get("chapter", "")).strip()
            chapter_key = chapter_name.casefold()
            bounds = chapter_time_bounds.setdefault(chapter_key, [start, end])
            bounds[0] = min(bounds[0], start)
            bounds[1] = max(bounds[1], end)
            if schema_version >= 4:
                opportunity = scene.get("programmatic_opportunity")
                if opportunity not in ALLOWED_PROGRAMMATIC_OPPORTUNITIES:
                    errors.append(
                        f"scene {sid}: programmatic_opportunity must be preferred, support, or not_suitable"
                    )
                if opportunity == "preferred" and carrier not in programmatic_carriers:
                    errors.append(f"scene {sid}: preferred programmatic opportunity must use a programmatic carrier")
                if opportunity == "not_suitable" and not scene.get("programmatic_declined_reason"):
                    errors.append(f"scene {sid}: not_suitable requires programmatic_declined_reason")

                if scene.get("burned_in_captions") is not False:
                    errors.append(f"scene {sid}: burned_in_captions must be false")
                if scene.get("provenance_label_on_canvas") is not False:
                    errors.append(f"scene {sid}: provenance_label_on_canvas must be false")

                if chapter_key not in OPENING_CHAPTERS and chapter_key not in seen_chapters:
                    seen_chapters.add(chapter_key)
                    if scene_type != "chapter_title":
                        errors.append(f"chapter {chapter_name!r}: first scene must be chapter_title")
                if scene_type == "chapter_title":
                    if scene_function != "introduce_chapter":
                        errors.append(f"scene {sid}: chapter_title function must be introduce_chapter")
                    if carrier not in {"remotion", "hyperframes"}:
                        errors.append(f"scene {sid}: chapter_title carrier must be remotion or hyperframes")
                    if scene.get("chapter_title_card") is not True or scene.get("fullscreen") is not True:
                        errors.append(f"scene {sid}: chapter_title_card and fullscreen must be true")
                    if not scene.get("screen_en") or not scene.get("screen_zh"):
                        errors.append(f"scene {sid}: chapter_title requires approved English and Chinese titles")
                    try:
                        title_px = float(scene.get("chapter_title_font_px", 0))
                    except (TypeError, ValueError):
                        title_px = 0
                    title_min, title_max = ((156, 220) if schema_version >= 6 else (132, 180))
                    if not title_min <= title_px <= title_max:
                        errors.append(
                            f"scene {sid}: chapter_title_font_px must be {title_min}..{title_max}"
                        )
                    overview = scene.get("chapter_overview_items", [])
                    if not isinstance(overview, list) or not 2 <= len(overview) <= 4:
                        errors.append(f"scene {sid}: chapter_overview_items must contain 2..4 bilingual items")
                    elif any(not isinstance(item, dict) or not item.get("en") or not item.get("zh") for item in overview):
                        errors.append(f"scene {sid}: every chapter overview item requires en and zh")
                    if scene.get("sound_emphasis") is not True:
                        errors.append(f"scene {sid}: chapter_title requires sound_emphasis=true")
                    if str(scene.get("transition_in", "")).lower() in {"hard_cut", "hard-cut"}:
                        errors.append(f"scene {sid}: chapter_title cannot enter with a hard cut")

                if schema_version >= 7:
                    mandatory_kind = scene.get("programmatic_mandatory_kind")
                    mandatory_values = {
                        "not_applicable", "chapter_open", "causal", "process",
                        "institutional_relation", "structural_relation", "textual_reasoning",
                    }
                    if mandatory_kind not in mandatory_values:
                        errors.append(f"scene {sid}: unsupported programmatic_mandatory_kind {mandatory_kind!r}")
                    must_programmatic = (
                        scene_type == "chapter_title"
                        or scene_type == "relationship"
                        or scene_function == "explain_causality"
                        or mandatory_kind != "not_applicable"
                    )
                    if must_programmatic:
                        if opportunity != "preferred" or carrier not in programmatic_carriers:
                            errors.append(
                                f"scene {sid}: chapter/causal/process/institution/relationship/text reasoning must use programmatic motion"
                            )

                transition_name = str(scene.get("transition_in", "")).lower()
                if transition_name in {"hard_cut", "hard-cut"} and not scene.get("hard_cut_reason"):
                    errors.append(f"scene {sid}: hard cut requires hard_cut_reason")

                media_kind = str(scene.get("media_kind", "")).lower()
                if media_kind not in {"image", "video", "none"}:
                    errors.append(f"scene {sid}: media_kind must be image, video, or none")
                if carrier in {"image", "broll", "archive", "video"} and media_kind not in MEDIA_KINDS:
                    errors.append(f"scene {sid}: carrier {carrier!r} requires media_kind image or video")
                master_ids = {str(value) for value in scene.get("master_media_ids", []) if str(value)}
                if media_kind in MEDIA_KINDS:
                    if not master_ids:
                        errors.append(f"scene {sid}: media scene requires master_media_ids")
                    if schema_version >= 7:
                        assignment = scene.get("asset_assignment")
                        if not isinstance(assignment, dict):
                            errors.append(f"scene {sid}: media scene requires locked asset_assignment")
                            assignment = {}
                        for field, expected in {
                            "user_verified": True,
                            "assignment_locked": True,
                            "assignment_reassessed": False,
                        }.items():
                            if assignment.get(field) is not expected:
                                errors.append(f"scene {sid}: asset_assignment.{field} must be {expected!r}")
                        assigned_path = str(assignment.get("assigned_asset_path", ""))
                        semantic_segment_id = str(scene.get("semantic_segment_id", ""))
                        if not assigned_path:
                            errors.append(f"scene {sid}: asset_assignment.assigned_asset_path is required")
                        if not semantic_segment_id:
                            errors.append(f"scene {sid}: semantic_segment_id is required")
                        if str(assignment.get("assigned_script_segment_id", "")) != semantic_segment_id:
                            errors.append(
                                f"scene {sid}: locked asset must remain assigned to the same semantic_segment_id"
                            )
                        try:
                            manifest_order = int(assignment.get("manifest_order", 0))
                        except (TypeError, ValueError):
                            manifest_order = 0
                        if manifest_order <= previous_manifest_order:
                            errors.append(f"scene {sid}: locked assets must follow increasing manifest_order")
                        previous_manifest_order = max(previous_manifest_order, manifest_order)
                        if scene.get("original_media_clear") is not True:
                            errors.append(f"scene {sid}: original_media_clear must be true")
                        try:
                            media_blur = float(scene.get("media_body_blur_px", -1))
                        except (TypeError, ValueError):
                            media_blur = -1
                        if media_blur != 0:
                            errors.append(f"scene {sid}: image/video body blur must be exactly 0")
                        if scene.get("fullscreen") is not True:
                            errors.append(f"scene {sid}: image/video must remain full screen")
                    else:
                        if scene.get("asset_semantic_match") != "MATCH":
                            errors.append(f"scene {sid}: asset_semantic_match must be MATCH")
                        if scene.get("asset_visual_review_status") != "APPROVED":
                            errors.append(f"scene {sid}: asset_visual_review_status must be APPROVED")
                    if master_ids & previous_master_ids:
                        errors.append(
                            f"scene {sid}: same master image/video cannot appear in adjacent scenes"
                        )
                    ratio = parse_aspect_ratio(scene.get("source_aspect_ratio"))
                    if ratio is None:
                        errors.append(f"scene {sid}: media scene requires source_aspect_ratio")
                    elif media_kind == "image":
                        if schema_version >= 7:
                            try:
                                timeline_duration = float(scene.get("timeline_duration_seconds", 0))
                            except (TypeError, ValueError):
                                timeline_duration = 0
                            if not 5 <= timeline_duration <= 10:
                                errors.append(f"scene {sid}: image timeline_duration_seconds must be 5..10")
                            if abs(timeline_duration - scene_duration) > 0.101:
                                errors.append(f"scene {sid}: image timeline duration must match Scene duration")
                            if scene.get("playback_mode") != "image_hold":
                                errors.append(f"scene {sid}: image playback_mode must be image_hold")
                            treatment = scene.get("frame_treatment")
                            material_class = scene.get("material_class")
                            is_evidence = (
                                material_class in {"archive_evidence", "book_evidence"}
                                if schema_version >= 8
                                else scene_type == "archive"
                            )
                            if is_evidence:
                                if scene_type != "archive":
                                    errors.append(f"scene {sid}: archive_evidence/book_evidence must use archive scene_type")
                                if treatment != "historical_evidence_split_title_source_plus_large_image":
                                    errors.append(
                                        f"scene {sid}: historical image must use title/source plus large clear evidence split"
                                    )
                                if scene.get("visual_mode") != "historical_evidence_split_title_source_plus_large_image":
                                    errors.append(f"scene {sid}: historical visual_mode is invalid")
                                metadata = scene.get("source_file_metadata")
                                if not isinstance(metadata, dict):
                                    errors.append(f"scene {sid}: historical image requires source_file_metadata")
                                else:
                                    missing_metadata = [
                                        key for key in ["file", "institution", "date_page", "excerpt"]
                                        if not metadata.get(key)
                                    ]
                                    if missing_metadata:
                                        errors.append(
                                            f"scene {sid}: source_file_metadata missing {missing_metadata}"
                                        )
                                if schema_version >= 8:
                                    if not scene.get("screen_en") or not scene.get("screen_zh"):
                                        errors.append(f"scene {sid}: evidence title/source explanation must be bilingual zh-CN + en")
                                    if scene.get("dynamic_reasoning_overlay") is not False:
                                        errors.append(f"scene {sid}: dynamic reasoning is forbidden over archive/book evidence")
                                media_has_text = bool(text_id or scene.get("screen_en") or scene.get("screen_zh"))
                                if media_has_text:
                                    if schema_version >= 8 and scene.get("text_overlay_engine") not in {"hyperframes", "remotion"}:
                                        errors.append(f"scene {sid}: evidence text_overlay_engine must be remotion or hyperframes")
                                    elif schema_version < 8 and scene.get("text_overlay_engine") != "hyperframes":
                                        errors.append(f"scene {sid}: historical title/source overlay must use HyperFrames")
                                    if scene.get("text_overlay_scope") != "local_text_glass_only":
                                        errors.append(f"scene {sid}: historical glass must be local to title/source text only")
                            else:
                                expected_treatment = (
                                    "image_fullscreen_bleed"
                                    if abs(ratio - 16 / 9) <= 0.02
                                    else "image_fullscreen_contain_solid_matte"
                                )
                                if treatment != expected_treatment:
                                    errors.append(
                                        f"scene {sid}: ordinary image must use {expected_treatment} with no blurred extension"
                                    )
                                if scene_type == "archive" or treatment == "historical_evidence_split_title_source_plus_large_image":
                                    errors.append(
                                        f"scene {sid}: historical split is reserved for archive_evidence/book_evidence"
                                    )
                                if scene.get("visual_mode") != "image_fullscreen_clear_local_text_glass":
                                    errors.append(
                                        f"scene {sid}: ordinary image visual_mode must preserve clear full-screen original"
                                    )
                                if scene.get("image_motion") not in IMAGE_MOTIONS_V7:
                                    errors.append(
                                        f"scene {sid}: ordinary image motion must use an approved semantic motion family"
                                    )
                                media_has_text = bool(text_id or scene.get("screen_en") or scene.get("screen_zh"))
                                if media_has_text:
                                    if scene.get("text_overlay_engine") != "hyperframes":
                                        errors.append(f"scene {sid}: image text overlay must use HyperFrames")
                                    if scene.get("text_overlay_scope") != "local_text_glass_only":
                                        errors.append(f"scene {sid}: image glass must be local to text only")
                        elif schema_version >= 6:
                            treatment = scene.get("frame_treatment")
                            if scene_type == "archive":
                                if treatment != "archive_split_image_left_source_file_right":
                                    errors.append(f"scene {sid}: archive image must use archive split")
                            else:
                                expected_treatment = "image_fullscreen_bleed" if abs(ratio - 16 / 9) <= 0.02 else "image_fullscreen_contain_ambient_extension"
                                if treatment != expected_treatment:
                                    errors.append(f"scene {sid}: ordinary image must use {expected_treatment}")
                        elif abs(ratio - 16 / 9) > 0.02:
                            if scene.get("frame_treatment") != "contain_left_bilingual_right":
                                errors.append(
                                    f"scene {sid}: non-16:9 image must use contain_left_bilingual_right"
                                )
                            if not scene.get("screen_en") or not scene.get("screen_zh"):
                                errors.append(
                                    f"scene {sid}: non-16:9 image requires English and Chinese right-side notes"
                                )
                    elif media_kind == "video":
                        if scene.get("video_looped") is not False:
                            errors.append(f"scene {sid}: video_looped must be false")
                        if schema_version >= 7:
                            if scene.get("video_muted") is not True:
                                errors.append(f"scene {sid}: video must be muted")
                            if scene.get("video_trimmed") is not False:
                                errors.append(f"scene {sid}: video_trimmed must be false")
                            if scene.get("frame_treatment") != "video_fullscreen_clear":
                                errors.append(f"scene {sid}: video must use video_fullscreen_clear")
                            if scene.get("visual_mode") != "video_fullscreen_clear_local_text_glass":
                                errors.append(f"scene {sid}: video visual_mode must preserve clear full-screen original")
                            try:
                                source_duration = float(scene.get("source_duration_seconds", 0))
                                timeline_duration = float(scene.get("timeline_duration_seconds", 0))
                                hold_seconds = float(scene.get("last_frame_hold_seconds", 0))
                            except (TypeError, ValueError):
                                source_duration, timeline_duration, hold_seconds = 0, 0, -1
                            if source_duration <= 0:
                                errors.append(f"scene {sid}: source_duration_seconds must be positive")
                            elif source_duration >= 5:
                                if abs(timeline_duration - source_duration) > 0.101:
                                    errors.append(f"scene {sid}: video >=5s must use its full natural duration")
                                if scene.get("playback_mode") != "natural_full_once":
                                    errors.append(f"scene {sid}: video >=5s playback_mode must be natural_full_once")
                                if abs(hold_seconds) > 0.101:
                                    errors.append(f"scene {sid}: video >=5s must not hold an extra last frame")
                            else:
                                if abs(timeline_duration - 5.0) > 0.101:
                                    errors.append(f"scene {sid}: video <5s must hold last frame to exactly 5s")
                                if scene.get("playback_mode") != "play_once_then_hold_last_frame":
                                    errors.append(f"scene {sid}: video <5s must play once then hold last frame")
                                if abs(hold_seconds - (5.0 - source_duration)) > 0.101:
                                    errors.append(f"scene {sid}: last_frame_hold_seconds must fill exactly to 5s")
                            if abs(timeline_duration - scene_duration) > 0.101:
                                errors.append(f"scene {sid}: video timeline duration must match Scene duration")
                            media_has_text = bool(text_id or scene.get("screen_en") or scene.get("screen_zh"))
                            if media_has_text:
                                if scene.get("text_overlay_engine") != "hyperframes":
                                    errors.append(f"scene {sid}: video text overlay must use HyperFrames")
                                if scene.get("text_overlay_scope") != "local_text_glass_only":
                                    errors.append(f"scene {sid}: video glass must be local to text only")
                    previous_master_ids = master_ids
                    previous_media_kind = media_kind
                else:
                    previous_master_ids = set()
                    previous_media_kind = ""
            if carrier in PRESENTER_CARRIERS:
                presenter_seconds += end - start
                if schema_version >= 6:
                    presenter_stage = str(scene.get("presenter_stage", ""))
                    is_opening_full = carrier == "presenter_opening_full" and presenter_stage == "opening_full"
                    is_closing_full = carrier == "presenter_closing_full" and presenter_stage == "closing_full_summary"
                    if is_opening_full:
                        opening_full_presenter_scenes.append(str(sid))
                        hyperframes_visible_scenes += 1
                        hyperframes_non_title = True
                        if scene.get("remotion_visible_motion") is not True:
                            errors.append(f"scene {sid}: opening presenter requires visible Remotion motion")
                        else:
                            remotion_visible_scenes += 1
                        if end > 15.0001:
                            errors.append(f"scene {sid}: opening presenter full screen must end by 15.0s")
                        if scene.get("visual_mode") != "presenter_opening_full_overlay":
                            errors.append(
                                f"scene {sid}: opening presenter visual_mode must be presenter_opening_full_overlay"
                            )
                        if scene.get("overlay_engine") != "hyperframes" or not scene.get("hyperframes_overlay_id"):
                            errors.append(
                                f"scene {sid}: opening presenter requires a real HyperFrames side overlay"
                            )
                        try:
                            side_count = int(scene.get("side_overlay_count", 0))
                        except (TypeError, ValueError):
                            side_count = 0
                        if not 2 <= side_count <= 4:
                            errors.append(f"scene {sid}: opening side_overlay_count must be 2..4")
                    elif is_closing_full:
                        closing_full_presenter_scenes.append(str(sid))
                        hyperframes_visible_scenes += 1
                        hyperframes_non_title = True
                        if scene.get("remotion_visible_motion") is not True:
                            errors.append(f"scene {sid}: closing presenter requires visible Remotion motion")
                        else:
                            remotion_visible_scenes += 1
                        if scene_index != len(scenes) - 1:
                            errors.append(f"scene {sid}: closing full-screen presenter must be the final scene")
                        if scene_function != "summarize":
                            errors.append(f"scene {sid}: closing full-screen presenter function must be summarize")
                        if scene.get("visual_mode") != "presenter_closing_full_summary":
                            errors.append(
                                f"scene {sid}: closing presenter visual_mode must be presenter_closing_full_summary"
                            )
                        if schema_version >= 8:
                            if scene.get("overlay_engine") not in {"hyperframes", "remotion"}:
                                errors.append(f"scene {sid}: closing presenter overlay_engine must be remotion or hyperframes")
                        elif scene.get("overlay_engine") != "hyperframes" or not scene.get("hyperframes_overlay_id"):
                            errors.append(f"scene {sid}: closing presenter requires a real HyperFrames summary overlay")
                        try:
                            side_count = int(scene.get("side_overlay_count", 0))
                        except (TypeError, ValueError):
                            side_count = 0
                        if not 2 <= side_count <= 4:
                            errors.append(f"scene {sid}: closing side_overlay_count must be 2..4")
                        if scene.get("summary_progression") not in {"progress_bar", "logic_arrows", "path", "step_reveal"}:
                            errors.append(
                                f"scene {sid}: closing summary requires progress_bar, logic_arrows, path, or step_reveal"
                            )
                    else:
                        if carrier != "presenter_pip_content_aware_circle_raised":
                            errors.append(
                                f"scene {sid}: presenter between opening and closing must use the raised content-aware PIP"
                            )
                        if scene.get("presenter_pip_shape") != "circle":
                            errors.append(f"scene {sid}: presenter_pip_shape must be circle")
                        if schema_version >= 8 and scene.get("presenter_pip_anchor") != "lower-right-raised":
                            errors.append(f"scene {sid}: presenter_pip_anchor must default to lower-right-raised")
                        elif schema_version < 8 and scene.get("presenter_pip_anchor") not in {"lower-right-raised", "lower-left-raised"}:
                            errors.append(f"scene {sid}: presenter_pip_anchor must use a raised left/right anchor")
                        try:
                            pip_diameter = float(scene.get("presenter_pip_diameter_px", 0))
                            pip_clearance = float(scene.get("pip_bottom_clearance_px", 0))
                        except (TypeError, ValueError):
                            pip_diameter, pip_clearance = 0, 0
                        if not 340 <= pip_diameter <= 380:
                            errors.append(f"scene {sid}: presenter_pip_diameter_px must be 340..380")
                        if pip_clearance < 220:
                            errors.append(f"scene {sid}: PIP must stay above the 220px subtitle exclusion zone")
                else:
                    if carrier in {"presenter", "presenter_full"} and not scene.get("opening_stage"):
                        if not scene.get("presenter_fullscreen_exception"):
                            errors.append(
                                f"scene {sid}: presenter full screen after opening requires presenter_fullscreen_exception"
                            )
                    if schema_version >= 4 and not scene.get("opening_stage"):
                        if carrier != "presenter_pip_lower_right_circle":
                            errors.append(f"scene {sid}: presenter after opening must use the lower-right circular PIP")
                        if scene.get("presenter_pip_shape") != "circle":
                            errors.append(f"scene {sid}: presenter_pip_shape must be circle")
                        try:
                            pip_diameter = float(scene.get("presenter_pip_diameter_px", 0))
                        except (TypeError, ValueError):
                            pip_diameter = 0
                        if not 340 <= pip_diameter <= 380:
                            errors.append(f"scene {sid}: presenter_pip_diameter_px must be 340..380")
            if scene.get("attention_reset"):
                attention_reset_times.append(start)
            has_text = bool(text_id or scene.get("screen_en") or scene.get("screen_zh"))
            if schema_version >= 7 and has_text:
                if not scene.get("semantic_segment_id"):
                    errors.append(f"scene {sid}: text-bearing scene requires semantic_segment_id")
                source_text_ids = scene.get("source_text_ids")
                if not isinstance(source_text_ids, list) or not source_text_ids:
                    errors.append(f"scene {sid}: text-bearing scene requires source_text_ids from one semantic segment")
                if scene.get("text_provenance") not in {
                    "verbatim", "faithful_compression", "approved_summary", "layout_only",
                }:
                    errors.append(f"scene {sid}: unsupported text_provenance")
                if scene.get("new_claims_added") is not False:
                    errors.append(f"scene {sid}: new_claims_added must be false")
                if scene.get("cross_chapter_merge") is not False:
                    errors.append(f"scene {sid}: cross_chapter_merge must be false")

            is_argument_bridge = scene_type == "argument_bridge"
            if schema_version >= 7 and is_argument_bridge:
                argument_bridge_seconds += scene_duration
                argument_bridge_by_chapter[chapter_key] = argument_bridge_by_chapter.get(chapter_key, 0) + 1
                if previous_was_argument_bridge:
                    errors.append(f"scene {sid}: argument_bridge scenes cannot be adjacent")
                if carrier != "hyperframes" or scene_function != "bridge_argument":
                    errors.append(f"scene {sid}: argument_bridge must use HyperFrames and bridge_argument")
                bridge = scene.get("argument_bridge")
                if not isinstance(bridge, dict):
                    errors.append(f"scene {sid}: argument_bridge details are required")
                else:
                    for field in ["insufficiency_reason", "left_en", "left_zh"]:
                        if not bridge.get(field):
                            errors.append(f"scene {sid}: argument_bridge.{field} is required")
                    try:
                        left_font_px = float(bridge.get("left_font_px", 0))
                        right_font_px = float(bridge.get("right_font_px", 0))
                    except (TypeError, ValueError):
                        left_font_px, right_font_px = 0, 0
                    if left_font_px < 88:
                        errors.append(f"scene {sid}: argument_bridge left_font_px must be at least 88")
                    if right_font_px < 48:
                        errors.append(f"scene {sid}: argument_bridge right_font_px must be at least 48")
                    items = bridge.get("right_items")
                    if not isinstance(items, list) or not 2 <= len(items) <= 4:
                        errors.append(f"scene {sid}: argument_bridge right_items must contain 2..4 bilingual items")
                    elif any(not isinstance(item, dict) or not item.get("en") or not item.get("zh") for item in items):
                        errors.append(f"scene {sid}: every argument_bridge right item requires en and zh")
                if not scene.get("semantic_segment_id") or not scene.get("source_text_ids"):
                    errors.append(f"scene {sid}: argument_bridge must cite one current semantic segment and source text IDs")
                if scene.get("new_claims_added") is not False or scene.get("cross_chapter_merge") is not False:
                    errors.append(f"scene {sid}: argument_bridge cannot add claims or merge chapters")
            previous_was_argument_bridge = is_argument_bridge
            material = scene.get("material")
            background_visibility = scene.get("background_visibility")
            if material is not None and material not in ALLOWED_MATERIALS:
                errors.append(f"scene {sid}: unsupported material {material!r}")
            if background_visibility is not None and background_visibility not in ALLOWED_BACKGROUND_VISIBILITY:
                errors.append(f"scene {sid}: unsupported background_visibility {background_visibility!r}")
            if carrier in programmatic_carriers:
                planned = animation_by_scene.get(str(sid))
                if planned is None:
                    errors.append(f"scene {sid}: programmatic scene requires animation-plan entry")
                else:
                    selection = scene.get("library_selection")
                    if not isinstance(selection, dict):
                        errors.append(f"scene {sid}: programmatic scene requires library_selection")
                    else:
                        planned_primary = (planned.get("primary_selection") or {}).get("id")
                        planned_ambient = (planned.get("ambient_selection") or {}).get("id")
                        if selection.get("primary") != planned_primary:
                            errors.append(f"scene {sid}: library_selection.primary differs from animation-plan")
                        if selection.get("ambient") != planned_ambient:
                            errors.append(f"scene {sid}: library_selection.ambient differs from animation-plan")
                    if schema_version >= 6:
                        planned_engine = str(planned.get("engine", "")).lower()
                        if planned_engine != carrier:
                            errors.append(
                                f"scene {sid}: carrier {carrier!r} must match animation-plan engine {planned_engine!r}"
                            )
                        programmatic_by_chapter[chapter_key] = programmatic_by_chapter.get(chapter_key, 0) + 1
                        if planned_engine == "hyperframes":
                            hyperframes_by_chapter[chapter_key] = hyperframes_by_chapter.get(chapter_key, 0) + 1
                            hyperframes_visible_scenes += 1
                            if scene_type != "chapter_title":
                                hyperframes_non_title = True
                        elif planned_engine == "remotion":
                            remotion_visible_scenes += 1
                        family = str(planned.get("motion_family", ""))
                        if family:
                            motion_families_by_chapter.setdefault(chapter_key, set()).add(family)
                        signature = planned.get("motion_signature")
                        signature_key = (
                            planned_engine,
                            family,
                            json.dumps(signature, ensure_ascii=False, sort_keys=True)
                            if isinstance(signature, dict) else "",
                        )
                        visual_page_id = str(planned.get("visual_page_id", ""))
                        content_fingerprint = str(planned.get("content_fingerprint", ""))
                        if previous_programmatic is not None:
                            previous_key = previous_programmatic["signature_key"]
                            if signature_key == previous_key:
                                errors.append(
                                    f"scene {sid}: adjacent programmatic scenes cannot use an identical engine/motion signature"
                                )
                            if family and family == previous_programmatic["family"]:
                                variation = planned.get("variation_from_previous") or {}
                                mode = variation.get("mode")
                                if mode == "changed":
                                    dimensions = {
                                        str(value) for value in variation.get("changed_dimensions", []) if str(value)
                                    }
                                    if len(dimensions) < 2:
                                        errors.append(
                                            f"scene {sid}: same motion family requires at least two changed dimensions"
                                        )
                                elif mode == "slower":
                                    try:
                                        multiplier = float(variation.get("pace_multiplier", 0))
                                    except (TypeError, ValueError):
                                        multiplier = 0
                                    if not 1.25 <= multiplier <= 1.60:
                                        errors.append(
                                            f"scene {sid}: slow variation pace_multiplier must be 1.25..1.60"
                                        )
                                else:
                                    errors.append(
                                        f"scene {sid}: adjacent same motion family requires changed or slower variation"
                                    )
                            if visual_page_id and visual_page_id == previous_programmatic["visual_page_id"]:
                                errors.append(
                                    f"scene {sid}: the same visual page cannot play in adjacent scenes"
                                )
                            if content_fingerprint and content_fingerprint == previous_programmatic["content_fingerprint"]:
                                errors.append(
                                    f"scene {sid}: adjacent summary/information pages must contain different content"
                                )
                        previous_programmatic = {
                            "signature_key": signature_key,
                            "family": family,
                            "visual_page_id": visual_page_id,
                            "content_fingerprint": content_fingerprint,
                        }
                intents = scene.get("animation_intent", [])
                if not isinstance(intents, list) or not intents:
                    errors.append(f"scene {sid}: programmatic scene requires animation_intent")
                if scene.get("motion_role") not in ALLOWED_MOTION_ROLES:
                    errors.append(f"scene {sid}: programmatic scene requires a valid motion_role")
                if not scene.get("subject_safe_zones"):
                    errors.append(f"scene {sid}: programmatic scene requires subject_safe_zones")
                if background_visibility not in ALLOWED_BACKGROUND_VISIBILITY:
                    errors.append(f"scene {sid}: programmatic scene requires background_visibility")
                if has_text and material not in ALLOWED_MATERIALS:
                    errors.append(f"scene {sid}: text-bearing programmatic scene requires material")
                if has_text and material == "none" and not scene.get("material_reason"):
                    errors.append(f"scene {sid}: material 'none' requires material_reason")
            if has_text:
                if schema_version >= 6:
                    try:
                        subtitle_exclusion = float(scene.get("subtitle_exclusion_bottom_px", 0))
                    except (TypeError, ValueError):
                        subtitle_exclusion = 0
                    if subtitle_exclusion < 220:
                        errors.append(
                            f"scene {sid}: text/graphics must reserve at least 220px for bottom subtitles"
                        )
                    if not scene.get("text_motion"):
                        errors.append(f"scene {sid}: text-bearing scene requires text_motion")
                    if scene.get("left_component_present") is True and scene.get("right_content_flow") != "vertical":
                        errors.append(f"scene {sid}: right-side content must flow vertically when a left component exists")
                legibility = scene.get("legibility")
                if not isinstance(legibility, dict):
                    errors.append(f"scene {sid}: text-bearing scene requires legibility object")
                else:
                    text_class = str(legibility.get("text_class", "body")).lower()
                    required_contrast = 3.0 if text_class in {"large", "display"} else 4.5
                    try:
                        scene_contrast = float(legibility.get("contrast_ratio_target", 0))
                    except (TypeError, ValueError):
                        scene_contrast = 0
                    if scene_contrast < required_contrast:
                        errors.append(
                            f"scene {sid}: contrast target {scene_contrast:g} is below {required_contrast:g}:1"
                        )
                    if not legibility.get("busy_frame"):
                        errors.append(f"scene {sid}: legibility.busy_frame is required")
                    if schema_version >= 6:
                        minimum_by_class = {
                            "display": 96,
                            "large": 64,
                            "body": 42,
                            "support": 32,
                            "source": 26,
                            "meta": 26,
                        }
                        try:
                            minimum_font_px = float(legibility.get("minimum_font_px", 0))
                        except (TypeError, ValueError):
                            minimum_font_px = 0
                        required_font_px = minimum_by_class.get(text_class, 42)
                        if minimum_font_px < required_font_px:
                            errors.append(
                                f"scene {sid}: {text_class} text minimum_font_px must be at least {required_font_px}"
                            )
        if schema_version >= 6:
            if presenter_seconds > 0:
                if len(opening_full_presenter_scenes) != 1:
                    errors.append(
                        "presenter projects require exactly one opening full-screen scene ending by 15s"
                    )
                if len(closing_full_presenter_scenes) != 1:
                    errors.append(
                        "presenter projects require exactly one final full-screen summary scene"
                    )
            total_programmatic_scenes = sum(programmatic_by_chapter.values())
            if schema_version < 8 and (total_programmatic_scenes >= 2 or presenter_seconds > 0):
                if remotion_visible_scenes < 1:
                    errors.append("Remotion must contribute visible motion, not only master-timeline assembly")
                if hyperframes_visible_scenes < 1:
                    errors.append("HyperFrames must contribute visible motion")
            if schema_version < 8 and hyperframes_visible_scenes > 0 and not hyperframes_non_title:
                errors.append("HyperFrames cannot be used only for chapter_title scenes")
            if 7 <= schema_version < 8 and total_programmatic_scenes > 0:
                hyperframes_programmatic = sum(hyperframes_by_chapter.values())
                hyperframes_share = hyperframes_programmatic / total_programmatic_scenes
                if hyperframes_share + 1e-9 < 0.40:
                    errors.append(
                        f"HyperFrames must be used in at least 40% of programmatic scenes; got {hyperframes_share:.2%}"
                    )
            for key, programmatic_count in programmatic_by_chapter.items():
                if key in OPENING_CHAPTERS:
                    continue
                required_hf_count = 0 if schema_version >= 8 else (1 if schema_version >= 7 else (1 if programmatic_count >= 3 else 0))
                if required_hf_count and hyperframes_by_chapter.get(key, 0) < 1:
                    errors.append(
                        f"chapter {key!r}: at least one HyperFrames scene is required when the chapter uses programmatic motion"
                    )
                bounds = chapter_time_bounds.get(key, [0.0, 0.0])
                chapter_duration = max(0.0, bounds[1] - bounds[0])
                required_families = 3 if chapter_duration > 60 and programmatic_count >= 3 else 2
                if programmatic_count >= required_families:
                    actual_families = len(motion_families_by_chapter.get(key, set()))
                    if actual_families < required_families:
                        errors.append(
                            f"chapter {key!r}: requires {required_families} motion families; got {actual_families}"
                        )

        duration = project.get("audio_duration_seconds")
        if duration is not None and previous_end is not None and abs(previous_end - float(duration)) > 0.101:
            errors.append(f"timeline ends at {previous_end:.3f}s, audio is {float(duration):.3f}s")
        total_duration = float(duration) if duration is not None else float(previous_end or 0)
        if schema_version >= 7:
            for key, count in argument_bridge_by_chapter.items():
                if count > 1:
                    errors.append(f"chapter {key!r}: argument_bridge may appear at most once")
            if total_duration > 0 and argument_bridge_seconds > 0:
                bridge_ratio = argument_bridge_seconds / total_duration
                if bridge_ratio > 0.0600001:
                    errors.append(f"argument_bridge hard maximum is 6%; got {bridge_ratio:.2%}")
                elif bridge_ratio < 0.04:
                    warnings.append(f"argument_bridge target is 4%-6% when used; got {bridge_ratio:.2%}")
        if total_duration > 0 and presenter_seconds / total_duration >= 0.20:
            errors.append(
                f"presenter ratio must be below 20%; got {presenter_seconds / total_duration:.2%}"
            )
        if total_duration > 1800:
            if not attention_reset_times:
                errors.append("videos over 30 minutes require attention_reset scenes every 5-8 minutes")
            else:
                intervals = [attention_reset_times[0]] + [
                    current - previous for previous, current in zip(attention_reset_times, attention_reset_times[1:])
                ]
                for index, interval in enumerate(intervals, 1):
                    if not 300 <= interval <= 480:
                        errors.append(
                            f"attention reset interval {index} must be 300..480s; got {interval:.3f}s"
                        )
                tail = total_duration - attention_reset_times[-1]
                if tail > 480:
                    errors.append(f"final attention-reset tail must be <=480s; got {tail:.3f}s")

        asset_requirements = load_json(root / "04_spec" / "asset-requirements.json", errors)
        ai_videos = asset_requirements.get("ai_video_requests", [])
        if not isinstance(ai_videos, list):
            errors.append("asset-requirements ai_video_requests must be a list")
        else:
            limit = 250 if schema_version >= 8 else 100
            if len(ai_videos) > limit:
                errors.append(f"AI video requests must not exceed {limit}; got {len(ai_videos)}")
            for item in ai_videos:
                item_id = item.get("id", "?")
                try:
                    duration = float(item.get("duration_seconds", 0))
                    if schema_version >= 8 and not 5.0 <= duration <= 15.0:
                        errors.append(f"AI video {item_id}: duration_seconds must be 5.0..15.0")
                    elif schema_version < 8 and abs(duration - 5.0) > 0.001:
                        errors.append(f"AI video {item_id}: duration_seconds must be 5.0")
                except (TypeError, ValueError):
                    errors.append(f"AI video {item_id}: duration_seconds must be numeric")
                for field in ["prompt_zh", "prompt_en"]:
                    if not item.get(field):
                        errors.append(f"AI video {item_id}: {field} is required")
                if schema_version >= 4:
                    if item.get("no_subtitles") is not True:
                        errors.append(f"AI video {item_id}: no_subtitles must be true")
                    for field in ["source_line", "visible_subject", "era", "location", "action", "evidence_role"]:
                        if not item.get(field):
                            errors.append(f"AI video {item_id}: {field} is required for semantic matching")

        if schema_version >= 4:
            for list_name in ["real_image_requests", "ai_image_requests", "real_video_requests"]:
                rows = asset_requirements.get(list_name, [])
                if not isinstance(rows, list):
                    errors.append(f"asset-requirements {list_name} must be a list")
                    continue
                for item in rows:
                    item_id = item.get("id", "?")
                    for field in ["source_line", "visible_subject", "era", "location", "evidence_role"]:
                        if not item.get(field):
                            errors.append(f"{list_name} {item_id}: {field} is required for semantic matching")
                    if schema_version >= 8 and list_name == "ai_image_requests":
                        for field in ["semantic_segment_id", "timecode", "planned_duration_seconds", "variant_role"]:
                            if item.get(field) in (None, ""):
                                errors.append(f"AI image {item_id}: {field} is required for coverage planning")
                        if item.get("expected_use_count", 1) != 1:
                            errors.append(f"AI image {item_id}: expected_use_count must be 1")

        if schema_version >= 8:
            coverage = asset_requirements.get("coverage_policy", {})
            expected_coverage = {
                "ai_image_count_cap": None,
                "ai_video_count_cap": 250,
                "ai_video_duration_seconds_range": [5, 15],
                "expected_ai_image_use_count": 1,
                "required_segments_must_have_primary_and_backup_or_programmatic_fallback": True,
            }
            for key, value in expected_coverage.items():
                if coverage.get(key) != value:
                    errors.append(f"asset-requirements coverage_policy.{key} must be {value!r}")

        if presenter_seconds > 0:
            presenter_plan = load_json(root / "05_assets" / "presenter" / "presenter-plan.json", errors)
            protocol = presenter_plan.get("recording_protocol", {})
            expected_protocol = {
                "head_silence_seconds": 5,
                "tail_silence_seconds": 5,
                "start_signal": "double_beep",
                "end_signal": "double_beep",
                "source_capture": (
                    "16:9_fullscreen_centered_circle_crop_safe"
                    if schema_version >= 4 else "16:9_fullscreen_centered"
                ),
            }
            for key, value in expected_protocol.items():
                if protocol.get(key) != value:
                    errors.append(f"presenter recording_protocol.{key} must be {value!r}")
            if schema_version >= 4:
                if protocol.get("final_pip_shape") != "circle":
                    errors.append("presenter recording_protocol.final_pip_shape must be 'circle'")
                if protocol.get("final_pip_diameter_px") != 360:
                    errors.append("presenter recording_protocol.final_pip_diameter_px must be 360")
            if schema_version >= 8:
                expected_presenter_v6 = {
                    "final_pip_default_anchor": "lower-right-raised",
                    "final_pip_alternate_requires_user_approval": True,
                    "subtitle_exclusion_bottom_px": 220,
                    "opening_fullscreen_max_seconds": 15.0,
                    "closing_fullscreen_summary": True,
                }
                for key, value in expected_presenter_v6.items():
                    if protocol.get(key) != value:
                        errors.append(f"presenter recording_protocol.{key} must be {value!r}")
            elif schema_version >= 6:
                expected_presenter_v6 = {
                    "final_pip_anchor_options": ["lower-right-raised", "lower-left-raised"],
                    "subtitle_exclusion_bottom_px": 220,
                    "opening_fullscreen_max_seconds": 15.0,
                    "closing_fullscreen_summary": True,
                }
                for key, value in expected_presenter_v6.items():
                    if protocol.get(key) != value:
                        errors.append(f"presenter recording_protocol.{key} must be {value!r}")

    if level >= STATUS_ORDER["QA"]:
        sound = load_json(root / "08_audio" / "sound-plan.json", errors)
        stale = [cue.get("id", "?") for cue in sound.get("cues", []) if cue.get("status") == "STALE"]
        if stale:
            errors.append("stale sound cues remain: " + ", ".join(map(str, stale)))
        qa = sound.get("qa", {})
        for device in ["headphones", "phone", "computer"]:
            if qa.get(device) != "PASS":
                errors.append(f"sound QA {device} is not PASS")
        if schema_version >= 6 and hyperframes_visible_scenes > 0:
            hyperframes_qa = load_json(
                root / "07_hyperframes" / "qa" / "hyperframes-qa.json", errors
            )
            expected_hyperframes_qa = {
                "lint": "PASS",
                "validate": "PASS",
                "inspect": "PASS",
                "animation_map": "REVIEWED",
            }
            for key, value in expected_hyperframes_qa.items():
                if hyperframes_qa.get(key) != value:
                    errors.append(f"HyperFrames QA {key} must be {value}")
        if schema_version >= 4:
            delivery = sound.get("delivery", {})
            if delivery.get("video_master_audio_mode") != "no_audio_stream":
                errors.append("sound delivery.video_master_audio_mode must be no_audio_stream")
            sourcing = sound.get("music_sourcing", {})
            allowed_sources = set(map(str, sourcing.get("allowed_sources", [])))
            if not {"ai_original_light_music", "youtube_studio_audio_library"}.issubset(allowed_sources):
                errors.append("sound music_sourcing must allow AI original light music and YouTube Studio Audio Library")
            if sourcing.get("ordinary_youtube_channels_allowed") is not False:
                errors.append("sound plan must forbid ordinary YouTube channels as assumed-free music")

            render_plan = load_json(root / "09_qa" / "render-plan.json", errors)
            if render_plan.get("max_segment_seconds") != 300:
                errors.append("render-plan max_segment_seconds must be 300")
            if render_plan.get("progress_report_interval_seconds") != 300:
                errors.append("render-plan progress_report_interval_seconds must be 300")
            if render_plan.get("prefer_gpu") is not True:
                errors.append("render-plan prefer_gpu must be true")
            if schema_version >= 5:
                if render_plan.get("schema_version") != 2:
                    errors.append("render-plan schema_version must be 2")
                tuning = render_plan.get("resource_tuning", {})
                if tuning.get("adaptive_concurrency") is not True:
                    errors.append("render-plan resource_tuning.adaptive_concurrency must be true")
                if tuning.get("parallel_encoding") is not True:
                    errors.append("render-plan resource_tuning.parallel_encoding must be true")
                try:
                    logical_threads = int(render_plan.get("detected_hardware", {}).get("logical_cpu_threads", 0))
                    initial_concurrency = int(tuning.get("initial_concurrency", 0))
                    candidates = [int(value) for value in tuning.get("concurrency_candidates", [])]
                except (TypeError, ValueError):
                    logical_threads, initial_concurrency, candidates = 0, 0, []
                if logical_threads <= 0:
                    errors.append("render-plan must record detected logical CPU threads")
                if not candidates or initial_concurrency not in candidates:
                    errors.append("render-plan initial_concurrency must be one of the concurrency candidates")
                if any(value <= 0 or value > logical_threads for value in candidates):
                    errors.append("render-plan concurrency candidates must be within logical CPU capacity")
                for key in ["media_cache_size_in_bytes", "offthreadvideo_cache_size_in_bytes"]:
                    try:
                        if int(tuning.get(key, 0)) <= 0:
                            errors.append(f"render-plan resource_tuning.{key} must be positive")
                    except (TypeError, ValueError):
                        errors.append(f"render-plan resource_tuning.{key} must be numeric")
                targets = tuning.get("targets_percent", {})
                expected_targets = {
                    "cpu_working_range": [75, 95],
                    "gpu_working_range_when_eligible": [65, 95],
                    "ram_working_range": [55, 78],
                    "vram_working_range": [55, 85],
                }
                for key, value in expected_targets.items():
                    if targets.get(key) != value:
                        errors.append(f"render-plan resource target {key} must be {value!r}")
                monitor = render_plan.get("progress_monitor", {})
                expected_monitor = {
                    "script": "scripts/watch_render_progress.py",
                    "resource_sample_interval_seconds": 15,
                    "heartbeat_interval_seconds": 300,
                    "low_utilization_window_seconds": 90,
                    "stall_diagnostic_seconds": 180,
                    "hard_stall_seconds": 300,
                    "heartbeat_is_required_even_without_progress": True,
                    "automatic_diagnostic_on_stall": True,
                }
                for key, value in expected_monitor.items():
                    if monitor.get(key) != value:
                        errors.append(f"render-plan progress_monitor.{key} must be {value!r}")
                template = str(render_plan.get("render_template", ""))
                for flag in [
                    "--concurrency=", "--offthreadvideo-video-threads=",
                    "--media-cache-size-in-bytes=", "--offthreadvideo-cache-size-in-bytes=",
                    "--hardware-acceleration if-possible", "--color-space=bt709", "--log=verbose",
                ]:
                    if flag not in template:
                        errors.append(f"render-plan render_template missing {flag}")
                if "--disallow-parallel-encoding" in template:
                    errors.append("render-plan must keep parallel encoding enabled by default")
            segments = render_plan.get("segments", [])
            if not isinstance(segments, list) or not segments:
                errors.append("render-plan requires at least one segment")
            else:
                for segment in segments:
                    segment_id = segment.get("id", "?")
                    try:
                        segment_duration = float(segment.get("duration_seconds", 0))
                    except (TypeError, ValueError):
                        segment_duration = 0
                    if not 0 < segment_duration <= 300.001:
                        errors.append(f"render segment {segment_id}: duration must be >0 and <=300s")
                    if not segment.get("scene_ids"):
                        errors.append(f"render segment {segment_id}: scene_ids are required")

    manifest = root / "source-manifest.csv"
    if not manifest.exists():
        errors.append(f"missing: {manifest}")
    else:
        manifest_lines = manifest.read_text(encoding="utf-8-sig").splitlines()
        if schema_version >= 7:
            required_manifest_columns = {
                "id", "manifest_order", "type", "assigned_asset_path", "assigned_script_segment_id",
                "user_verified", "assignment_locked", "assignment_reassessed", "source_duration_seconds",
            }
            header_columns = set(manifest_lines[0].split(",")) if manifest_lines else set()
            missing_columns = sorted(required_manifest_columns - header_columns)
            if missing_columns:
                errors.append(f"source manifest missing locked-assignment columns {missing_columns}")
        if level >= STATUS_ORDER["PRODUCTION_RELEASED"] and len(manifest_lines) <= 1:
            warnings.append("source manifest has no asset rows")

    if level >= STATUS_ORDER["DELIVERED"]:
        deliverables = root / "10_deliverables"
        required_documents = [
            "视频剪辑执行说明书.txt",
            "图片资料搜集需求单.docx",
            "图片AI生成需求单.docx",
            "视频AI生成需求单.docx",
            "真人露脸补录台词清单.docx",
            "动效文字执行手册.docx",
        ]
        for name in required_documents:
            path = deliverables / name
            if not path.exists():
                errors.append(f"missing delivered document: {path}")
        if presenter_seconds > 0:
            audio_manifest = load_json(root / "05_assets" / "audio" / "presenter-audio-manifest.json", errors)
            audio_rows = audio_manifest.get("segments", [])
            if not isinstance(audio_rows, list) or not audio_rows:
                errors.append("presenter-audio-manifest requires at least one segment")
            else:
                for row in audio_rows:
                    row_id = row.get("id", "?")
                    if row.get("guide_head_silence_seconds") != 5.0:
                        errors.append(f"presenter audio {row_id}: head silence must be 5.0s")
                    if row.get("guide_tail_silence_seconds") != 5.0:
                        errors.append(f"presenter audio {row_id}: tail silence must be 5.0s")
                    if "double 1000Hz beep" not in str(row.get("signals", "")):
                        errors.append(f"presenter audio {row_id}: double start/end beep signal is required")
                    for field in ["exact_file", "guide_file"]:
                        media_path = Path(str(row.get(field, "")))
                        if not media_path.is_file():
                            errors.append(f"presenter audio {row_id}: missing {field} {media_path}")

    result = {
        "project_root": str(root),
        "status": status,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
