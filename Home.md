---
type: home
status: active
created: 2026-06-14
updated: 2026-08-01
tags:
  - robotics
  - physical-ai
  - llm-wiki
sources:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
---

# Robotics / Physical AI Wiki

이 vault는 로보틱스와 Physical AI 연구, 논문, 업체 동향, 개인 노하우를 누적하는 LLM-maintained wiki다. 사람은 자료를 고르고 좋은 질문을 하고, 에이전트가 정리·연결·유지관리를 맡는다.

## Main Entry Points

- [[index]] — 전체 위키 카탈로그. 질문에 답할 때 여기부터 읽는다.
- [[Workflow]] — 자료를 넣고, 질문하고, 점검하는 절차.
- [[Maintenance]] — 위키 점검 체크리스트와 lint 스크립트.
- [[Ontology]] — 지식 축, 관계 어휘, 태그, 근거 등급.
- [[Templates]] — 페이지 템플릿과 frontmatter 명세.
- [[Chat Source Workflow]] — LLM 대화 기록 처리 절차.
- `AGENTS.md` — 에이전트 운영 계약. 규칙은 모두 여기에 있다.

## How To Use

1. 원자료를 `raw/` 아래 알맞은 폴더에 넣는다.
2. 에이전트에게 "이 자료 위키에 넣어줘"라고 요청한다.
3. 에이전트가 `wiki/` 아래에 source note, 논문·개념·방법 페이지, 링크, index, log를 갱신한다.
4. 나중에 질문하면 에이전트가 위키를 먼저 읽고 필요한 경우 원자료까지 확인해 답한다.
5. 가끔 "위키 점검"이라고 하면 깨진 링크, 빠진 페이지, 낡은 주장을 정리한다.

## Ground Rules

- `raw/`는 읽기 전용이다.
- 중요한 주장에는 출처나 불확실성 표시가 붙는다.
- LLM 답변만 근거인 내용은 `검증 필요:`로 남는다.
- 틀린 내용은 삭제하지 않고 `superseded`로 대체된다.

## Current Seed Concepts

- [[Embodied AI]]
- [[Physical AI]]
- [[Vision-Language-Action Models]]
