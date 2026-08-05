#!/usr/bin/env python3
"""Validate a final SRT against the locked transcript, role manifest, and audio duration."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from rebuild_srt import normalized_chars, parse_srt, parse_transcript


def audio_duration_ms(path: Path) -> int:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return round(float(result.stdout.strip()) * 1000)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--srt", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--role-manifest", type=Path)
    parser.add_argument("--default-role", default="主讲人")
    parser.add_argument("--max-cps", type=float, default=22.0)
    args = parser.parse_args()

    entries = parse_srt(args.srt)
    script_lines = parse_transcript(args.transcript, args.default_role)
    expected = "".join(normalized_chars("".join(line.text for line in script_lines)))
    actual = "".join(normalized_chars("".join(text for _, _, text in entries)))
    errors: list[str] = []
    warnings: list[str] = []

    if actual != expected:
        errors.append(f"normalized subtitle text differs from transcript: {len(actual)} != {len(expected)} characters")

    for index, (start, end, text) in enumerate(entries, start=1):
        duration = (end - start) / 1000
        count = len(normalized_chars(text))
        cps = count / max(duration, 0.001)
        if cps > args.max_cps:
            warnings.append(f"cue {index}: {cps:.1f} chars/s")
        if duration < 0.35:
            warnings.append(f"cue {index}: short duration {duration:.3f}s")

    duration_ms = None
    if args.audio:
        duration_ms = audio_duration_ms(args.audio)
        if entries[-1][1] > duration_ms + 50:
            errors.append(f"final cue ends after audio: {entries[-1][1]} > {duration_ms} ms")

    role_counts: dict[str, int] = {}
    if args.role_manifest:
        manifest = json.loads(args.role_manifest.read_text(encoding="utf-8"))
        if len(manifest) != len(entries):
            errors.append(f"role manifest count differs: {len(manifest)} != {len(entries)}")
        else:
            for index, (cue, entry) in enumerate(zip(manifest, entries), start=1):
                start, end, text = entry
                if cue.get("index") != index:
                    errors.append(f"role manifest index mismatch at cue {index}")
                if cue.get("text") != text or cue.get("start_ms") != start or cue.get("end_ms") != end:
                    errors.append(f"role manifest content or timing mismatch at cue {index}")
                role = str(cue.get("role", ""))
                role_counts[role] = role_counts.get(role, 0) + 1

    report = {
        "status": "fail" if errors else "pass",
        "cue_count": len(entries),
        "first_start_ms": entries[0][0],
        "last_end_ms": entries[-1][1],
        "audio_duration_ms": duration_ms,
        "role_counts": role_counts,
        "warnings": warnings,
        "errors": errors,
        "note": "Structural validation does not replace required listening checkpoints.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
