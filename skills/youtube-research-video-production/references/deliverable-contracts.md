# Deliverable contracts

Use these filenames as defaults. Adapt them to an existing project without overwriting user files.

## Project structure

```text
video-project/
├── 01_topic_brief.md
├── 02_research_dossier.md
├── 03_script_final.txt
├── 03_script_performance.txt        # optional
├── 03_script_roles_tagged.txt       # optional for multiple speakers
├── 04_pronunciation_glossary.txt
├── 05_visual_manifest.md
├── assets/
│   ├── source-original/
│   ├── source-annotated/
│   ├── generated-scenes/
│   └── evidence/
├── 06_visual_master_no_text_no_audio.mp4
├── 06_voice_final.wav
├── 06_sfx_only.wav                  # optional; omit when no SFX are used
├── 06_bgm_only.wav                  # optional only when BGM is approved
├── 06_reference_publish_master.mp4  # optional viewing reference, not the editable source
├── 07_subtitles_asr_scaffold.srt
├── 08_subtitles_final.srt
├── 08_subtitle_role_manifest.json   # optional for role styling
├── 09_timeline_map.md
├── 10_nle_media_registry.json
├── 10_jianying_placement_record.md
├── 11_thumbnail.png
├── 12_upload_metadata.md
└── 13_publish_qc.md
```

## Gate A: Topic to research

Require in `01_topic_brief.md`:

- `GO` decision
- Main query and viewer question
- Current search evidence
- Concrete differentiated promise
- Primary-source and evidence leads
- Approved claim and forbidden overclaim
- Chosen title-thumbnail direction

## Gate B: Research to script

Require in `02_research_dossier.md`:

- Primary sources with locations, versions, dates, or data definitions
- Uncertainty, edition, measurement, or interpretation limits
- Current evidence linked and summarized
- Claim-evidence table with limits
- Facts and interpretations kept separate
- Available visuals and missing assets

## Gate C: Script lock

- Keep only spoken words in `03_script_final.txt`.
- Add sparse delivery tags in `03_script_performance.txt` only when needed.
- Create `03_script_roles_tagged.txt` only for two or more speakers.
- Put one protected word or phrase per line in `04_pronunciation_glossary.txt`.
- Require identical normalized spoken text across every script variant.

Changing spoken wording after voice generation invalidates subtitle text, timing, chapters, and visual placement.

## Visual manifest schema

| ID | Script cue | Provisional/final time | Asset file | Visual class | Motion | Source/authenticity | Status |
|---|---|---|---|---|---|---|---|
| V01 | Opening claim | 00:00–00:08 | `assets/...` | evidence card | slow push | official source | ready |

Before audio, use script cues instead of guessed timecodes. After final audio, replace them with exact ranges.

Include every class needed by the script: original source, annotated source, generated scene, evidence visualization, and editorial connective graphics. For each moving shot, also record its semantic subject, subject change, no-crop region, subtitle-safe region, and source/authenticity class.

For source-led claims, the manifest should preserve `original source → annotated source → semantic explanation` instead of replacing the source with a generated scene.

## Subtitle alignment contract

`07_subtitles_asr_scaffold.srt` must come from the final audio. Use a final-quality ASR model or forced aligner. Treat small or heavily quantized models as rough-draft tools only.

`08_subtitles_final.srt` must satisfy:

- Sequential cue numbers
- Valid, non-overlapping timestamps
- Exact normalized text match to the locked spoken script
- No role labels or performance tags
- No protected phrase split
- Final cue inside the audio duration
- Similarity, anchor coverage, and unmatched-span thresholds from `scripts/rebuild_srt.py`
- Audible spot checks recorded in `13_publish_qc.md`

When role styling is required, `08_subtitle_role_manifest.json` contains one object per cue:

```json
{"index": 1, "role": "主讲人", "text": "字幕文本", "start_ms": 110, "end_ms": 3124}
```

## Timeline map schema

| Segment | Start | End | Narration cue | Visual IDs | Edit note |
|---|---:|---:|---|---|---|
| 01 | 00:00.000 | 00:08.500 | opening scene | V01, V02 | cut on question |

Use the final voice as the master clock. Derive chapter times from this map or the corrected SRT.

## Jianying placement record

Record:

- Draft folder and `draft_id`
- Decrypted source file and modification time
- Pre-edit video, audio, and text track counts
- Backup path
- Inserted visual and subtitle track IDs
- Speaker colors
- Written timeline copies and hashes
- Post-write decrypt/readback counts
- Subtitle end versus audio/project duration
- Remaining listening checks

`10_nle_media_registry.json` records each inserted asset's stable absolute path, role, codec, duration, hash, material ID, and segment IDs. It must distinguish visual-only, voice, SFX, optional BGM, native subtitles, and any external reference export.

## Editable NLE contract

The Jianying draft must retain:

- A visual-only video layer with no baked captions or audio
- A final-voice audio layer
- An SFX-only layer when SFX exist
- A BGM-only layer only when BGM is approved
- Native Jianying subtitle materials

A baked publish master may accompany the project as a reference but cannot be the only editable media. All timeline references and material/media registrations must point to stable files outside temporary or session directories. Run a short codec-and-link smoke test before full-duration insertion.

## Upload metadata contract

`12_upload_metadata.md` contains:

- Recommended title and two alternatives
- Exact thumbnail text
- Description with payoff in the first two lines
- Final chapters
- Sources and any required disclaimer
- Up to three hashtags
- Compact tag field
- Pinned comment
- Audience/category recommendation

## Publish QC

`13_publish_qc.md` records pass or fail for:

- Full export plays without missing media
- Every visual class appears at the matching spoken passage
- Original or archival material remains present where it is the basis of the claim
- Dynamic shots animate semantic subjects without cropping required words, units, source lines, or evidence
- Subject-only motion review passes after captions and decorative background motion are excluded
- Subtitle import is readable and exact
- Subtitle starts and ends match audible speech at required checkpoints
- Speaker colors match role changes
- No malformed characters or broken protected phrases
- Source quotations, numbers, and claims match citations
- Thumbnail text and title promise match the video
- Chapters match final duration
- Description links work
- Jianying keeps visual-only, voice, SFX, optional BGM, and native subtitles independently editable
- Timeline references and draft media registrations resolve after decrypt/readback
- Published URL and 24-hour/7-day follow-up dates
