---
type: meta
status: active
created: 2026-06-14
updated: 2026-08-01
tags:
  - templates
sources: []
---

# Templates

페이지 유형별 템플릿이다. frontmatter 필드 규칙은 `AGENTS.md`의 Frontmatter Contract, 태그 어휘는 [[Ontology]]를 따른다.

## Frontmatter Reference

| 필드 | 필수 | 값 |
|---|---|---|
| `type` | O | `source` `paper` `concept` `method` `entity` `benchmark` `synthesis` `question` `meta` `index` `log` `home` |
| `status` | O | 지식 페이지: `stub` `draft` `active` `verified` `superseded` / source note: `ingested` `partial` |
| `created` | O | `YYYY-MM-DD` |
| `updated` | O | `YYYY-MM-DD`, 내용 변경 시 반드시 갱신 |
| `tags` | O | 소문자 kebab-case, 3-7개 |
| `sources` | O | `raw/` 경로 또는 URL 목록. 없으면 `[]` |
| `superseded_by` | 조건부 | `status: superseded`일 때 필수. `"[[New Page]]"` |
| `title` `authors` `year` `venue` `doi` `url` | paper | 알 수 없으면 빈 값으로 남긴다 |
| `entity_type` | entity | `company` `lab` `product` `platform` `person` |
| `source_kind` `platform` `model` `chat_date` | chat source | 모르면 `unknown` |

## Source (일반)

```markdown
---
type: source
status: ingested
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - source
sources:
  - raw/path/to/source.pdf
---

# Source Title

## Source

- Raw file:
- Type: 논문 / 업체 자료 / 메모 / 강의 자료
- Date:
- Evidence tier: A / B / C

## TL;DR

## Key Content

## Notes / Marginalia Check

## Claims To Verify

## Promoted To Wiki Pages

## Open Questions
```

## Paper

```markdown
---
type: paper
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources:
  - raw/path/to/source.pdf
title:
authors:
year:
venue:
doi:
url:
---

# Title

## TL;DR

## Problem

## Core Idea

## Method

## Data / Embodiment

## Evaluation

## Results

## Limitations

## Connections

## Contradictions / Updates

## Notes / Marginalia

## Open Questions
```

## Concept

```markdown
---
type: concept
status: stub
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
---

# Concept

## Definition

## Why It Matters

## Key Ideas

## Related Papers

## Related Concepts

## Contradictions / Updates

## Open Questions
```

## Method

```markdown
---
type: method
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - method
sources: []
---

# Method

## TL;DR

## Problem Setting

## Procedure

## Assumptions / Requirements

## Inputs / Outputs

## Failure Modes

## Evidence

## Related Concepts

## Open Questions
```

## Benchmark / Dataset

```markdown
---
type: benchmark
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
---

# Benchmark

## Snapshot

## Task Definition

## Data / Scale

## Metrics

## Known Results

## Caveats

## Related Papers

## Open Questions
```

## Company / Product

```markdown
---
type: entity
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
entity_type: company
---

# Company or Product

## Snapshot

## Product / Platform

## Technical Claims

## Evidence

## Market / Deployment

## Related Entities

## As Of

정보 기준 시점과 다음 확인 시점을 적는다.

## Open Questions
```

## Question

```markdown
---
type: question
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - question
sources: []
---

# Question

## Short Answer

## Why This Question Matters

## Current Answer

## Evidence / Sources

## Important Caveats

## Linked Pages
```

## Synthesis

```markdown
---
type: synthesis
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
sources: []
---

# Topic

## Executive Summary

## Current Picture

## Evidence

## Comparison

## Implications

## What To Watch
```

## Chat Source

```markdown
---
type: source
status: ingested
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - source
  - chat-log
sources:
  - raw/chats/YYYY-MM-DD Platform - Topic.md
source_kind: llm-chat
platform:
model:
chat_date:
---

# Chat - Topic

## Source

- Raw file:
- Platform / model:
- Chat date:
- User intent:
- Export format:

## TL;DR

## Important Questions

| Question | Why it matters | Status | Linked page |
|---|---|---|---|
|  |  | source-only / open-question / promoted |  |

## Reusable Answer

## Claims To Verify

## Ideas / Hypotheses

## Links / References Mentioned

## Privacy / Security Notes

## Promoted To Wiki Pages

## Open Questions
```

## Log Entry

`wiki/log.md` 맨 위에 추가한다.

```markdown
## [YYYY-MM-DD] kind | title

- Input:
- Changed:
- Notes:
```

`kind`: `ingest`, `query`, `lint`, `schema`, `maintenance`.

## Superseded Header

페이지가 대체될 때 frontmatter에 `status: superseded`, `superseded_by`를 넣고 본문 첫 줄에 다음을 남긴다.

```markdown
> 이 페이지는 YYYY-MM-DD에 [[New Page]]로 대체되었다. 사유: ...
```
