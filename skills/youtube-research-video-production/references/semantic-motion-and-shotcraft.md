# Semantic motion and video-shotcraft profile

Use this reference for Remotion, dynamic explainers, `$video-shotcraft`, or motion review in a research-led video.

## Start autonomously

Inspect the topic brief, locked script, final audio, visual manifest, existing assets, prior project constraints, and current draft before asking questions. Reuse decisions that are already explicit or safely inferable, including 16:9 delivery, language, BGM policy, series style, and draft target.

For research, medicine, literature, or history, treat `$video-shotcraft` as a motion system rather than a product-video brief. Do not ask product-launch questions when the narration and evidence already define the job. Back up an existing project before rebuilding it.

## Preserve visual truth

Classify every asset:

- `SOURCE`: untouched scan, page, document, dataset, interface, code, photo, or archival record
- `ANNOTATED SOURCE`: a copy with highlights, boxes, arrows, or readable crops
- `EVIDENCE`: chart, comparison, timeline, table, or study card built from cited data
- `GENERATED CONCEPT`: an illustration or reconstruction with an on-screen label when viewers could mistake it for evidence
- `EDITORIAL`: connective graphics that organize or pace the explanation

Use the sequence `SOURCE → ANNOTATED SOURCE → semantic explanation` for claims grounded in original material. A digital transcription is not an original scan. A generated historical scene is not archival evidence. Do not remove the source layer merely because a reconstructed motion scene looks cleaner.

## Animate meaning, not files

A finished poster, screenshot, evidence card, or page is not automatically a good animation layer. Before adding motion, identify:

- the spoken claim or question
- the subject the viewer must track
- the label, number, line, or relationship that must stay visible
- no-crop regions
- the subtitle-safe region
- the desired change during the shot

If the useful object cannot survive the crop, rebuild it as an editable semantic layer. Extract or recreate nodes, labels, highlights, chart marks, timelines, and comparison blocks. Use generated visuals for supporting scenes or backgrounds, not for text that must be exact.

Never crop through a title, unit, conclusion, source line, axis, face, joint, quoted passage, or evidence boundary merely to create a zoom. Do not move a full text-heavy image around the frame while expecting the viewer to read it.

Useful narration-driven patterns include:

- source page, then highlight the exact sentence
- number appears when spoken, followed by its unit and comparator
- process nodes activate in causal order
- two states separate, converge, or exchange emphasis during a comparison
- evidence card reveals population, result, and limitation in sequence
- map, anatomy, or diagram highlights only the region being discussed

## Motion and transition rules

- Give each shot one dominant subject and one readable change.
- Use object-level transforms, masks, line growth, state changes, focus shifts, and controlled camera moves.
- Keep intentional stillness when it helps comprehension, but do not leave a long subject hold while only captions, particles, a grid, a top bar, or one-pixel drift move.
- Do not apply blanket shake, continuous breathing zoom, or random Ken Burns movement to every shot.
- Use hard cuts, matched cuts, or short overlaps as appropriate. Do not make every incoming shot start at zero opacity, which creates dark flashes between scenes.
- Keep captions out of evidence conclusions, units, source labels, and other important lower-third content.

## Shot recipe extension

For each dynamic shot, add these fields to the normal shot recipe:

```text
Narration cue:
Semantic subject:
Subject change:
Source/authenticity class:
No-crop regions:
Subtitle-safe region:
First/middle/last frame expectation:
```

## Subject-only motion QC

Review motion on the content region, excluding captions, decorative top bars, looping grids, particles, and background noise. These elements must not be allowed to hide a static subject.

Check:

1. First, middle, and last frames preserve every required word, number, unit, and source label.
2. Subject-level changes follow spoken beats rather than a fixed timer.
3. Long shots have meaningful progression or a documented reason to hold.
4. Shot boundaries have no accidental black or dark flash.
5. Generated concept visuals keep their required authenticity label.
6. Captions do not cover evidence conclusions or source lines.

Use separate gates:

- Technical review checks render integrity, codecs, duration, audio, and missing media.
- Content review checks claims, labels, citations, transcript, and timing.
- Visual review checks semantic motion, crop integrity, source continuity, layout, and seams.
- User approval occurs only after those checks pass.

Record the hash of the user-approved candidate. Later non-blocking preferences belong in the next iteration notes; they do not silently reopen the accepted file.
