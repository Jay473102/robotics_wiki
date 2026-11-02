---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, humanoid, perception]
sources:
  - https://arxiv.org/abs/2609.28959v1
  - https://arxiv.org/html/2609.28959v1
---

# TactileStep Source

발을 천천히 내려놓고 안정적인 지지를 확보하는 단계별 보상의 원자료다.

## Source

- 최초 제출 및 사용 버전: 2026-09-24, v1. [서지](https://arxiv.org/abs/2609.28959v1)
- Evidence tier: A. [본문](https://arxiv.org/html/2609.28959v1)의 §3, Algorithm 1, 부록 B.1 보상 목록을 확인했다.
- 조사 경로: [RBQ10 문헌 참조 기록](/home/jay/RBQ10_RL_compare_ws/reports/literature-stairs-20261026-01/implementation.json).

## Notes / Marginalia Check

웹 본문만 사용했다. 사용자 주석 PDF가 없어 annotation 유무는 미확인이다.

## Claims To Verify

본문의 개념식과 부록의 deadband·warmup·event 처리식을 함께 봐야 한다. RBQ10 합력·최저점 proxy를 압력 센서의 면적·CoP와 동일시하지 않는다.

## Promoted To Wiki Pages

- [[2026 - TactileStep Sole Tactile Locomotion]] — 관측과 접촉 단계별 보상.
- [[Open Stair Reward Design and Evaluation]] — 구현 단위와 측정 한계.
- [[index]] — 전체 출처 카탈로그.
