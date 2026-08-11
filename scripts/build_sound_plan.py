#!/usr/bin/env python3
"""Generate a deterministic six-bus sound cue plan from video-spec JSON."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def now_local() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_tc(value: str) -> float:
    parts = str(value).replace(",", ".").split(":")
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = "0", parts[0], parts[1]
    else:
        return float(parts[0])
    return int(h) * 3600 + int(m) * 60 + float(s)


def format_tc(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


FOLEY_RULES = [
    (re.compile(r"click|tap|switch|点击|开关", re.I), "click", "真实点击/开关", "真实点击 开关 音效", "real click switch foley"),
    (re.compile(r"page|flip|paper|book|翻页|纸张|书页", re.I), "page_flip", "翻页/纸张", "真实翻页 纸张 音效", "realistic page flip paper foley"),
    (re.compile(r"card|land|stamp|drop|落位|卡片|盖章", re.I), "card_land", "卡片落位", "卡片落位 轻撞击 音效", "card settle soft impact foley"),
    (re.compile(r"number|counter|count|数字|计数|跳动", re.I), "counter_tick", "数字跳动", "计数器 数字跳动 音效", "counter tick number increment foley"),
    (re.compile(r"draw|write|underline|trace|书写|画线|下划线", re.I), "draw_write", "书写/描线", "铅笔 记号笔 书写 音效", "pencil marker writing foley"),
]


def add_cue(cues: list[dict], scene: dict, bus: str, trigger: str, action: str,
            at: float, search_cn: str = "", search_en: str = "", notes: str = "") -> None:
    cues.append({
        "id": f"CUE-{len(cues) + 1:04d}",
        "scene_id": scene.get("id", ""),
        "timecode": format_tc(at),
        "relative_to": f"SHOTS.{scene.get('id', 'UNKNOWN')}.from + offset",
        "bus": bus,
        "trigger": trigger,
        "action": action,
        "search_cn": search_cn,
        "search_en": search_en,
        "source": "[待选择]",
        "license": "[待记录]",
        "gain_db": None,
        "duration_frames": None,
        "status": "PLANNED",
        "notes": notes,
    })


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a sound plan from video-spec JSON.")
    parser.add_argument("input_spec", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    spec = json.loads(args.input_spec.read_text(encoding="utf-8-sig"))
    scenes = spec.get("scenes", [])
    if not isinstance(scenes, list):
        raise SystemExit("video-spec scenes must be a list")

    cues: list[dict] = []
    previous_space = None
    for scene in scenes:
        start = parse_tc(scene.get("start", "0"))
        end = parse_tc(scene.get("end", scene.get("start", "0")))
        if end <= start:
            raise SystemExit(f"scene {scene.get('id', '?')} has invalid start/end")
        duration = end - start
        importance = int(scene.get("importance", 1) or 1)
        space = str(scene.get("space", "")).strip()
        transition = str(scene.get("transition_in", "hard_cut")).lower()
        motion = " ".join(map(str, scene.get("motion", []) if isinstance(scene.get("motion", []), list) else [scene.get("motion", "")]))
        emotion = str(scene.get("emotion", "neutral")).lower()
        scene_type = str(scene.get("scene_type", "")).lower()

        if scene_type == "chapter_title":
            add_cue(
                cues,
                scene,
                "TRANSITION",
                "chapter_title_emphasis",
                "强化全屏章节总览落定",
                start + min(duration * 0.58, 2.2),
                "温暖 克制 章节 标题 落定 提示音",
                "warm restrained chapter title settle impact",
                "每章只保留一个主落点；与人声字头、BGM重拍或其他SFX冲突时做减法。",
            )

        if space and space != previous_space:
            add_cue(cues, scene, "AMBIENCE", "space_enter", f"建立空间：{space}", start,
                    f"{space} 真实 环境音", f"{space} realistic room tone ambience",
                    f"轻铺并延续到空间变化，最长约 {duration:.2f}s 后按后续 Scene 判断续接。")
            previous_space = space

        if transition not in {"", "none", "hard_cut", "hard-cut"} and importance >= 2:
            add_cue(cues, scene, "TRANSITION", transition, "强化重要切换", start,
                    "克制 柔和 转场 音效", "subtle soft transition whoosh",
                    "长度贴可见转场；普通语义硬切不配音。")
        elif transition in {"hard_cut", "hard-cut"} and importance >= 3:
            add_cue(cues, scene, "TRANSITION", "semantic_impact", "重大语义硬切钉点", start,
                    "短促 深沉 冲击 音效", "short deep cinematic impact",
                    "仅重大转折；若 BGM 已有重拍则删除此 cue。")

        for pattern, trigger, action, cn, en in FOLEY_RULES:
            if pattern.search(motion):
                add_cue(cues, scene, "FOLEY", trigger, action, start + min(duration * 0.35, 1.2), cn, en,
                        "最终 offset 必须对齐可见动作帧。")

        if emotion in {"rise", "rising", "build", "上升", "蓄力"}:
            lead = min(max(duration * 0.5, 0.8), 2.5)
            add_cue(cues, scene, "EMOTION", "riser", "进入转折/高潮前铺垫", max(start, end - lead),
                    "克制 电影感 上升 音效", "subtle cinematic riser", "若下一落点不重要则删除。")
        elif emotion in {"climax", "impact", "高潮", "落点"}:
            add_cue(cues, scene, "EMOTION", "impact", "核心结论/证据落定", start + min(duration * 0.65, 2.0),
                    "温暖 深沉 电影冲击 音效", "warm deep cinematic impact", "全片峰值数量要克制。")
        elif emotion in {"resolution", "resolve", "收束", "余韵"}:
            add_cue(cues, scene, "EMOTION", "swell", "收束与余韵", start,
                    "温暖 柔和 情绪渐强 音效", "warm soft emotional swell", "保持在人声后方。")

    plan = {
        "schema_version": 1,
        "project": spec.get("project", ""),
        "source_spec": str(args.input_spec),
        "source_version": spec.get("version", ""),
        "generated_at": now_local(),
        "buses": ["VOICE", "BGM", "AMBIENCE", "TRANSITION", "FOLEY", "EMOTION"],
        "voice": {"pan": "center", "priority": "highest", "target": "clear_stable"},
        "music_sourcing": {
            "allowed_sources": ["ai_original_light_music", "youtube_studio_audio_library"],
            "ordinary_youtube_channels_allowed": False,
            "ai_required_metadata": ["platform", "model_version", "prompt", "generated_at", "sha256", "usage_rights"],
            "youtube_audio_library_required_metadata": [
                "track", "artist", "audio_library_page", "license_type",
                "attribution_required", "attribution_text", "downloaded_at", "allowed_use",
            ],
            "chapter_music_briefs": [],
            "selected_tracks": [],
        },
        "ducking": {
            "detector": "final_voice_activity",
            "pre_roll_ms": [80, 150],
            "attack_ms": [50, 100],
            "release_ms": [250, 500],
            "bgm_reduction_db": [6, 10],
            "dense_voice_max_reduction_db": 12,
            "ambience_reduction_db": [2, 4],
        },
        "mastering_start_point": {"sample_rate_hz": 48000, "integrated_lufs": [-16, -14], "true_peak_dbtp_max": -1.0},
        "delivery": {
            "video_master_audio_mode": "no_audio_stream",
            "sidecar_stems": ["voice.wav", "bgm.wav", "ambience.wav", "sfx.wav", "review_mix.wav"],
        },
        "cues": cues,
        "qa": {"headphones": "PENDING", "phone": "PENDING", "computer": "PENDING", "stale_cues": 0},
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output_json.resolve()), "scenes": len(scenes), "cues": len(cues)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
