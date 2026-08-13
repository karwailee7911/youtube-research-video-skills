---
name: youtube-research-video-production
description: End-to-end workflow for research-led Chinese YouTube long videos in medicine, economics, technology, literature, history, and other evidence-based topics. Use after a topic is approved, or when researching primary sources and current evidence, writing single-speaker or multi-speaker narration, generating source screenshots and wide visual carousels, aligning subtitles to final audio, directly editing a Jianying draft without desktop control, creating a series-matched thumbnail, or preparing titles, descriptions, chapters, sources, and tags.
---

# YouTube Research Video Production

Turn an approved topic into a publish-ready research-led long video. Treat the user's recorded or synthesized final voice as a handoff. Prepare everything before and after that handoff.

Read [references/deliverable-contracts.md](references/deliverable-contracts.md) before creating files or handing work between stages. Read only the relevant domain reference:

- Health or medicine: [references/domain-health.md](references/domain-health.md)
- Economics or business: [references/domain-economics.md](references/domain-economics.md)
- Technology or science: [references/domain-technology.md](references/domain-technology.md)
- Literature, philosophy, or history: [references/domain-literature-history.md](references/domain-literature-history.md)

Read [references/subtitle-alignment-qc.md](references/subtitle-alignment-qc.md) whenever audio or subtitles are in scope. Read [references/jianying-direct-draft.md](references/jianying-direct-draft.md) before touching a Jianying draft.

## Hard rules

- Follow this order: `approved topic → research → locked script → visual package → final voice → acoustic alignment → timeline → direct draft edit → readback QC → thumbnail → upload package`.
- Treat the final audio as the only master clock. Regenerated audio invalidates subtitle, chapter, and visual timecodes.
- Finish acoustic alignment and the final visual timeline against the final audio before writing anything into Jianying. Then import video/visuals and subtitles as separate tracks in the same aligned timeline. Subtitles must remain native and editable; never burn subtitles into the video asset used for Jianying assembly.
- Do not control the desktop, click Jianying, open and close Jianying, or use GUI automation. Edit draft files directly when the user asks for assembly.
- Reuse the last verified Jianying import/edit method whenever it still works. Do not research, prototype, or switch to a new import path merely because another method exists. Change methods only after the verified path produces a reproducible failure with recorded evidence, or when the user explicitly requests a different method. Explain the failure and proposed replacement before switching.
- Back up every Jianying file that will change. Write atomically. Decrypt and read back the saved result before reporting success.
- Do not use low-quality ASR as a final timing source. Do not stretch missing transcript text between a few manual anchors.
- Place all relevant source, evidence, and generated visual classes at their matching spoken passages. Do not populate only one class.
- Do not claim completion while any applicable gate or QC check fails.

## Stage 0: Confirm the topic gate

Require a `GO` brief from `$youtube-topic-search-gate`, or create equivalent evidence before continuing. Confirm:

- One searchable viewer question and main query
- One concrete difference from current videos
- Traceable primary sources or data
- Relevant current evidence or scholarship
- One approved claim and one forbidden overclaim
- One title-thumbnail direction

Return to topic validation when an item is missing.

## Stage 1: Build the research dossier

### Primary sources

Locate and preserve the strongest material for the topic. Depending on the domain, this may be:

- A scanned book page, manuscript, speech, law, or archival record
- An official dataset, statistical release, filing, or central-bank document
- Official technical documentation, a standard, code, benchmark, or research paper
- A named literary edition, passage, translation, or critical text

Record title, author or institution, edition or version, date, page or section, URL or local file, and uncertainty. Save untouched originals before annotation.

### Evidence and interpretation

1. Browse current sources when facts, versions, markets, policies, or research may have changed.
2. Prefer primary sources, official documentation, datasets, systematic reviews, and strong scholarship.
3. Record the unit of analysis, comparison, result, limitation, and date.
4. Separate source facts from the creator's interpretation.
5. Mark disagreements and missing evidence instead of flattening them into one answer.

