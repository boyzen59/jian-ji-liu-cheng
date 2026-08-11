#!/usr/bin/env python3
"""Create a non-destructive project scaffold for jian-ji-liu-cheng."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


THEME_TS = """export const softSignal = {
  name: 'Soft Signal',
  designLanguage: 'Apple-inspired warmth',
  materialLanguage: 'frosted-glass',
  colors: {
    background: '#FFF8F0', surface: '#FFFFFF', elevated: '#FFF5EA',
    foreground: '#3D3028', foregroundSecondary: 'rgba(61,48,40,0.66)',
    foregroundMuted: 'rgba(61,48,40,0.42)', foregroundFaint: 'rgba(61,48,40,0.18)',
    accent: '#E8734A', accent2: 'rgba(232,115,74,0.40)', accent3: 'rgba(232,115,74,0.14)',
    line: 'rgba(61,48,40,0.08)', lineStrong: 'rgba(61,48,40,0.16)',
    lineStrongest: 'rgba(61,48,40,0.28)', flash: '#3D3028',
    green: '#6BAA6B', red: '#CC6B6B', yellow: '#C4A646',
  },
  typography: {
    displayFont: '\"SF Pro Display\", -apple-system, BlinkMacSystemFont, \"Helvetica Neue\", \"PingFang SC\", sans-serif',
    sansFont: '\"SF Pro Text\", -apple-system, BlinkMacSystemFont, \"Helvetica Neue\", \"PingFang SC\", sans-serif',
    monoFont: '\"SFMono-Regular\", \"SF Mono\", \"IBM Plex Mono\", \"Menlo\", monospace',
    chineseFont: '\"PingFang SC\", \"Hiragino Sans GB\", \"Microsoft YaHei\", sans-serif',
    serifFont: '\"Lora\", \"Georgia\", serif',
    scale: {chapterDisplayMin: 156, chapterDisplayMax: 220, display: 128, conclusion: 112, h1: 96, h2: 72, h3: 56, body: 46, small: 34, cap: 30, meta: 26},
    minimum: {body: 42, support: 32, sourceMeta: 26},
    weight: {regular: 400, mid: 600, bold: 700, heavy: 800},
    letterSpacing: {display: '-0.025em', h1: '-0.018em', h2: '-0.01em', body: '0', small: '0.01em', caps: '0.08em', meta: '0.12em'},
    lineHeight: {display: 1.02, heading: 1.1, tight: 1.25, body: 1.55},
    opticalSizing: 'auto',
  },
  spacing: {s1: 8, s2: 16, s3: 24, s4: 40, s5: 56, s6: 80},
  borderRadius: {none: 0, sm: 10, md: 18, lg: 28, xl: 40},
  materials: {
    glassThin: {
      background: 'rgba(255,255,255,0.56)', blur: 18, saturate: 1.25,
      border: 'rgba(255,255,255,0.64)', shadow: '0 8px 24px rgba(61,48,40,0.08)',
    },
    glassRegular: {
      background: 'rgba(255,248,240,0.70)', blur: 26, saturate: 1.35,
      border: 'rgba(255,255,255,0.72)', shadow: '0 16px 48px rgba(61,48,40,0.12)',
    },
    glassThick: {
      background: 'rgba(255,248,240,0.84)', blur: 36, saturate: 1.20,
      border: 'rgba(255,255,255,0.82)', shadow: '0 24px 64px rgba(61,48,40,0.16)',
    },
    backgroundPatternOpacity: {min: 0.08, default: 0.14, max: 0.24},
    textScrim: 'rgba(255,248,240,0.88)',
  },
  accessibility: {contrastBody: 4.5, contrastLarge: 3, reducedMotion: true, reducedTransparency: true, highContrast: true},
  motion: {
    easeOut: 'cubic-bezier(0.22, 1, 0.36, 1)', easeIn: 'cubic-bezier(0.55, 0, 1, 0.45)',
    easeSoft: 'cubic-bezier(0.4, 0, 0.2, 1)',
    durationFast: 250, durationNormal: 500, durationSlow: 1000, durationHero: 1200,
    springGentle: {mass: 1, stiffness: 130, damping: 23},
    springStandard: {mass: 1, stiffness: 170, damping: 26},
    springSnappy: {mass: 1, stiffness: 220, damping: 30},
    springMomentum: {mass: 1, stiffness: 170, damping: 21},
  },
  decoration: {
    density: 'restrained-experiential', ambientMotionAllowed: true, maxAmbientFamiliesPerScene: 1,
    subjectPriority: 'text-face-gesture-data-evidence-ui', backgroundTexture: 'subtle-through-glass',
  },
  subtitleSafe: {bottomExclusion: 220, minHeightRatio: 0.15, horizontalInset: 120},
  presenterPip: {shape: 'circle', diameter: 360, minDiameter: 340, maxDiameter: 380, borderWidth: 2, defaultAnchor: 'lower-right-raised', alternateRequiresApproval: true},
} as const;
"""


def now_local() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def write_if_missing(path: Path, content: str, created: list[str], skipped: list[str]) -> None:
    if path.exists():
        skipped.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))


def load_library_summary() -> tuple[str, dict]:
    catalog_path = Path(__file__).resolve().parents[1] / "assets" / "remotion-library" / "catalog.json"
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
        return str(catalog["catalog_revision"]), dict(catalog["inventory"])
    except (FileNotFoundError, KeyError, json.JSONDecodeError, OSError, TypeError):
        return "[待重建]", {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a reusable video-production project.")
    parser.add_argument("project_root", type=Path, help="Explicit target project directory")
    parser.add_argument("--name", required=True, help="Project display name")
    parser.add_argument("--width", type=int, default=2560)
    parser.add_argument("--height", type=int, default=1440)
    parser.add_argument("--fps", type=int, default=60)
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0 or args.fps <= 0:
        parser.error("width, height, and fps must be positive")

    root = args.project_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    dirs = [
        "00_input", "01_brief", "02_transcript", "03_review", "04_spec",
        "05_assets/user", "05_assets/search", "05_assets/ai", "05_assets/programmatic",
        "05_assets/presenter", "05_assets/audio/exact", "05_assets/audio/guide",
        "05_assets/research", "06_remotion/src", "07_hyperframes", "07_hyperframes/compositions", "07_hyperframes/qa",
        "07_programmatic/lottie", "07_programmatic/d3", "07_programmatic/blender", "07_programmatic/manim",
        "08_audio", "09_qa", "10_deliverables",
    ]
    for rel in dirs:
        (root / rel).mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []
    catalog_revision, catalog_inventory = load_library_summary()
    project = {
        "schema_version": 8,
        "project": args.name,
        "created_at": now_local(),
        "status": "INTAKE",
        "spec": {
            "width": args.width,
            "height": args.height,
            "fps": args.fps,
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
        },
        "time_source": "[待补充]",
        "audio_duration_seconds": None,
        "sidecar_delivery": {
            "captions": ["srt", "ass"],
            "audio_sample_rate": 48000,
            "audio_files": ["voice.wav", "bgm.wav", "sfx.wav", "review_mix.wav"],
        },
        "render_policy": {
            "prefer_gpu": True,
            "hardware_acceleration": "if-possible",
            "gl_backend": "auto_by_remotion_version",
            "cpu_fallback": True,
            "max_segment_seconds": 300,
            "progress_report_interval_seconds": 300,
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
        },
        "music_policy": {
            "voice_priority": "highest",
            "preferred_sources": ["ai_original_light_music", "youtube_studio_audio_library"],
            "ordinary_youtube_channels_allowed": False,
            "license_record_required": True,
        },
        "fixed_theme": {
            "name": "Soft Signal",
            "label_zh": "亲密 · 温暖",
            "accent": "#E8734A",
            "design_language": "Apple-inspired warmth",
            "material": "frosted-glass",
        },
        "text_review_release": None,
        "remotion_library": {
            "catalog_revision": catalog_revision,
            "entry_count": sum(
                value for counts in catalog_inventory.values() for key, value in counts.items()
                if key in {"styles", "templates", "scenes", "components", "effects"}
            ),
        },
        "assumptions": [],
    }
    write_if_missing(root / "project.json", json.dumps(project, ensure_ascii=False, indent=2) + "\n", created, skipped)
    write_if_missing(
        root / "01_brief" / "project-brief.md",
        "# 项目简报\n\n- 生成时间：[待生成]\n- 状态：[READY / READY_WITH_ASSUMPTIONS / BLOCKED]\n- 目的：\n- 受众：\n- 核心命题：\n- 平台与规格：H.264 / Rec.709 / 2560×1440 / 60fps CFR / MP4 / 无音频流\n- 时间基准：\n- 外挂字幕与双语解释文字：连续字幕不烧录；底部保留220px字幕排除区；既有文字已通过，仅新增/改字增量审阅\n- 章节策略：每章先用156–220px超大双语标题铺满主视觉区的程序化动态总览，再进入正文\n- 真人策略：成片占比 <20%；只有总开头和实际最终结尾全屏；中段固定抬高右下圆窗；最终全屏持续到最后一帧\n- 素材锁：严格按用户核对清单顺序与文案对应使用，不重新匹配、交换或跨段借用\n- 图片策略：普通/AI图片清晰全屏并按语义变化运动；图片需求不设上限，按时间线覆盖量生成主画面/细节/衔接/备用\n- 证据资料：archive_evidence与book_evidence使用简中+英文来源区和清晰证据图；在屏时禁止动态说理\n- 视频策略：清晰原画全屏、静音、不循环；AI视频每条5–15秒且全项目不超过250条\n- Shotcraft：锁定原文后逐镜执行video-shotcraft语义pass，并与RVE/Scenes/Curvable/Playground/HyperFrames候选同场比较\n- 双栏补位：仅缺少合适媒体/具体动态图解时使用；目标4%–6%、硬上限6%、每章最多一场且不连续\n- 叙事曲线：\n- 注意力重置：长于 30 分钟时每 5–8 分钟一次\n- 玻璃材质与背景显隐：Soft Signal / Apple-inspired / frosted-glass；玻璃只包文字，媒体本体保持清晰\n- 可读性目标：正文 4.5:1，大字 3:1；正文42–54px，辅助至少32px\n- 动效方向：Remotion与HyperFrames逐镜比较，不设引擎比例或配额；动效覆盖缺少媒体的叙事区间\n- 转场方向：章节接缝不得裸硬切；普通硬切仅用于有理由的语义撞击\n- GPU/分段：GPU if-possible；每段不超过300秒；每5分钟固定心跳；180秒无进展自动诊断；分段间自适应并发\n- 声音方向：主录音优先；AI轻音乐或YouTube Studio Audio Library；voice/BGM/SFX独立stems与审片混音\n- 风险与待确认：\n",
        created,
        skipped,
    )
    review = {
        "project": args.name,
        "version": "V1",
        "fps": args.fps,
        "review_mode": "delta_only",
        "baseline_existing_text_approved": True,
        "source_files": [],
        "rows": [],
    }
    write_if_missing(root / "03_review" / "text-review.json", json.dumps(review, ensure_ascii=False, indent=2) + "\n", created, skipped)
    outline = {
        "project": args.name,
        "version": "V1",
        "source_files": [],
        "segments": [],
        "allowed_scene_types": [
            "chapter_title", "chart", "screenshot", "data", "key_text", "image_explainer", "archive", "map",
            "relationship", "environment", "presenter", "argument_bridge",
        ],
    }
    write_if_missing(
        root / "04_spec" / "outline-scene-types.json",
        json.dumps(outline, ensure_ascii=False, indent=2) + "\n",
        created,
        skipped,
    )
    spec = {
        "project": args.name,
        "version": "V1",
        "fps": args.fps,
        "output": project["spec"],
        "audio_duration_seconds": None,
        "presenter_policy": {
            "max_ratio_exclusive": 0.20,
            "opening_fullscreen_allowed": True,
            "opening_fullscreen_max_seconds": 15.0,
            "opening_programmatic_overlays_required": True,
            "opening_side_overlay_count_range": [2, 4],
            "after_opening_default": "presenter_pip_lower_right_circle_raised",
            "intermediate_fullscreen_forbidden": True,
            "closing_fullscreen_summary_required": True,
            "closing_programmatic_overlays_required": True,
            "closing_fullscreen_must_reach_final_frame": True,
            "closing_side_overlay_count_range": [2, 4],
            "pip_shape": "circle",
            "pip_diameter_px": 360,
            "pip_diameter_range_px": [340, 380],
            "pip_default_anchor": "lower-right-raised",
            "pip_alternate_requires_user_approval": True,
            "pip_bottom_clearance_px": 220,
        },
        "chapter_policy": {
            "required": True,
            "scene_type": "chapter_title",
            "carrier": ["remotion", "hyperframes"],
            "fullscreen": True,
            "bilingual": True,
            "title_font_px_range": [156, 220],
            "overview_item_count_range": [2, 4],
            "sound_emphasis": True,
            "chapter_hard_cut_allowed": False,
        },
        "caption_policy": {
            "burned_in": False,
            "delivery": "sidecar_srt_ass",
            "bilingual_explainer_text_allowed": True,
            "bottom_exclusion_px": 220,
            "overlays_must_stay_above_exclusion": True,
        },
        "motion_policy": {
            "prefer_remotion_hyperframes": True,
            "engine_usage_quota_enforced": False,
            "assess_every_scene": True,
            "chapter_transition_required": True,
            "hard_cut_requires_reason": True,
            "adjacent_identical_motion_signature_forbidden": True,
            "adjacent_same_visual_page_forbidden": True,
            "adjacent_same_content_fingerprint_forbidden": True,
            "repeat_page_to_fill_duration_forbidden": True,
            "internal_phases_min_when_extending": 3,
            "same_family_changed_dimensions_min": 2,
            "same_family_slow_variant_multiplier_range": [1.25, 1.60],
            "engine_selection_peer_level": True,
            "engine_selection_criteria": ["semantic_accuracy", "hierarchy_clarity", "subject_safety", "render_stability", "visual_impact"],
            "near_tie_prefer": "hyperframes",
            "video_shotcraft_pass_required": True,
            "candidate_sources": ["video-shotcraft", "rve", "scenes", "curvable", "playground", "hyperframes", "remotion"],
            "motion_coverage_for_media_gaps_required": True,
            "motion_families_per_chapter_short_min": 2,
            "motion_families_per_chapter_over_60s_min": 3,
        },
        "media_policy": {
            "image_duration_seconds": [5, 10],
            "adjacent_same_master_forbidden": True,
            "video_loop_to_fill_forbidden": True,
            "asset_assignment_mode": "user_verified_manifest_locked",
            "reassess_locked_asset_match": False,
            "image_default_treatment": "image_fullscreen_clear_local_text_glass",
            "non_16_9_treatment": "image_fullscreen_contain_solid_matte",
            "evidence_material_classes": ["archive_evidence", "book_evidence"],
            "historical_treatment": "historical_evidence_split_title_source_plus_large_image",
            "evidence_bilingual": ["zh-CN", "en"],
            "dynamic_reasoning_forbidden_over_evidence": True,
            "media_body_blur_px": 0,
            "media_text_overlay_engine": "selected_per_scene",
            "video_duration_policy": "natural_full_if_at_least_5_else_hold_last_frame_to_5",
            "video_max_duration_seconds": None,
            "video_muted": True,
            "provenance_labels_on_canvas": False,
        },
        "argument_bridge_policy": {
            "engine": "hyperframes",
            "target_ratio": [0.04, 0.06],
            "hard_max_ratio": 0.06,
            "max_per_chapter": 1,
            "adjacent_forbidden": True,
            "right_item_count_range": [2, 4],
            "left_font_px_min": 88,
            "right_font_px_min": 48,
            "same_semantic_segment_required": True,
            "only_when_media_or_concrete_diagram_insufficient": True,
        },
        "visual_system": {
            "theme": "Soft Signal",
            "design_language": "Apple-inspired warmth",
            "default_material": "glass_regular",
            "default_background_visibility": "faint",
            "contrast_ratio_target": 4.5,
            "subtitle_exclusion_bottom_px": 220,
            "font_px": {
                "chapter": [156, 220],
                "conclusion": [104, 148],
                "body": [42, 54],
                "support_min": 32,
                "source_meta_min": 26,
            },
        },
        "scenes": [],
    }
    write_if_missing(root / "04_spec" / "video-spec.json", json.dumps(spec, ensure_ascii=False, indent=2) + "\n", created, skipped)
    animation_plan = {
        "project": args.name,
        "version": "V1",
        "catalog_revision": catalog_revision,
        "selection_policy": "source-led Shotcraft pass; peer Remotion/HyperFrames candidate comparison with no engine quota",
        "programmatic_default": "peer-remotion-hyperframes-near-tie-hyperframes",
        "engine_policy": {
            "remotion_master_timeline": True,
            "engine_usage_quota_enforced": False,
            "opening_and_closing_presenter_overlays": "selected_per_scene",
            "engine_selection_peer_level": True,
            "engine_selection_criteria": ["semantic_accuracy", "hierarchy_clarity", "subject_safety", "render_stability", "visual_impact"],
            "near_tie_prefer": "hyperframes",
            "video_shotcraft_pass_required": True,
            "adjacent_identical_signature_forbidden": True,
            "adjacent_same_visual_page_forbidden": True,
            "repeat_page_to_fill_duration_forbidden": True,
        },
        "scenes": [],
    }
    write_if_missing(
        root / "04_spec" / "animation-plan.json",
        json.dumps(animation_plan, ensure_ascii=False, indent=2) + "\n",
        created,
        skipped,
    )
    hyperframes_qa = {
        "project": args.name,
        "version": "V1",
        "lint": "PENDING",
        "validate": "PENDING",
        "inspect": "PENDING",
        "animation_map": "PENDING",
        "notes": [],
    }
    write_if_missing(
        root / "07_hyperframes" / "qa" / "hyperframes-qa.json",
        json.dumps(hyperframes_qa, ensure_ascii=False, indent=2) + "\n",
        created,
        skipped,
    )
    asset_requirements = {
        "project": args.name,
        "version": "V1",
        "real_image_requests": [],
        "ai_image_requests": [],
        "ai_video_requests": [],
        "real_video_requests": [],
        "coverage_policy": {
            "ai_image_count_cap": None,
            "ai_video_count_cap": 250,
            "ai_video_duration_seconds_range": [5, 15],
            "expected_ai_image_use_count": 1,
            "required_variant_roles": ["primary", "detail", "transition", "backup"],
            "planned_image_seconds": 0,
            "requested_image_coverage_seconds": 0,
            "unresolved_gap_seconds": 0,
            "required_segments_must_have_primary_and_backup_or_programmatic_fallback": True,
        },
    }
    write_if_missing(
        root / "04_spec" / "asset-requirements.json",
        json.dumps(asset_requirements, ensure_ascii=False, indent=2) + "\n",
        created,
        skipped,
    )
    presenter_plan = {
        "project": args.name,
        "version": "V1",
        "source_audio": "",
        "recording_protocol": {
            "head_silence_seconds": 5,
            "tail_silence_seconds": 5,
            "start_signal": "double_beep",
            "end_signal": "double_beep",
            "source_capture": "16:9_fullscreen_centered_circle_crop_safe",
            "final_pip_shape": "circle",
            "final_pip_diameter_px": 360,
            "final_pip_default_anchor": "lower-right-raised",
            "final_pip_alternate_requires_user_approval": True,
            "subtitle_exclusion_bottom_px": 220,
            "opening_fullscreen_max_seconds": 15.0,
            "closing_fullscreen_summary": True,
        },
        "segments": [],
    }
    write_if_missing(
        root / "05_assets" / "presenter" / "presenter-plan.json",
        json.dumps(presenter_plan, ensure_ascii=False, indent=2) + "\n",
        created,
        skipped,
    )
    write_if_missing(root / "06_remotion" / "src" / "theme-soft-signal.ts", THEME_TS, created, skipped)
    write_if_missing(
        root / "source-manifest.csv",
        "id,manifest_order,type,material_class,assigned_asset_path,assigned_script_segment_id,user_verified,assignment_locked,assignment_reassessed,source,author,license,downloaded_at,nature,source_aspect_ratio,source_duration_seconds,status,notes\n",
        created,
        skipped,
    )

    print(json.dumps({"project_root": str(root), "created": created, "preserved": skipped}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
