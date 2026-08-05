#!/usr/bin/env python3
"""Rebuild exact subtitles from an ASR timing scaffold and a locked transcript."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from dataclasses import dataclass
from pathlib import Path


TIME_RE = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")
ROLE_RE = re.compile(r"^\s*【([^】]+)】\s*$")
DELIVERY_TAG_RE = re.compile(r"\[[A-Za-z][^\]\n]{0,48}\]\s*")


@dataclass(frozen=True)
class ScriptLine:
    role: str
    text: str


@dataclass(frozen=True)
class Chunk:
    role: str
    text: str
    start_index: int
    end_index: int


def parse_time(value: str) -> int:
    hours, minutes, rest = value.split(":")
    seconds, milliseconds = rest.split(",")
    return ((int(hours) * 60 + int(minutes)) * 60 + int(seconds)) * 1000 + int(milliseconds)


def format_time(value: float) -> str:
    value = max(0, round(value))
    milliseconds = value % 1000
    total_seconds = value // 1000
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    hours = total_minutes // 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def normalized_chars(value: str) -> list[str]:
    return [character.lower() for character in value if character.isalnum()]


def parse_transcript(path: Path, default_role: str) -> list[ScriptLine]:
    role = default_role
    lines: list[ScriptLine] = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        role_match = ROLE_RE.fullmatch(raw)
        if role_match:
            role = role_match.group(1).strip()
            continue
        text = DELIVERY_TAG_RE.sub("", raw).strip()
        if not text:
            continue
        lines.append(ScriptLine(role=role, text=text))
    if not lines:
        raise ValueError("Transcript contains no spoken text")
    return lines


def parse_srt(path: Path) -> list[tuple[int, int, str]]:
    entries: list[tuple[int, int, str]] = []
    raw = path.read_text(encoding="utf-8-sig").strip()
    for block in re.split(r"\n\s*\n", raw):
        lines = block.splitlines()
        timing_index = next((i for i, line in enumerate(lines) if TIME_RE.fullmatch(line.strip())), None)
        if timing_index is None:
            raise ValueError(f"Invalid SRT block without timing: {block!r}")
        match = TIME_RE.fullmatch(lines[timing_index].strip())
        assert match is not None
        text = "".join(lines[timing_index + 1 :]).strip()
        start, end = parse_time(match.group(1)), parse_time(match.group(2))
        if end <= start:
            raise ValueError(f"Non-positive source cue duration: {block!r}")
        if entries and start < entries[-1][1]:
            raise ValueError(f"Overlapping source cue: {block!r}")
        entries.append((start, end, text))
    if not entries:
        raise ValueError("Source SRT contains no cues")
    return entries


def source_character_timing(entries: list[tuple[int, int, str]]) -> tuple[str, list[float]]:
    characters: list[str] = []
    centers: list[float] = []
    for start, end, text in entries:
        cue_characters = normalized_chars(text)
        if not cue_characters:
            continue
        duration = max(1, end - start)
        for index, character in enumerate(cue_characters):
            characters.append(character)
            centers.append(start + (index + 0.5) * duration / len(cue_characters))
    if not characters:
        raise ValueError("Source SRT contains no alignable text")
    return "".join(characters), centers


def alignment_metrics(
    source: str,
    source_centers: list[float],
    target: str,
) -> tuple[difflib.SequenceMatcher, dict[str, float | int]]:
    matcher = difflib.SequenceMatcher(None, source, target, autojunk=False)
    blocks = [block for block in matcher.get_matching_blocks() if block.size]
    matched = sum(block.size for block in blocks)
    max_unmatched = 0
    max_unmatched_source = 0
    max_unanchored_ms = 0.0
    previous_target_end = 0
    previous_source_end = 0
    previous_center: float | None = None
    for block in blocks:
        max_unmatched = max(max_unmatched, block.b - previous_target_end)
        max_unmatched_source = max(max_unmatched_source, block.a - previous_source_end)
        if previous_center is not None and block.a < len(source_centers):
            max_unanchored_ms = max(max_unanchored_ms, source_centers[block.a] - previous_center)
        previous_target_end = block.b + block.size
        previous_source_end = block.a + block.size
        previous_center = source_centers[previous_source_end - 1]
    max_unmatched = max(max_unmatched, len(target) - previous_target_end)
    max_unmatched_source = max(max_unmatched_source, len(source) - previous_source_end)
    return matcher, {
        "similarity": matcher.ratio(),
        "target_anchor_coverage": matched / max(1, len(target)),
        "source_anchor_coverage": matched / max(1, len(source)),
        "matched_characters": matched,
        "target_characters": len(target),
        "source_characters": len(source),
        "max_unmatched_target_characters": max_unmatched,
        "max_unmatched_source_characters": max_unmatched_source,
        "max_unanchored_audio_ms": round(max_unanchored_ms),
    }


def enforce_alignment_thresholds(metrics: dict[str, float | int], args: argparse.Namespace) -> None:
    failures: list[str] = []
    if float(metrics["similarity"]) < args.min_alignment:
        failures.append(f"similarity {metrics['similarity']:.3f} < {args.min_alignment:.3f}")
    if float(metrics["target_anchor_coverage"]) < args.min_anchor_coverage:
        failures.append(
            f"target anchor coverage {metrics['target_anchor_coverage']:.3f} < "
            f"{args.min_anchor_coverage:.3f}"
        )
    if float(metrics["source_anchor_coverage"]) < args.min_source_anchor_coverage:
        failures.append(
            f"source anchor coverage {metrics['source_anchor_coverage']:.3f} < "
            f"{args.min_source_anchor_coverage:.3f}"
        )
    if int(metrics["max_unmatched_target_characters"]) > args.max_unmatched_chars:
        failures.append(
            f"longest unmatched transcript run {metrics['max_unmatched_target_characters']} > "
            f"{args.max_unmatched_chars} characters"
        )
    if int(metrics["max_unmatched_source_characters"]) > args.max_unmatched_source_chars:
        failures.append(
            f"longest unmatched ASR run {metrics['max_unmatched_source_characters']} > "
            f"{args.max_unmatched_source_chars} characters"
        )
    if int(metrics["max_unanchored_audio_ms"]) > args.max_unanchored_ms:
        failures.append(
            f"longest audio span without reliable text anchors {metrics['max_unanchored_audio_ms']} > "
            f"{args.max_unanchored_ms} ms"
        )
    if failures:
        raise ValueError(
            "Unsafe subtitle alignment; generate a better ASR scaffold or inspect the audio. "
            + "; ".join(failures)
        )


def target_timing(
    matcher: difflib.SequenceMatcher,
    source_centers: list[float],
    target_length: int,
) -> list[float]:
    centers: list[float | None] = [None] * target_length
    for source_start, target_start, size in matcher.get_matching_blocks():
        for offset in range(size):
            centers[target_start + offset] = source_centers[source_start + offset]

    matched = [index for index, value in enumerate(centers) if value is not None]
    if not matched:
        raise ValueError("No transcript alignment was found")

    average_step = (source_centers[-1] - source_centers[0]) / max(1, target_length - 1)
    first, last = matched[0], matched[-1]
    for index in range(first - 1, -1, -1):
        centers[index] = float(centers[index + 1]) - average_step
    for index in range(last + 1, len(centers)):
        centers[index] = float(centers[index - 1]) + average_step

    previous = first
    for following in matched[1:]:
        if following - previous > 1:
            start = float(centers[previous])
            end = float(centers[following])
            step = (end - start) / (following - previous)
            for index in range(previous + 1, following):
                centers[index] = start + step * (index - previous)
        previous = following

    result = [float(value) for value in centers]
    for index in range(1, len(result)):
        result[index] = max(result[index], result[index - 1] + 0.01)
    return result


def punctuation_pieces(line: str) -> list[str]:
    pieces: list[str] = []
    current = ""
    stripped = line.strip()
    for index, character in enumerate(stripped):
        current += character
        if character in "，。！？：；":
            if character == "，" and len(normalized_chars(current)) < 7:
                continue
            if index + 1 < len(stripped) and stripped[index + 1] in "”’」』":
                continue
            pieces.append(current)
            current = ""
    if current:
        pieces.append(current)
    return [piece for piece in pieces if normalized_chars(piece)]


def phrase_ranges(text: str, protected: set[str]) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for phrase in protected:
        normalized_phrase = "".join(normalized_chars(phrase))
        start = text.find(normalized_phrase)
        while normalized_phrase and start != -1:
            ranges.append((start, start + len(normalized_phrase)))
            start = text.find(normalized_phrase, start + 1)
    return ranges


def split_long_piece(piece: str, max_chars: int, protected: set[str]) -> list[str]:
    visible = normalized_chars(piece)
    if max_chars <= 0 or len(visible) <= max_chars:
        return [piece]

    raw_positions = [index for index, character in enumerate(piece) if character.isalnum()]
    visible_text = "".join(visible)
    ranges = phrase_ranges(visible_text, protected)
    parts: list[str] = []
    raw_start = 0
    visible_start = 0

    while len(visible) - visible_start > max_chars:
        remaining = len(visible) - visible_start
        minimum_tail = 4
        ideal = visible_start + max(8, max_chars - 3)
        lower = visible_start + max(6, max_chars // 2)
        upper = min(visible_start + max_chars, len(visible) - minimum_tail)
        if upper < lower:
            upper = min(visible_start + max_chars, len(visible) - 1)
            lower = max(visible_start + 1, upper - 2)
        candidates: list[tuple[int, int]] = []
        for boundary in range(lower, upper + 1):
            if any(start < boundary < end for start, end in ranges):
                continue
            left, right = visible[boundary - 1], visible[boundary]
            if left.isascii() and left.isalnum() and right.isascii() and right.isalnum():
                continue
            score = abs(boundary - ideal)
            if right in "的地得了着过和与或也又就则却但而被把是在会能":
                score += 5
            if left in "和与或把被在是会能可更很不没再还的":
                score += 5
            candidates.append((score, boundary))
        boundary = min(candidates)[1] if candidates else upper
        raw_end = raw_positions[boundary]
        parts.append(piece[raw_start:raw_end].strip())
        raw_start = raw_end
        visible_start = boundary
        if remaining <= max_chars:
            break
    parts.append(piece[raw_start:].strip())
    parts = [part for part in parts if normalized_chars(part)]
    if len(parts) > 1 and len(normalized_chars(parts[-1])) < 4:
        parts[-2] += parts[-1]
        parts.pop()
    return parts


def build_chunks(lines: list[ScriptLine], max_chars: int, protected: set[str]) -> list[Chunk]:
    chunks: list[Chunk] = []
    normalized_index = 0
    for line in lines:
        for piece in punctuation_pieces(line.text):
            for text in split_long_piece(piece, max_chars, protected):
                length = len(normalized_chars(text))
                chunks.append(
                    Chunk(
                        role=line.role,
                        text=text,
                        start_index=normalized_index,
                        end_index=normalized_index + length,
                    )
                )
                normalized_index += length
    if not chunks:
        raise ValueError("Approved transcript contains no text")
    return chunks


def load_glossary(path: Path | None) -> set[str]:
    if path is None:
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def rebuild(args: argparse.Namespace) -> None:
    entries = parse_srt(args.source_srt)
    source_text, source_centers = source_character_timing(entries)
    script_lines = parse_transcript(args.transcript, args.default_role)
    target_text = "".join(normalized_chars("".join(line.text for line in script_lines)))
    matcher, metrics = alignment_metrics(source_text, source_centers, target_text)
    enforce_alignment_thresholds(metrics, args)

    centers = target_timing(matcher, source_centers, len(target_text))
    boundaries = [float(entries[0][0])]
    boundaries.extend((centers[index - 1] + centers[index]) / 2 for index in range(1, len(centers)))
    boundaries.append(float(entries[-1][1]))

    protected = load_glossary(args.glossary)
    chunks = build_chunks(script_lines, args.max_chars, protected)
    if chunks[-1].end_index != len(target_text):
        raise ValueError(f"Chunking lost text: {chunks[-1].end_index} != {len(target_text)}")

    blocks: list[str] = []
    manifest: list[dict[str, object]] = []
    previous_end = -1.0
    reconstructed: list[str] = []
    for number, chunk in enumerate(chunks, start=1):
        start, end = boundaries[chunk.start_index], boundaries[chunk.end_index]
        if start < previous_end:
            raise ValueError(f"Overlap before cue {number}")
        if end <= start:
            raise ValueError(f"Non-positive duration in cue {number}")
        blocks.append(f"{number}\n{format_time(start)} --> {format_time(end)}\n{chunk.text}")
        manifest.append(
            {
                "index": number,
                "role": chunk.role,
                "text": chunk.text,
                "start_ms": round(start),
                "end_ms": round(end),
            }
        )
        reconstructed.extend(normalized_chars(chunk.text))
        previous_end = end

    if "".join(reconstructed) != target_text:
        raise ValueError("Output text does not exactly match the approved transcript")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    if args.role_manifest:
        args.role_manifest.parent.mkdir(parents=True, exist_ok=True)
        args.role_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = {
        **metrics,
        "source_cues": len(entries),
        "output_cues": len(chunks),
        "first_start_ms": round(boundaries[0]),
        "last_end_ms": round(boundaries[-1]),
        "roles": {role: sum(1 for cue in manifest if cue["role"] == role) for role in sorted({line.role for line in script_lines})},
        "output": str(args.output),
        "role_manifest": str(args.role_manifest) if args.role_manifest else None,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-srt", type=Path, required=True, help="ASR SRT from the final audio")
    parser.add_argument("--transcript", type=Path, required=True, help="Locked clean or role-tagged transcript")
    parser.add_argument("--output", type=Path, required=True, help="Corrected SRT output path")
    parser.add_argument("--glossary", type=Path, help="Optional UTF-8 file with one protected phrase per line")
    parser.add_argument("--role-manifest", type=Path, help="Optional JSON cue manifest for native Jianying styling")
    parser.add_argument("--report", type=Path, help="Optional JSON alignment report")
    parser.add_argument("--default-role", default="主讲人", help="Role for transcripts without role headings")
    parser.add_argument("--max-chars", type=int, default=18, help="Maximum alphanumeric characters per cue")
    parser.add_argument("--min-alignment", type=float, default=0.75, help="Minimum SequenceMatcher similarity")
    parser.add_argument("--min-anchor-coverage", type=float, default=0.75, help="Minimum matched target coverage")
    parser.add_argument("--min-source-anchor-coverage", type=float, default=0.75, help="Minimum matched ASR coverage")
    parser.add_argument("--max-unmatched-chars", type=int, default=32, help="Maximum unmatched target run")
    parser.add_argument("--max-unmatched-source-chars", type=int, default=32, help="Maximum unmatched ASR run")
    parser.add_argument("--max-unanchored-ms", type=int, default=4000, help="Maximum audio span without anchors")
    rebuild(parser.parse_args())


if __name__ == "__main__":
    main()
