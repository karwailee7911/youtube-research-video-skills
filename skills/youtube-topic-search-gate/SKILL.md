---
name: youtube-topic-search-gate
description: Search-first validation for Chinese YouTube long-video topics in medicine, economics, technology, literature, history, and other research-led fields. Use when choosing what to publish next, comparing candidate topics, checking current search demand and competition, testing evidence feasibility, or deciding whether a topic is strong enough to enter research and scripting.
---

# YouTube Topic Search Gate

Validate the viewer question before writing the script. Treat search evidence as a gate, not decoration added after production.

Produce one `topic_brief.md` using [references/topic-brief-template.md](references/topic-brief-template.md). End with exactly one decision: `GO`, `REWORK`, or `PARK`.

Do not write the full script in this skill.

## 1. Turn the idea into viewer language

Start with one rough topic, source, dataset, product, work, event, or claim. Generate query clusters in the words a viewer would type:

- Direct question
- Problem, fear, or desired result
- Named source, person, product, theory, or event
- Missing context, contradiction, or common misconception
- Simplified Chinese, Traditional Chinese, common variants, and likely misspellings

Keep one main query and no more than eight supporting queries.

## 2. Search current demand

Browse for every new topic because demand and competition change. Search YouTube first, then a general search engine. Use a trend source when it adds signal.

For each query, record:

- Autocomplete and related questions
- Relevant existing videos, not only the largest channels
- Title, thumbnail promise, view count, publish date, duration, and channel scale
- Whether recent small or medium channels can still receive views
- Recurring claims, viewer anxieties, and unanswered questions

Do not treat one large old video as proof of current demand. Do not treat empty results as automatic opportunity.

## 3. Find a defensible difference

Write one sentence explaining why this video should exist beside current results. Prefer differences such as:

- Restoring omitted source context
- Testing a popular claim against primary data or current evidence
- Comparing two sources or interpretations that are usually separated
- Reproducing a technical claim under named conditions
- Explaining a useful distinction that competitors collapse

Reject differences based only on being “more complete” or “more professional.” Name the missing fact, comparison, test, or mistaken inference.

## 4. Test evidence feasibility

Verify that the proposed promise has enough support before approval.

1. Locate at least one traceable primary source, dataset, official document, specification, text, or other source artifact.
2. Locate current evidence or strong scholarship that can test, contextualize, or challenge the claim.
3. Record versions, dates, pages, units, populations, methods, and limits that matter for the domain.
4. Separate facts from inference and interpretation.

For health topics, prefer current guidelines and systematic reviews. For economics, prefer official data and filings. For technology, prefer official documentation, source code, and reproducible tests. For literature and history, identify the edition, passage, variant, and scholarly disagreement.

## 5. Test packaging before production

Draft three title-thumbnail pairs. Put the searchable question in the title. Let the thumbnail add tension instead of repeating the full title.

Examples:

- Economics title: `降息一定会推高房价吗？先看过去三轮数据` / Thumbnail: `降息＝房价涨？`
- Technology title: `这个 AI 模型真能替代搜索吗？我按官方条件重测了一遍` / Thumbnail: `官方演示靠谱吗`
- Literature title: `《红楼梦》真在这里写了结局吗？脂批原文少不了这句` / Thumbnail: `被省掉的一句`

Avoid certainty that the evidence cannot support.

## 6. Score the gate

Score each item from 0 to 5:

- Search demand
- Click tension
- Concrete differentiation
- Primary-source strength
- Evidence or scholarship strength
- Visual and production feasibility

Decision rules:

- `GO`: at least 21/30, with both source-strength scores at least 3.
- `REWORK`: 16–20, or the package is weak but evidence exists.
- `PARK`: below 16, either source-strength score below 3, or the central claim cannot be framed honestly.

Explain the evidence behind each score.

## Handoff

Only a `GO` brief proceeds to `$youtube-research-video-production`. Include the main query, viewer question, unique angle, primary-source leads, evidence leads, claim boundaries, visual hooks, and chosen title-thumbnail direction.
