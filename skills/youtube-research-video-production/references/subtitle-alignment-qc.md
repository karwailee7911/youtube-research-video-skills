# Subtitle acoustic alignment and QC

Use this procedure after the final Fish Audio file exists.

## Build the timing scaffold

1. Preserve the original WAV or MP3.
2. Decode an analysis copy to 16 kHz mono WAV.
3. Run a final-quality Chinese ASR model or a forced aligner with word or character timestamps.
4. Export an SRT scaffold from the complete audio.
5. Confirm that the scaffold covers the entire recording and does not omit a speaker.

Do not use a tiny or heavily quantized model for final placement. Do not accept a scaffold because its total duration looks correct.

## Rebuild exact text

Run:

```bash
python3 scripts/rebuild_srt.py \
  --source-srt 07_subtitles_asr_scaffold.srt \
  --transcript 03_script_final.txt \
  --output 08_subtitles_final.srt \
  --glossary 04_pronunciation_glossary.txt
```

For multiple speakers or role colors, replace `03_script_final.txt` with `03_script_roles_tagged.txt` and add `--role-manifest 08_subtitle_role_manifest.json`.

The script removes `【角色】` headings and square-bracket performance tags when present. It preserves spoken punctuation. It assigns cue roles only when a role manifest is requested.

Stop when the tool reports:

- Similarity below the configured threshold
- Matched target coverage below the threshold
- An unmatched target run above the threshold
- A long acoustic span with no reliable text anchors
- A role boundary inside one cue

Generate a better scaffold or inspect whether the audio and script differ. Do not lower thresholds until a weak result passes.

## Cue rules

- Prefer 8–18 Chinese alphanumeric characters per cue.
- Keep one semantic phrase per cue.
- Avoid one-character tails.
- Keep protected names, quotations, numbers, and medical terms intact.
- Keep cue times non-overlapping.
- Keep the final cue inside the final audio duration.
- Do not add a fixed global offset unless the waveform proves that the entire file has the same offset.
- Do not warp a long missing span between a few manually chosen sentence anchors.

## Required listening checkpoints

Listen while viewing the subtitles at:

1. First spoken word
2. Every speaker change when the audio has multiple speakers
3. Every direct quotation or source reading
4. Every important criterion, date, or number
5. Every chapter boundary
6. Last spoken sentence

Add checkpoints around every low-confidence or long-interpolation span reported by the rebuild tool.

Record the measured difference at each checkpoint. Treat a repeated offset as a global timing issue. Treat offsets that grow or shrink as local alignment drift. Fix the scaffold or the affected span, then rerun validation.

## Final checks

Run `scripts/validate_srt.py` against the final audio and the matching locked script. Add the role manifest only for multi-speaker styling. Structural validation cannot replace listening. Mark subtitle timing as passed only after both checks succeed.
