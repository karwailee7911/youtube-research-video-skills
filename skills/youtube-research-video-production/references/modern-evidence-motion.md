# Modern evidence motion

Use this reference whenever current research, official statistics, survey results, company filings, technical benchmarks, or paper findings appear on screen.

## Purpose

Present modern evidence with the clarity and energy of a strong product-data shot while preserving research accuracy. Motion and sound should help viewers notice the comparison, trend, scale, or uncertainty; they must not turn evidence into decorative advertising.

## Route the shot

1. Lock the exact claim, source, sample, date, unit, denominator, and uncertainty before designing motion.
2. Decide the one fact the shot must make visible. One shot should have one primary comparison or conclusion.
3. Invoke the installed `$video-shotcraft` skill in **single-shot / single-motion** mode. Read its `SKILL.md`, but do not invoke its full product-promo workflow for the whole research video.
4. From the resolved installed `video-shotcraft` skill directory, inspect `gallery/api/library.json`, scan relevant shot-card frontmatter, select the closest Gallery card/variant, then read the selected card and its exact demo source before adapting it. Reuse the motion grammar and tuned timing; reskin typography, color, layout, and material to the research video's visual system.
5. Read `references/sound-design.md` from the resolved `video-shotcraft` skill directory. Use restrained, action-matched SFX such as counter ticks, paper movement, data reveals, impacts, risers, or transitions. Avoid synthetic game-feedback tones unless the narration explicitly depicts a system response. Use BGM when it can continue naturally across the surrounding section without masking narration or creating an audible seam.
6. During implementation, read and apply `references/aesthetic-rules.md` from the resolved `video-shotcraft` skill directory. Before delivery, run the applicable parts of its `references/final-review.md`. Mark product-feature, product-page, and Gallery-fidelity checks `N/A` when they do not apply; never invent substitute product requirements.

If `video-shotcraft` is unavailable, preserve this sequence and create a simpler evidence shot instead of guessing its cards or assets.

## GSAP router

Use installed GSAP skills only when the evidence shot is being implemented as DOM/SVG/web animation or GSAP materially improves a custom data motion. Existing verified Remotion/Jianying implementations remain the default when they already work.

- Always start with `gsap-core` for GSAP tweens, eases, transforms, stagger, and reduced-motion handling.
- Add `gsap-timeline` for multi-step reveals such as source card → axes → bars/line → highlighted number → conclusion.
- Add `gsap-react` for React/Next.js, or `gsap-frameworks` for Vue/Svelte; use the matching lifecycle, scoped selectors, and cleanup rules.
- Add `gsap-plugins` only for a named need such as DrawSVG chart lines, MorphSVG, Flip layout transitions, SplitText, or MotionPath. Register only the plugins used.
- Add `gsap-utils` when mapping values, clamping, normalizing, interpolating, snapping, or distributing chart elements.
- Add `gsap-performance` when many marks animate or the preview drops frames. Prefer transforms/opacity and avoid layout thrashing.
- Add `gsap-scrolltrigger` only for an interactive webpage whose animation is driven by user scrolling. Do not use it for a fixed-time video render merely because a chart scans across the screen.

Do not load every GSAP skill by default. Select the minimum set required by the actual implementation.

## Evidence and layout rules

- Keep source title/institution, date, sample or denominator, unit, and necessary caveat readable long enough to verify.
- Never animate from altered values or visually exaggerate a difference through a truncated, unlabeled, or inconsistent scale.
- Preserve exact labels and numbers from the approved evidence manifest. Generated decorative values are forbidden in evidence shots.
- Give charts, statistics, source pages, and explanatory copy separate owned rectangles. Run the collision and z-order checks from the main skill.
- Use motion to reveal hierarchy: establish context, reveal the comparison, emphasize the result, then hold. Do not keep elements moving after the evidence has landed.
- Production directions, Gallery card names, implementation notes, frame counts, and shot IDs stay in the manifest and never appear on screen.

## Sound rules

- Sound follows visible actions and the final-audio clock. It never shifts narration, subtitles, or evidence timing.
- Use BGM only when it supports the surrounding section; do not add a new music bed to a single data shot if it causes an audible seam.
- Use one sound purpose per action. Counter ticks belong to number changes; impacts belong to a meaningful landing; whooshes belong to real movement.
- After any visual timing change, retime the SFX table against the final timeline.
- Keep narration intelligible. Deliver a no-BGM version when the project uses `video-shotcraft` BGM, following that skill's sound-delivery rule.

## Final evidence-motion review

Confirm:

- The spoken claim, displayed value, source, unit, and caveat agree.
- The chosen motion makes the comparison easier to understand than a static card would.
- The primary number is readable at delivery resolution and remains still long enough to absorb.
- No card, chart, label, subtitle, or source line collides or becomes obscured.
- BGM/SFX are synchronized to visible actions and do not mask narration.
- No production metadata is visible.
- `video-shotcraft` aesthetic rules were applied during production and applicable final-review items were checked with frame evidence.
- Any GSAP implementation used only the relevant GSAP skills and follows framework cleanup and performance requirements.
