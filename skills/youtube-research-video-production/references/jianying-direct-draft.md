# Direct Jianying draft editing

Use this workflow instead of desktop or GUI control.

## Resolve the draft

1. Read `root_meta_info.json` and locate the exact draft folder.
2. Match both folder path and `draft_id`. Do not rely on a display name alone.
3. Read `Timelines/project.json` to find the active timeline.
4. Use the root `draft_info.json` as the source and confirm its `draft_id` matches metadata.
5. Check for lock markers and confirm active-file modification times remain stable during staging. Stop if the draft is being edited.
6. Do not open, close, restart, or click Jianying as part of the operation.

## Back up before writing

Copy every file that may change into a timestamped backup outside the draft folder:

- Root `draft_info.json`, `.bak`, and template files
- Active `Timelines/<id>/draft_info.json`, `.bak`, and template files
- `draft_meta_info.json`
- `root_meta_info.json`

Record checksums and pre-edit track counts.

## Edit the decrypted structure

1. Decrypt the timeline and metadata with the verified local Jianying crypto utility.
2. Preserve unrelated materials, tracks, IDs, and media paths.
3. Remove only prior tracks created by the same automation group when rerunning.
4. Add visuals according to the final timeline map.
5. Add native text materials from the subtitle role manifest when speaker colors are required.
6. Keep source and target ranges inside the audio and project duration.
7. Do not rename the draft unless the user asks.

Default subtitle colors:

- `主讲人`: `#FFFFFF`
- `提问者`: `#4DD1FF`

Use one white track for a single speaker. For more roles, pass a JSON role-to-color map with `--role-colors`; unknown roles fall back to the narrator color.

Use a black outline or shadow for contrast. Keep subtitle position, size, and safe margin consistent across speakers.

## Write safely

1. Serialize and encrypt in a workspace staging directory.
2. Replace only the active main files atomically: root and active-timeline `draft_info.json` plus `template-2.tmp` when present.
3. Update draft metadata and the root index modification time.
4. Leave `.bak` and the small `template.tmp` untouched; they are recovery or template structures, not active main copies.
5. Keep all written active main copies byte-identical after writing.

For a subtitle-only operation, use the bundled script after completing acoustic QC:

```bash
python3 scripts/inject_jianying_subtitles.py \
  --draft-dir "/absolute/path/to/draft" \
  --manifest 08_subtitle_role_manifest.json \
  --crypto "/absolute/path/to/verified/jianying_crypto" \
  --work-dir "/workspace/staging" \
  --backup-dir "/workspace/backups/before-subtitles-YYYYMMDD-HHMMSS" \
  --root-index "/absolute/path/to/root_meta_info.json" \
  --report 10_jianying_placement_record.json
```

Run once with `--dry-run` before requesting write permission or changing the draft.

## Read back and verify

Decrypt the saved draft again. Confirm:

- Pre-existing video and audio segment counts remain unchanged unless the task required changes.
- Expected visual and text track counts exist.
- Subtitle cue count matches the final SRT and role manifest.
- Speaker color counts match role counts.
- Text segments are ordered and non-overlapping.
- Subtitle end is within audio and project duration.
- Every active timeline copy has the same checksum.
- All referenced local media paths exist.

Report the backup path and verification results. Do not report success after encryption alone.
