# Direct Jianying draft editing

Use this workflow instead of desktop or GUI control.

## Preserve the verified method

Use the last verified direct-draft workflow for this user's Jianying version and project layout when it still succeeds. Do not investigate or introduce a new import, relink, encryption, timeline, or media-assembly method as routine experimentation.

Switch methods only when:

- The verified method has produced a reproducible failure and the failure evidence is recorded; or
- The user explicitly asks to use another method.

Before switching, state what failed, show the relevant evidence, and name the replacement method. Do not experiment inside the live draft. Test any necessary replacement against a disposable copy or workspace staging artifact first.

## Align first, then insert separate tracks

Complete these steps before changing the Jianying draft:

1. Lock the final audio as the master clock.
2. Finish acoustic alignment of the exact subtitle text to that audio.
3. Finish the visual timeline against the same audio clock.
4. Verify that subtitle cues and visual ranges stay within the final audio/project duration.

Only after those checks pass, write the draft. Insert video/visuals and subtitles as separate track groups:

- Video/visual track: contains the picture program or individual visual segments, without burned-in subtitles.
- Subtitle track: contains native Jianying text materials, split into editable cues.
- Audio track: remains the timing master and must not be replaced or shifted during insertion unless the user explicitly asks.

Do not use a flattened video-with-subtitles as the Jianying assembly asset. Do not rely on Jianying's automatic subtitle recognition when an aligned manifest already exists. A review export may contain subtitles, but the editable draft must preserve the separate native subtitle track and the clean video/visual track.

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
4. Add the clean video/visual track according to the already aligned final timeline map.
5. Add native editable text materials from the already aligned subtitle manifest; use the role manifest when speaker colors are required.
6. Keep video/visual and text as separate track groups. Never burn or flatten subtitle text into the inserted video asset.
7. Keep source and target ranges inside the audio and project duration, without shifting the final-audio master.
8. Do not rename the draft unless the user asks.

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
- Video/visual segments and subtitle cues occupy separate track groups.
- The inserted video/visual asset has no burned-in duplicate subtitles.
- Subtitle cue count matches the final SRT and role manifest.
- Speaker color counts match role counts.
- Text segments are ordered and non-overlapping.
- Native subtitle materials remain individually editable after readback.
- Subtitle end is within audio and project duration.
- Every active timeline copy has the same checksum.
- All referenced local media paths exist.

Report the backup path and verification results. Do not report success after encryption alone.