Create a claim-evidence table. Mark every important claim `supported`, `inference`, `uncertain`, or `exclude`.

## Stage 2: Write and lock the narration

Build the long-form progression:

1. Start from the viewer's search situation or concrete puzzle.
2. Expose the missing context, contradiction, or popular shortcut.
3. Show the primary source and explain it in plain Chinese.
4. State what that source cannot establish alone.
5. Compare current evidence or competing interpretations.
6. Give the viewer a usable conclusion and its boundary.
7. Return to the opening question.

Use `$dbs-hook` for the opening, `$dbs-script-flow` for continuity, and `$stop-slop` for the final language pass when available.

Always preserve a clean spoken script. Add only the variants required by the chosen format:

- Clean spoken text with no labels or delivery tags
- Optional performance version with sparse tags such as `[pause]`, `[soft]`, and `[emphasis]`
- Optional role-tagged version for two or more speakers, using headings such as `【主讲人】` and `【提问者】`

Use a single-speaker monologue, question-and-answer format, or multiple roles according to the content. Do not force a second speaker into a script. Do not let role labels or delivery tags enter subtitle text. When variants exist, keep every spoken character identical after normalization.

Lock the script only when claims, dates, numbers, names, pronunciation, breath length, and domain boundaries are resolved. Changing spoken wording after voice generation invalidates downstream timing.

## Stage 3: Create the complete visual package

Create a visual manifest before generating assets. Use the classes that fit the topic:

- Untouched primary-source pages, documents, datasets, interfaces, or code
- Annotated crops that point to the exact sentence, number, table cell, or passage
- Generated historical, conceptual, or atmospheric scenes labeled as illustration when needed
- Modern evidence cards, charts, comparisons, diagrams, or short contrast cards

Use 16:9 for standard inserts. Use a wide canvas such as 7200×900 only when a controlled horizontal pan supports the narration. Give every asset a stable numbered filename and source/authenticity note.

Assign provisional placement by script cue. Wait for final audio before assigning exact timecodes. Do not rotate visuals on a fixed interval. Keep an image on screen while its evidence remains the subject.

Keep production directions in the visual manifest only. Labels such as `画面动作`、`扫描`、`停住`、`标注`、camera directions, timing notes, asset IDs, shot numbers, frame counts, and implementation comments are never audience-facing copy and must not be rendered into the video. If a styleframe contains such notes, treat it as a planning artifact rather than a renderable asset.

Preserve useful evidence motions when they clarify the narration: scan the primary-source page, pause on the cited passage, then mark the exact keywords in sequence. The motion itself should communicate this process; do not explain the motion with an on-screen production note.

For evidence-desk compositions that combine primary sources and modern evidence, assign each card an owned rectangle and readable z-order before rendering. Primary-source pages may overlap slightly as a deliberate stack, but one page must not cover the cited passage on another. Charts, statistics, and explanatory copy must not collide with page cards. When the layout cannot satisfy these constraints, use side-by-side placement or sequential reveals instead of adding more overlap.

## Stage 4: Prepare the final-voice handoff

Give the user:

- Locked clean narration
- Role-tagged or performance copy when requested
- Pronunciation glossary for names, titles, technical terms, foreign words, and unusual characters
- Pace or loudness notes when requested

Pause time-based work until the final WAV or MP3 returns.

## Stage 5: Align the transcript to the final audio

Convert the final audio to 16 kHz mono WAV for analysis while preserving the original file. Generate a word- or character-timestamp ASR scaffold from the complete audio with a final-quality model or forced aligner suited to the language.

Use `scripts/rebuild_srt.py` to rebuild exact subtitle text against that scaffold. Use strict thresholds. If the tool reports low similarity, sparse anchor coverage, or a long unmatched span, generate a better scaffold or inspect the audio. Do not force a low-confidence result through.

For multi-speaker audio, provide the role-tagged script and export the role manifest. Preserve speaker changes at cue boundaries. For a single speaker, use the clean script and omit the role manifest unless native styling needs it.

