#!/usr/bin/env python3
"""Insert a role-colored native subtitle track into an encrypted Jianying draft."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path


DEFAULT_FONT = "/Applications/VideoFusion-macOS.app/Contents/Resources/Font/SystemFont/zh-hans.ttf"


def uid() -> str:
    return str(uuid.uuid4()).upper()


def dump_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def atomic_copy(source: Path, target: Path) -> None:
    temporary = target.with_name(target.name + ".codex-write-tmp")
    shutil.copy2(source, temporary)
    os.replace(temporary, target)


def decrypt(crypto: Path, source: Path, target: Path) -> dict:
    subprocess.run([str(crypto), "decrypt", str(source), str(target)], check=True)
    return json.loads(target.read_text(encoding="utf-8"))


def encrypt(crypto: Path, source: Path, target: Path) -> None:
    subprocess.run([str(crypto), "encrypt", str(source), str(target)], check=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def color_components(value: str) -> list[float]:
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Invalid color: {value!r}")
    return [int(value[index : index + 2], 16) / 255 for index in (0, 2, 4)]


def load_rows(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_rows = payload if isinstance(payload, list) else payload.get("subtitles")
    if not isinstance(raw_rows, list) or not raw_rows:
        raise ValueError("Subtitle manifest contains no rows")
    rows: list[dict[str, object]] = []
    for index, row in enumerate(raw_rows, start=1):
        if "start_ms" in row:
            start_ms, end_ms = int(row["start_ms"]), int(row["end_ms"])
        elif "start" in row:
            start_ms, end_ms = round(float(row["start"]) * 1000), round(float(row["end"]) * 1000)
        else:
            raise ValueError(f"Cue {index} has no timing")
        text = str(row.get("text", "")).strip()
        role = str(row.get("role", "主讲人")).strip() or "主讲人"
        if not text or end_ms <= start_ms:
            raise ValueError(f"Invalid cue {index}")
        if rows and start_ms < int(rows[-1]["end_ms"]):
            raise ValueError(f"Overlapping cue {index}")
        rows.append({"index": index, "role": role, "text": text, "start_ms": start_ms, "end_ms": end_ms})
    return rows


def text_material(
    row: dict[str, object],
    group_id: str,
    role_colors: dict[str, str],
    font: str,
    font_size: float,
) -> dict:
    text = str(row["text"])
    color_hex = role_colors.get(str(row["role"]), role_colors.get("主讲人", "#FFFFFF"))
    style = {
        "text": text,
        "styles": [
            {
                "size": font_size,
                "fill": {
                    "alpha": 1.0,
                    "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": color_components(color_hex)}},
                },
                "font": {"id": "", "path": font if Path(font).exists() else ""},
                "strokes": [
                    {
                        "width": 0.06,
                        "alpha": 1.0,
                        "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": [0.0, 0.0, 0.0]}},
                    }
                ],
                "range": [0, len(text)],
            }
        ],
    }
    content = json.dumps(style, ensure_ascii=False, separators=(",", ":"))
    duration_ms = int(row["end_ms"]) - int(row["start_ms"])
    char_duration = duration_ms / max(1, len(text))
    words = {
        "start_time": [round(index * char_duration) for index in range(len(text))],
        "end_time": [round((index + 1) * char_duration) for index in range(len(text))],
        "text": list(text),
    }
    return {
        "id": uid(),
        "recognize_task_id": group_id,
        "recognize_text": text,
        "recognize_model": "locked-transcript+acoustic-align",
        "type": "subtitle",
        "content": content,
        "base_content": content,
        "words": words,
        "current_words": {},
        "combo_info": {},
        "caption_template_info": {"resource_id": "", "path": ""},
        "layer_weight": 1,
        "line_spacing": 0.02,
        "shadow_alpha": 0.9,
        "shadow_smoothing": 0.45,
        "shadow_distance": 5.0,
        "shadow_point": {"x": 0.6363961031, "y": -0.6363961031},
        "shadow_angle": -45.0,
        "border_color": "#000000",
        "border_width": 0.08,
        "text_color": color_hex.upper(),
        "font_size": font_size,
        "font_path": font if Path(font).exists() else "",
        "initial_scale": 1.0,
        "add_type": 1,
        "group_id": group_id,
        "subtitle_keywords": {},
        "lyrics_template": {"resource_id": "", "path": ""},
    }


def text_segment(material_id: str, animation_id: str, row: dict[str, object], position_y: float) -> dict:
    return {
        "id": uid(),
        "target_timerange": {
            "start": int(row["start_ms"]) * 1000,
            "duration": (int(row["end_ms"]) - int(row["start_ms"])) * 1000,
        },
        "render_timerange": {},
        "clip": {
            "scale": {"x": 1.0, "y": 1.0},
            "transform": {"x": 0.0, "y": position_y},
            "flip": {},
        },
        "uniform_scale": {},
        "material_id": material_id,
        "extra_material_refs": [animation_id],
        "render_index": 14000,
        "enable_lut": False,
        "enable_adjust": False,
        "enable_hsl": False,
        "track_render_index": 1,
        "responsive_layout": {},
        "enable_adjust_mask": False,
        "source": "segmentsourcenormal",
    }


def active_timeline_files(draft: Path, timeline_dir: Path) -> list[Path]:
    names = ["draft_info.json", "template-2.tmp"]
    result = [path for base in (draft, timeline_dir) for name in names if (path := base / name).exists()]
    if draft / "draft_info.json" not in result:
        raise FileNotFoundError(draft / "draft_info.json")
    return result


def related_timeline_files(draft: Path, timeline_dir: Path) -> list[Path]:
    names = ["draft_info.json", "draft_info.json.bak", "template.tmp", "template-2.tmp"]
    return [path for base in (draft, timeline_dir) for name in names if (path := base / name).exists()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--crypto", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--backup-dir", type=Path, required=True)
    parser.add_argument("--root-index", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--track-name", default="口播字幕")
    parser.add_argument("--group-id", default="Auto_Codex_ResearchVideo_QA_Subtitles")
    parser.add_argument("--narrator-color", default="#FFFFFF")
    parser.add_argument("--questioner-color", default="#4DD1FF")
    parser.add_argument("--role-colors", type=Path, help="Optional JSON mapping arbitrary role names to hex colors")
    parser.add_argument("--font", default=DEFAULT_FONT)
    parser.add_argument("--font-size", type=float, default=8.0)
    parser.add_argument("--position-y", type=float, default=-0.70)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    draft = args.draft_dir.resolve()
    rows = load_rows(args.manifest)
    role_colors = {"主讲人": args.narrator_color.upper(), "提问者": args.questioner_color.upper()}
    if args.role_colors:
        role_colors.update(
            {str(role): str(color).upper() for role, color in json.loads(args.role_colors.read_text(encoding="utf-8")).items()}
        )
    project = json.loads((draft / "Timelines/project.json").read_text(encoding="utf-8"))
    timeline_dir = draft / "Timelines" / project["main_timeline_id"]
    timeline_targets = active_timeline_files(draft, timeline_dir)
    source = draft / "draft_info.json"
    lock_markers = [
        path
        for base in (draft, timeline_dir)
        for path in base.iterdir()
        if "lock" in path.name.lower() and path.is_file()
    ]
    if lock_markers:
        raise RuntimeError(f"Draft appears active or locked: {lock_markers}")
    initial_fingerprints = {path: (path.stat().st_mtime_ns, sha256(path)) for path in timeline_targets}

    args.work_dir.mkdir(parents=True, exist_ok=True)
    plain_timeline = args.work_dir / "timeline.before.json"
    plain_meta = args.work_dir / "meta.before.json"
    timeline = decrypt(args.crypto, source, plain_timeline)
    meta = decrypt(args.crypto, draft / "draft_meta_info.json", plain_meta)
    if str(meta.get("draft_fold_path", "")) and Path(meta["draft_fold_path"]).resolve() != draft:
        raise ValueError("draft_meta_info.json points to a different draft folder")

    before_counts = {
        kind: sum(len(track.get("segments", [])) for track in timeline["tracks"] if track.get("type") == kind)
        for kind in ("video", "audio", "text")
    }
    project_duration = int(timeline.get("duration", 0))
    last_end_us = int(rows[-1]["end_ms"]) * 1000
    if project_duration and last_end_us > project_duration:
        raise ValueError(f"Subtitle end {last_end_us} exceeds project duration {project_duration}")

    materials = timeline["materials"]
    materials.setdefault("texts", [])
    materials.setdefault("material_animations", [])
    old_ids = {
        item["id"]
        for item in materials["texts"]
        if item.get("group_id") == args.group_id or item.get("recognize_task_id") == args.group_id
    }
    old_animation_ids: set[str] = set()
    kept_tracks: list[dict] = []
    for track in timeline["tracks"]:
        kept_segments = []
        for segment in track.get("segments", []):
            if segment.get("material_id") in old_ids:
                old_animation_ids.update(segment.get("extra_material_refs", []))
            else:
                kept_segments.append(segment)
        if track.get("type") != "text" or kept_segments:
            if len(kept_segments) != len(track.get("segments", [])):
                track["segments"] = kept_segments
            kept_tracks.append(track)
    materials["texts"] = [item for item in materials["texts"] if item.get("id") not in old_ids]
    materials["material_animations"] = [
        item for item in materials["material_animations"] if item.get("id") not in old_animation_ids
    ]

    subtitle_segments: list[dict] = []
    for row in rows:
        material = text_material(
            row,
            args.group_id,
            role_colors,
            args.font,
            args.font_size,
        )
        animation_id = uid()
        materials["texts"].append(material)
        materials["material_animations"].append({"id": animation_id, "type": "sticker_animation"})
        subtitle_segments.append(text_segment(material["id"], animation_id, row, args.position_y))

    track_id = uid()
    subtitle_track = {
        "id": track_id,
        "type": "text",
        "name": args.track_name,
        "segments": subtitle_segments,
        "is_default_name": False,
    }
    audio_index = next((index for index, track in enumerate(kept_tracks) if track.get("type") == "audio"), len(kept_tracks))
    kept_tracks.insert(audio_index, subtitle_track)
    timeline["tracks"] = kept_tracks
    now_us = int(time.time() * 1_000_000)
    meta["tm_draft_modified"] = now_us

    after_counts = {
        kind: sum(len(track.get("segments", [])) for track in timeline["tracks"] if track.get("type") == kind)
        for kind in ("video", "audio", "text")
    }
    if after_counts["video"] != before_counts["video"] or after_counts["audio"] != before_counts["audio"]:
        raise RuntimeError("Subtitle insertion changed video or audio segment counts")

    report = {
        "status": "dry-run" if args.dry_run else "pending-write",
        "draft_dir": str(draft),
        "draft_id": meta.get("draft_id"),
        "source_timeline": str(source),
        "before_segment_counts": before_counts,
        "after_segment_counts": after_counts,
        "subtitle_track_id": track_id,
        "subtitle_cues": len(rows),
        "role_counts": {role: sum(1 for row in rows if row["role"] == role) for role in sorted({str(row["role"]) for row in rows})},
        "speaker_colors": {
            role: role_colors.get(role, role_colors["主讲人"])
            for role in sorted({str(row["role"]) for row in rows})
        },
        "subtitle_end_us": last_end_us,
        "project_duration_us": project_duration,
        "backup_dir": str(args.backup_dir),
    }
    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.backup_dir.exists():
        raise FileExistsError(f"Backup directory already exists: {args.backup_dir}")
    changed = [
        str(path)
        for path, fingerprint in initial_fingerprints.items()
        if (path.stat().st_mtime_ns, sha256(path)) != fingerprint
    ]
    if changed:
        raise RuntimeError(f"Draft changed during staging; stop instead of overwriting active work: {changed}")
    args.backup_dir.mkdir(parents=True)
    backup_targets = related_timeline_files(draft, timeline_dir) + [draft / "draft_meta_info.json"]
    if args.root_index:
        backup_targets.append(args.root_index)
    for target in dict.fromkeys(backup_targets):
        saved = args.backup_dir / ("root_meta_info.json" if args.root_index and target == args.root_index else target.relative_to(draft))
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, saved)

    final_timeline_plain = args.work_dir / "timeline.after.json"
    final_meta_plain = args.work_dir / "meta.after.json"
    final_timeline_encrypted = args.work_dir / "timeline.after.encrypted"
    final_meta_encrypted = args.work_dir / "meta.after.encrypted"
    dump_json(final_timeline_plain, timeline)
    dump_json(final_meta_plain, meta)
    encrypt(args.crypto, final_timeline_plain, final_timeline_encrypted)
    encrypt(args.crypto, final_meta_plain, final_meta_encrypted)
    for target in timeline_targets:
        atomic_copy(final_timeline_encrypted, target)
    atomic_copy(final_meta_encrypted, draft / "draft_meta_info.json")

    if args.root_index:
        root = json.loads(args.root_index.read_text(encoding="utf-8"))
        matching = [
            item
            for item in root.get("all_draft_store", [])
            if Path(item.get("draft_fold_path", "")).resolve() == draft and item.get("draft_id") == meta.get("draft_id")
        ]
        if len(matching) != 1:
            raise ValueError(f"Expected one root index match, found {len(matching)}")
        matching[0]["tm_draft_modified"] = now_us
        root_stage = args.work_dir / "root_meta_info.after.json"
        root_stage.write_text(json.dumps(root, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        atomic_copy(root_stage, args.root_index)

    verify_path = args.work_dir / "timeline.readback.json"
    verified = decrypt(args.crypto, draft / "draft_info.json", verify_path)
    verified_track = next(
        track for track in verified["tracks"] if track.get("id") == track_id and track.get("name") == args.track_name
    )
    if len(verified_track.get("segments", [])) != len(rows):
        raise RuntimeError("Readback subtitle cue count differs")
    hashes = {str(path): sha256(path) for path in timeline_targets}
    if len(set(hashes.values())) != 1:
        raise RuntimeError("Active timeline copies are not byte-identical after writing")

    report.update({"status": "pass", "timeline_hashes": hashes, "readback_subtitle_cues": len(verified_track["segments"])})
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
