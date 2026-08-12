---
name: youtube-research-video-production
description: End-to-end workflow for research-led Chinese YouTube long videos in medicine, economics, technology, literature, history, and other evidence-based topics. Use after a topic is approved, or when researching primary sources and current evidence, writing single-speaker or multi-speaker narration, designing semantic motion without blind image cropping, aligning subtitles to final audio, delivering editable Jianying tracks without desktop control, creating a series-matched thumbnail, or preparing titles, descriptions, chapters, sources, and tags.
---

# YouTube Research Video Production

Turn an approved topic into a publish-ready research-led long video. Treat the user's recorded or synthesized final voice as a handoff. Prepare everything before and after that handoff.

Read [references/deliverable-contracts.md](references/deliverable-contracts.md) before creating files or handing work between stages. Read only the relevant domain reference:

- Health or medicine: [references/domain-health.md](references/domain-health.md)
- Economics or business: [references/domain-economics.md](references/domain-economics.md)
- Technology or science: [references/domain-technology.md](references/domain-technology.md)
- Literature, philosophy, or history: [references/domain-literature-history.md](references/domain-literature-history.md)

Read [references/subtitle-alignment-qc.md](references/subtitle-alignment-qc.md) whenever audio or subtitles are in scope. Read [references/jianying-direct-draft.md](references/jianying-direct-draft.md) before touching a Jianying draft.

Read [references/semantic-motion-and-shotcraft.md](references/semantic-motion-and-shotcraft.md) whenever dynamic visuals, Remotion, `$video-shotcraft`, or motion QC are in scope.

## Hard rules

- Follow this order: `approved topic → research → locked script → visual package → final voice → acoustic alignment → timeline → direct draft edit → readback QC → thumbnail → upload package`.
- Treat the final audio as the only master clock. Regenerated audio invalidates subtitle, chapter, and visual timecodes.
- Do not control the desktop, click Jianying, open and close Jianying, or use GUI automation. Edit draft files directly when the user asks for assembly.
- Back up every Jianying file that will change. Write atomically. Decrypt and read back the saved result before reporting success.
- Do not use low-quality ASR as a final timing source. Do not stretch missing transcript text between a few manual anchors.
- Place all relevant source, evidence, and generated visual classes at their matching spoken passages. Do not populate only one class.
- Animate semantic objects, not arbitrary crops of finished posters, screenshots, evidence cards, or text-heavy images. Preserve every meaningful label and no-crop region.
- For historical or textual claims, keep the source layer visible in the sequence: `untouched source → annotated source → semantic explanation`. A generated reconstruction cannot replace the cited original.
- Default to an editable NLE handoff: visual-only master, final voice, SFX, optional BGM, and native subtitles remain separate. A baked reference export is not the only project asset.
- Inspect existing project files and retained constraints before asking setup questions. Do not re-ask choices such as aspect ratio, BGM, or draft target when the answer is already available.
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

For source-led passages, plan a three-layer visual sequence when the material exists:

1. Show the untouched original long enough to establish provenance.
2. Show an annotated copy that points to the exact passage, value, or object.
3. Rebuild the idea as clean semantic objects for motion and explanation.

Do not zoom into the middle of a page merely to manufacture movement. If text, labels, or evidence cannot survive the crop, create a new supporting asset or extract the relevant object into an editable composition. When `$video-shotcraft` is installed and dynamic visuals are requested, use its validated recipe system with the research-video profile in [references/semantic-motion-and-shotcraft.md](references/semantic-motion-and-shotcraft.md). Do not import product-video discovery questions into an already specified research project.

Assign provisional placement by script cue. Wait for final audio before assigning exact timecodes. Do not rotate visuals on a fixed interval. Keep an image on screen while its evidence remains the subject.

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

Use slow push-ins for pages and screenshots only when the crop remains semantically valid. Use horizontal pans for intentionally wide images and restrained object-level movement for charts or evidence. Record every asset's start, end, semantic target, motion, crop, no-crop region, subtitle-safe region, and narration cue. Preserve breathing space while the same visual still supports the spoken point.

Long shots must contain narration-driven subject change or an explicitly justified hold. A moving grid, caption animation, top-bar sweep, particle layer, or one-pixel drift does not make a static subject dynamic. Avoid blanket shake, continuous breathing zoom, and transitions that fade every new shot up from black. Run subject-only motion QC using [references/semantic-motion-and-shotcraft.md](references/semantic-motion-and-shotcraft.md).

Derive chapter times from the final SRT or timeline map. Never estimate them from the written script.

## Stage 7: Edit the Jianying draft directly

Do not use desktop control. Follow [references/jianying-direct-draft.md](references/jianying-direct-draft.md).

At minimum:

1. Resolve the exact draft folder and `draft_id` with read-only inspection.
2. Decrypt the newest active timeline and metadata.
3. Count and record existing video, audio, and text tracks.
4. Back up every target file outside the draft folder.
5. Add or replace only the generated tracks.
6. Preserve unrelated materials and tracks.
7. Encrypt once, then write atomically to every active timeline copy.
8. Update the root index modification time without renaming the draft unless asked.
9. Decrypt the saved result and verify counts, duration, hashes, ordering, and media paths.

Keep the handoff editable by default:

- Video: visual-only master with no baked subtitles and no baked audio
- Audio 1: locked final voice
- Audio 2: SFX-only track
- Audio 3: BGM only when the project explicitly uses it
- Text: native Jianying subtitle materials from the final aligned SRT or role manifest

Keep any fully mixed export as a reference outside the editable stack. Do not replace the separate tracks with that export. Use stable media paths, update both timeline references and draft media registration, and run a short smoke test before assembling the full duration. Default to zero user-run command files; if OS permission makes one unavoidable, provide one idempotent, resumable entry point rather than a sequence of command files.

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
- Speaker colors change at the correct turns.
- Source quotations, numbers, and interpretations match citations.
- Thumbnail text, title, and opening make the same promise.
- Chapters and description links are correct.

Use four separate approval states:

- Technical: file integrity, codec, duration, paths, render, and readback
- Content: claims, source labels, transcript, subtitle timing, and safety boundaries
- Visual: semantic motion, crop integrity, source continuity, subtitle-safe layout, and transition seams
- User approval: the user has watched the candidate and accepted it

Run the independent technical, content, and visual review before asking for user approval. Record the approved file hash or draft snapshot. After approval, lock that version; do not reopen it for later non-blocking aesthetic observations. Reopen only for a concrete blocking defect, and state the reason before changing the approved version.

After publication, record 24-hour and 7-day impressions, click-through rate, average view duration, retention drops, traffic sources, search terms, and viewer confusion. Feed those results into the next topic gate.

## Completion rule

Report a stage as complete only after its artifact exists and passes its gate. Report the full video package as complete only after direct-draft readback and final subtitle listening checks pass.