Follow [references/subtitle-alignment-qc.md](references/subtitle-alignment-qc.md). Listen at the opening, every role change, every quotation, every important number, each chapter boundary, and the ending. Correct local drift before draft insertion.

## Stage 6: Build the final visual timeline

Map exact audio ranges to the visual manifest. Include every ready class required by the script, not one class only.

Use slow push-ins for pages and screenshots, horizontal pans for wide images, and restrained movement for charts or evidence. Record every asset's start, end, motion, crop, and narration cue. Preserve breathing space while the same visual still supports the spoken point.

Derive chapter times from the final SRT or timeline map. Never estimate them from the written script.

## Stage 7: Edit the Jianying draft directly

Do not use desktop control. Follow [references/jianying-direct-draft.md](references/jianying-direct-draft.md).

At minimum:

1. Resolve the exact draft folder and `draft_id` with read-only inspection.
2. Decrypt the newest active timeline and metadata.
3. Count and record existing video, audio, and text tracks.
4. Back up every target file outside the draft folder.
5. Confirm the video/visual timeline and subtitle cues are already aligned to the same final-audio clock before draft insertion.
6. Add or replace the video/visual track and native editable subtitle track as separate track groups. Never substitute a subtitle-burned video for these separate tracks.
7. Preserve unrelated materials and tracks.
8. Encrypt once, then write atomically to every active timeline copy.
9. Update the root index modification time without renaming the draft unless asked.
10. Decrypt the saved result and verify counts, duration, hashes, ordering, media paths, and continued subtitle editability.

SRT does not carry reliable per-speaker Jianying colors. Use a normal single-color subtitle track for one speaker. When the user wants role colors, create native Jianying text materials from the role manifest. Default to white for `主讲人` and cyan-blue for `提问者`, unless the user specifies another palette.

## Stage 8: Create the thumbnail

Use the strongest prior cover as a style reference. Follow the approved title-thumbnail pair.

- Do not assume the creator must appear.
- Preserve the user's likeness only when the user supplies a reference and asks to appear.
- Use an anonymous or symbolic subject when the user asks not to appear.
- Keep no more than three short text lines.
- Inspect exact Chinese characters, mobile legibility, contrast, and safe margins.
- Let the title add information that the thumbnail does not repeat.

## Stage 9: Prepare the upload package

Create:

- One recommended searchable title and two alternatives
- A description whose first two lines state the question and payoff
- Chapters from the final audio or SRT
- Direct primary-source and evidence links
- A domain-appropriate disclaimer when needed
- Up to three hashtags
- A compact tag field for variants, Traditional Chinese, and common errors
- A pinned-comment prompt

Put the main query near the beginning of the title. Keep the promise accurate. Treat tags as secondary metadata.

## Stage 10: Final QC and feedback

Verify:

- The full export plays without missing media.
- Visual changes match spoken passages.
- Subtitle text matches the locked script.
- Subtitle starts and ends match audible speech.
- The Jianying draft contains separate video/visual and native editable subtitle tracks aligned to the same final audio; the assembly video has no burned-in duplicate subtitles.
- Speaker colors change at the correct turns.
- Source quotations, numbers, and interpretations match citations.
- Thumbnail text, title, and opening make the same promise.
- Chapters and description links are correct.
- Every visible non-source text string appears in an approved audience-copy list; no production direction, motion note, asset label, shot ID, frame count, or implementation comment is visible.
- Every multi-card evidence frame passes a collision check: cited source text remains readable, cards do not cover unrelated headings or statistics, and overlap communicates hierarchy rather than accidental crowding.

After publication, record 24-hour and 7-day impressions, click-through rate, average view duration, retention drops, traffic sources, search terms, and viewer confusion. Feed those results into the next topic gate.

## Completion rule

Report a stage as complete only after its artifact exists and passes its gate. Report the full video package as complete only after direct-draft readback and final subtitle listening checks pass.
