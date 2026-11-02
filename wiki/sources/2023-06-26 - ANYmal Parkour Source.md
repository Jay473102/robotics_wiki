---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, perception, robotics]
sources:
  - https://arxiv.org/abs/2306.14874v1
  - https://arxiv.org/html/2306.14874v1
  - https://www.research-collection.ethz.ch/entities/publication/192e4e2a-a24d-432a-99f6-6993e6fc870d
---

# ANYmal Parkour Source

계층형 보행 구조와 동작 정규화 보상을 비교하는 원자료다.

## Source

- 최초 제출: 2023-06-26, arXiv v1. 저널: Science Robotics 9(88), 2024, DOI `10.1126/scirobotics.adi7566`.
- 원본: [arXiv 본문](https://arxiv.org/html/2306.14874v1), [ETH 기관 서지](https://www.research-collection.ethz.ch/entities/publication/192e4e2a-a24d-432a-99f6-6993e6fc870d).
- Evidence tier: A. 본문 구조·한계와 supplementary **Table S2**의 locomotion rewards를 확인했다. ETH 서지는 검색 제공 내용으로 확인했으며 직접 열기는 403이었다.
- 조사 경로: [RBQ10 문헌 참조 기록](/home/jay/RBQ10_RL_compare_ws/reports/literature-stairs-20261026-01/implementation.json).

## Notes / Marginalia Check

HTML 본문과 보충표를 사용했다. 사용자 필기 PDF는 제공되지 않아 주석 검사는 수행하지 않았다.

## Claims To Verify

로컬 기록의 링크 fragment보다 표 제목을 기준으로 찾는다. 상위 navigation과 하위 locomotion 보상은 서로 다른 목적이다.

## Promoted To Wiki Pages

- [[2023 - ANYmal Parkour]] — 저널 연도와 preprint 연도를 구분한 요약.
- [[Open Stair Reward Design and Evaluation]] — 발·몸체 가속도와 정지 항목.
- [[index]] — 전체 출처 카탈로그.
