#!/usr/bin/env python3
"""Create exact presenter reference clips and 5-second-silence beep guides."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


SAMPLE_RATE = 48000
SILENCE_SECONDS = 5.0
BEEP_SECONDS = 0.12
BEEP_GAP_SECONDS = 0.12
BEEP_FREQUENCY = 1000


def parse_timecode(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    parts = str(value).replace(",", ".").split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        return float(parts[0])
    except (ValueError, IndexError) as exc:
        raise ValueError(f"invalid timecode: {value}") from exc


def resolve_binary(value: str | None, name: str) -> str:
    if value:
        path = Path(value).expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"{name} not found: {path}")
        return str(path)
    found = shutil.which(name)
    if not found:
        raise SystemExit(
            f"{name} is required but is not on PATH. Install FFmpeg or pass --{name} with an explicit path."
        )
    return found


def resolve_ffprobe(value: str | None, ffmpeg: str) -> str:
    if value:
        return resolve_binary(value, "ffprobe")
    sibling = Path(ffmpeg).with_name("ffprobe.exe" if Path(ffmpeg).suffix.lower() == ".exe" else "ffprobe")
    if sibling.is_file():
        return str(sibling)
    return resolve_binary(None, "ffprobe")


def run(command: list[str]) -> None:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise SystemExit(f"FFmpeg failed:\n{detail}")


def probe_duration(ffprobe: str, path: Path) -> float:
    completed = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(f"ffprobe failed for {path}: {completed.stderr.strip()}")
    try:
        return float(completed.stdout.strip())
    except ValueError as exc:
        raise SystemExit(f"ffprobe returned an invalid duration for {path}: {completed.stdout!r}") from exc


def resolve_source(root: Path, value: str) -> Path:
    source = Path(value).expanduser()
    if not source.is_absolute():
        source = root / source
    source = source.resolve()
    if not source.is_file():
        raise SystemExit(f"Source audio not found: {source}")
    return source


def exact_filter(start: float, end: float) -> str:
    return (
        f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS,"
        f"aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:sample_rates={SAMPLE_RATE}:"
        "channel_layouts=stereo[out]"
    )


def guide_filter(start: float, end: float) -> str:
    silence = f"anullsrc=channel_layout=stereo:sample_rate={SAMPLE_RATE}"
    beep = (
        f"sine=frequency={BEEP_FREQUENCY}:sample_rate={SAMPLE_RATE}:duration={BEEP_SECONDS},"
        "volume=0.35,pan=stereo|c0=c0|c1=c0"
    )
    voice = (
        f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS,"
        f"aresample={SAMPLE_RATE},aformat=sample_fmts=fltp:sample_rates={SAMPLE_RATE}:"
        "channel_layouts=stereo[voice]"
    )
    return ";".join([
        f"{silence}:duration={SILENCE_SECONDS}[pre]",
        f"{beep}[b1]",
        f"{silence}:duration={BEEP_GAP_SECONDS}[gap1]",
        f"{beep}[b2]",
        voice,
        f"{beep}[b3]",
        f"{silence}:duration={BEEP_GAP_SECONDS}[gap2]",
        f"{beep}[b4]",
        f"{silence}:duration={SILENCE_SECONDS}[post]",
        "[pre][b1][gap1][b2][voice][b3][gap2][b4][post]concat=n=9:v=0:a=1[out]",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description="Build presenter exact and 5s-silence beep guide WAV files.")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--ffmpeg", help="Explicit ffmpeg executable path")
    parser.add_argument("--ffprobe", help="Explicit ffprobe executable path")
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()
    plan_path = root / "05_assets" / "presenter" / "presenter-plan.json"
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing presenter plan: {plan_path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid presenter plan: {exc}") from exc

    ffmpeg = resolve_binary(args.ffmpeg, "ffmpeg")
    ffprobe = resolve_ffprobe(args.ffprobe, ffmpeg)
    source = resolve_source(root, str(plan.get("source_audio", "")))
    rows = plan.get("segments", [])
    if not rows:
        raise SystemExit("presenter-plan segments must not be empty")
    exact_dir = root / "05_assets" / "audio" / "exact"
    guide_dir = root / "05_assets" / "audio" / "guide"
    exact_dir.mkdir(parents=True, exist_ok=True)
    guide_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        clip_id = str(row.get("id", "")).strip()
        if not clip_id or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in clip_id):
            raise SystemExit(f"Invalid presenter segment id: {clip_id!r}")
        if clip_id in seen:
            raise SystemExit(f"Duplicate presenter segment id: {clip_id}")
        seen.add(clip_id)
        try:
            start = parse_timecode(row.get("start"))
            end = parse_timecode(row.get("end"))
        except ValueError as exc:
            raise SystemExit(f"{clip_id}: {exc}") from exc
        if start < 0 or end <= start:
            raise SystemExit(f"{clip_id}: end must be after non-negative start")
        exact = exact_dir / f"{clip_id}_exact.wav"
        guide = guide_dir / f"{clip_id}_5s-beep-guide.wav"
        run([
            ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
            "-filter_complex", exact_filter(start, end), "-map", "[out]", "-c:a", "pcm_s24le", str(exact),
        ])
        run([
            ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
            "-filter_complex", guide_filter(start, end), "-map", "[out]", "-c:a", "pcm_s24le", str(guide),
        ])
        voice_duration = end - start
        double_beep_duration = BEEP_SECONDS * 2 + BEEP_GAP_SECONDS
        expected_guide_duration = voice_duration + SILENCE_SECONDS * 2 + double_beep_duration * 2
        exact_actual = probe_duration(ffprobe, exact)
        guide_actual = probe_duration(ffprobe, guide)
        if abs(exact_actual - voice_duration) > 0.03:
            raise SystemExit(
                f"{clip_id}: exact clip duration mismatch; expected {voice_duration:.3f}s, got {exact_actual:.3f}s"
            )
        if abs(guide_actual - expected_guide_duration) > 0.03:
            raise SystemExit(
                f"{clip_id}: guide duration mismatch; expected {expected_guide_duration:.3f}s, got {guide_actual:.3f}s"
            )
        manifest_rows.append({
            "id": clip_id,
            "source_start": start,
            "source_end": end,
            "voice_duration_seconds": voice_duration,
            "exact_file": str(exact),
            "guide_file": str(guide),
            "guide_head_silence_seconds": SILENCE_SECONDS,
            "guide_speech_starts_at_seconds": SILENCE_SECONDS + double_beep_duration,
            "guide_tail_silence_seconds": SILENCE_SECONDS,
            "exact_actual_duration_seconds": exact_actual,
            "guide_expected_duration_seconds": expected_guide_duration,
            "guide_actual_duration_seconds": guide_actual,
            "signals": "double 1000Hz beep before and after speech",
        })

    manifest = {
        "project": plan.get("project", ""),
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_audio": str(source),
        "sample_rate": SAMPLE_RATE,
        "codec": "pcm_s24le",
        "segments": manifest_rows,
    }
    manifest_path = root / "05_assets" / "audio" / "presenter-audio-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "segments": len(manifest_rows)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
