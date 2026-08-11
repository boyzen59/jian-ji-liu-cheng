#!/usr/bin/env python3
"""Query and shortlist the unified Remotion catalog from a script beat."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = SKILL_ROOT / "assets" / "remotion-library" / "catalog.json"

INTENT_TERMS: dict[str, tuple[str, ...]] = {
    "explain": ("为什么", "因为", "所以", "如何", "原理", "机制", "步骤", "流程", "导致", "结果", "归成", "归类", "分类", "explain", "because", "how", "process"),
    "focus": ("最重要", "关键", "重点", "注意", "核心", "唯一", "记住", "聚焦", "紧急", "真正改变", "推到面前", "focus", "key", "important", "only", "urgent"),
    "compare": ("相比", "对比", "不同", "区别", "之前", "之后", "一方面", "另一方面", "versus", "compare", "before", "after"),
    "relate": ("关系", "连接", "关联", "之间", "路径", "阶段", "时间线", "从而", "先把", "再把", "归类", "分类", "relation", "connect", "timeline", "between"),
    "quantify": ("数据", "数字", "数量", "比例", "百分比", "增长", "下降", "排名", "统计", "倍", "封邮件", "三类", "二十七", "data", "percent", "metric", "growth", "rank"),
    "demonstrate": ("点击", "输入", "拖动", "打开", "关闭", "操作", "界面", "演示", "使用", "click", "type", "drag", "scroll", "demo"),
    "transition": ("但是", "然而", "接下来", "转折", "换句话说", "另一方面", "最终", "回到", "however", "next", "finally", "meanwhile"),
    "identity": ("开场", "章节", "标题", "品牌", "名字", "结尾", "总结", "行动", "intro", "chapter", "title", "brand", "outro"),
    "rhythm": ("连续", "逐个", "依次", "先", "再", "节奏", "加速", "倒计时", "重复", "beat", "rhythm", "stagger", "countdown"),
    "atmosphere": ("氛围", "温暖", "亲密", "安静", "悬念", "情绪", "背景", "呼吸感", "atmosphere", "mood", "ambient", "warm"),
    "delight": ("惊喜", "趣味", "轻松", "庆祝", "活泼", "可爱", "delight", "playful", "celebrate", "fun"),
}

RUNTIME_BONUS = {
    "component_library": 2.0,
    "copy_and_adapt": 1.5,
    "project_source": 1.0,
    "recipe_and_demo": 1.0,
    "legacy_reference": -4.0,
}

CONCEPT_BRIDGES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "分类/列表": (
        ("分类", "归类", "分组", "列表", "清单", "类目", "三类", "sort", "classify", "group"),
        ("list", "grid", "stack", "filter", "ranking", "category", "sort", "step"),
    ),
    "重点/优先级": (
        ("聚焦", "紧急", "优先", "最重要", "关键", "核心", "唯一", "priority", "urgent", "focus"),
        ("focus", "spotlight", "hero", "highlight", "priority", "attention", "selected"),
    ),
    "比较": (
        ("对比", "相比", "不同", "差异", "以前", "现在", "前后", "compare", "versus", "before", "after"),
        ("comparison", "compare", "before-after", "slider", "split", "versus"),
    ),
    "数值": (
        ("数据", "数字", "数量", "比例", "百分比", "增长", "下降", "排名", "统计", "封邮件", "metric", "percent"),
        ("chart", "counter", "stat", "metric", "gauge", "progress", "ranking", "number", "data"),
    ),
    "流程/关系": (
        ("步骤", "流程", "阶段", "先", "再", "然后", "导致", "关系", "连接", "process", "step", "flow"),
        ("timeline", "step", "flow", "diagram", "cascade", "map", "line", "path", "connect", "progress"),
    ),
    "文档/消息": (
        ("邮件", "信", "消息", "通知", "文档", "回复", "email", "message", "document", "notification"),
        ("notification", "document", "stream-response", "list", "stack", "input", "inbox", "message"),
    ),
}


def load_catalog(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def infer_intents(text: str) -> list[str]:
    lowered = text.lower()
    intents = [intent for intent, terms in INTENT_TERMS.items() if any(term in lowered for term in terms)]
    return intents or ["explain"]


def english_tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", value.lower()) if len(token) > 1}


def keyword_score(query: str, entry: dict[str, Any]) -> tuple[float, list[str]]:
    if not query.strip():
        return 0.0, []
    q_lower = query.lower()
    q_tokens = english_tokens(query)
    reasons: list[str] = []
    score = 0.0
    weighted_fields = [
        ("title", 6.0), ("name", 6.0), ("category", 4.0), ("tags", 4.0),
        ("semantic_roles", 5.0), ("description", 2.5), ("use", 2.5), ("intention", 2.0),
    ]
    for field, weight in weighted_fields:
        value = entry.get(field, "")
        haystack = " ".join(map(str, value)) if isinstance(value, list) else str(value)
        lowered = haystack.lower()
        token_hits = len(q_tokens & english_tokens(haystack))
        substring_hit = bool(q_lower and len(q_lower) >= 2 and q_lower in lowered)
        if token_hits or substring_hit:
            gain = min(weight * (2 if substring_hit else 1), weight + token_hits * 1.5)
            score += gain
            reasons.append(f"{field}匹配")
    return score, reasons


def concept_score(query: str, entry: dict[str, Any]) -> tuple[float, list[str]]:
    lowered_query = query.lower()
    entry_blob = " ".join(
        str(value) if not isinstance(value, list) else " ".join(map(str, value))
        for value in [entry.get("id", ""), entry.get("title", ""), entry.get("name", ""), entry.get("category", ""), entry.get("tags", [])]
    ).lower()
    score = 0.0
    reasons: list[str] = []

    def entry_has(term: str) -> bool:
        if re.fullmatch(r"[a-z0-9-]+", term):
            return bool(re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", entry_blob))
        return term in entry_blob

    for label, (query_terms, entry_terms) in CONCEPT_BRIDGES.items():
        if any(term in lowered_query for term in query_terms) and any(entry_has(term) for term in entry_terms):
            score += 6.0
            reasons.append(f"概念桥={label}")
    return score, reasons


def score_entry(
    entry: dict[str, Any], *, query: str, intents: list[str], energy: str | None,
    layer: str | None, source: str | None, ambient: bool,
) -> tuple[float, list[str]]:
    if source and entry["source"] != source:
        return -999.0, ["来源不匹配"]
    reasons: list[str] = []
    score, keyword_reasons = keyword_score(query, entry)
    reasons.extend(keyword_reasons)
    bridge_score, bridge_reasons = concept_score(query, entry)
    score += bridge_score
    reasons.extend(bridge_reasons)
    matched_intents = sorted(set(intents) & set(entry.get("semantic_roles", [])))
    score += 7.0 * len(matched_intents)
    if matched_intents:
        reasons.append("意图=" + ",".join(matched_intents))
    desired_layer = layer or ("ambient" if ambient else "primary")
    if desired_layer in entry.get("layer_fit", []):
        score += 5.0
        reasons.append(f"适合{desired_layer}层")
    elif ambient:
        return -999.0, ["不适合ambient层"]
    elif not ambient and "support" in entry.get("layer_fit", []):
        score += 1.0
    else:
        score -= 3.0
    experience = set(entry.get("experience_roles", []))
    if ambient:
        if experience:
            score += 5.0
            reasons.append("具备视觉体验=" + ",".join(sorted(experience)))
        else:
            score -= 4.0
    elif set(intents).issubset({"atmosphere", "delight", "rhythm"}) and experience:
        score += 2.0
    if energy:
        if entry.get("energy") == energy:
            score += 3.0
            reasons.append(f"能量={energy}")
        else:
            score -= 1.0
    score += RUNTIME_BONUS.get(entry.get("runtime_status", ""), 0.0)
    if entry.get("preview_status") == "offline" or entry.get("preview_path"):
        score += 1.0
        reasons.append("有离线预览")
    return score, reasons


def ranked(
    entries: list[dict[str, Any]], *, query: str, intents: list[str], energy: str | None,
    layer: str | None, source: str | None, ambient: bool, limit: int,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for entry in entries:
        score, reasons = score_entry(
            entry, query=query, intents=intents, energy=energy, layer=layer, source=source, ambient=ambient
        )
        if score <= -900:
            continue
        item = {
            "id": entry["id"],
            "score": round(score, 2),
            "source": entry["source"],
            "title": entry["title"],
            "category": entry["category"],
            "semantic_roles": entry.get("semantic_roles", []),
            "experience_roles": entry.get("experience_roles", []),
            "layer_fit": entry.get("layer_fit", []),
            "energy": entry.get("energy"),
            "runtime_status": entry.get("runtime_status"),
            "source_path": entry.get("source_path"),
            "source_path_from_skill_root": f"assets/remotion-library/{entry.get('source_path')}",
            "preview_path": entry.get("preview_path"),
            "preview_path_from_skill_root": (
                f"assets/remotion-library/{entry.get('preview_path')}" if entry.get("preview_path") else None
            ),
            "demo_paths": entry.get("demo_paths", []),
            "demo_paths_from_skill_root": [f"assets/remotion-library/{path}" for path in entry.get("demo_paths", [])],
            "why_shortlisted": reasons[:6],
        }
        results.append(item)
    return sorted(results, key=lambda item: (-item["score"], item["id"]))[:limit]


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Search or shortlist the unified Remotion library.")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("stats")

    show = sub.add_parser("show")
    show.add_argument("id")

    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--source", choices=["video-shotcraft", "rve", "scenes", "curvable", "playground"])
    search.add_argument("--layer", choices=["primary", "support", "ambient"])
    search.add_argument("--energy", choices=["low", "medium", "high"])
    search.add_argument("--limit", type=int, default=10)

    suggest = sub.add_parser("suggest")
    suggest.add_argument("--text", required=True, help="The exact script beat or on-screen copy")
    suggest.add_argument("--task", default="", help="Scene task such as compare, explain, turn, or chapter")
    suggest.add_argument("--energy", choices=["low", "medium", "high"])
    suggest.add_argument("--source", choices=["video-shotcraft", "rve", "scenes", "curvable", "playground"])
    suggest.add_argument("--limit", type=int, default=5)
    suggest.add_argument("--no-ambient", action="store_true")

    args = parser.parse_args()
    catalog = load_catalog(args.catalog.expanduser().resolve())
    entries = catalog["entries"]

    if args.command == "stats":
        print_json({
            "catalog_revision": catalog["catalog_revision"],
            "entry_count": catalog["entry_count"],
            "inventory": catalog["inventory"],
        })
        return 0
    if args.command == "show":
        match = next((entry for entry in entries if entry["id"] == args.id), None)
        if match is None:
            parser.error(f"unknown catalog id: {args.id}")
        shown = dict(match)
        shown["source_path_from_skill_root"] = f"assets/remotion-library/{match.get('source_path')}"
        shown["preview_path_from_skill_root"] = (
            f"assets/remotion-library/{match.get('preview_path')}" if match.get("preview_path") else None
        )
        shown["demo_paths_from_skill_root"] = [
            f"assets/remotion-library/{path}" for path in match.get("demo_paths", [])
        ]
        print_json(shown)
        return 0
    if args.command == "search":
        intents = infer_intents(args.query)
        print_json({
            "query": args.query,
            "inferred_intents": intents,
            "results": ranked(
                entries, query=args.query, intents=intents, energy=args.energy, layer=args.layer,
                source=args.source, ambient=args.layer == "ambient", limit=max(1, args.limit),
            ),
        })
        return 0

    query = f"{args.task} {args.text}".strip()
    intents = infer_intents(query)
    result = {
        "catalog_revision": catalog["catalog_revision"],
        "script_text": args.text,
        "scene_task": args.task,
        "inferred_intents": intents,
        "primary_candidates": ranked(
            entries, query=query, intents=intents, energy=args.energy, layer="primary",
            source=args.source, ambient=False, limit=max(1, args.limit),
        ),
        "ambient_candidates": [],
            "selection_note": "候选只是短名单；primary_candidates 指主选条目，不等于 catalog 的 layer_fit 必须为 primary，转场/接力类 support 条目可成为主选动作。所有路径均提供相对 Skill 根目录版本；最终选择前必须完整读取源文件、预览并完成主体保护检查。",
    }
    if not args.no_ambient:
        result["ambient_candidates"] = ranked(
            entries, query=query, intents=intents, energy=args.energy, layer="ambient",
            source=args.source, ambient=True, limit=max(1, args.limit),
        )
    print_json(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
