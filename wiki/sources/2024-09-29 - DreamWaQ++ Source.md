---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, perception, robotics]
sources:
  - https://arxiv.org/abs/2409.19709v2
  - https://arxiv.org/html/2409.19709v2
---

# DreamWaQ++ Source

외부 지각 융합과 style reward 완화를 검토하는 원자료다.

## Source

- 최초 제출: 2024-09-29. 사용 버전: v2, 2026-02-26.
- [arXiv 서지](https://arxiv.org/abs/2409.19709v2)는 IEEE Transactions on Robotics 2026과 DOI `10.1109/TRO.2026.3653774`를 명시한다.
- Evidence tier: A. [본문](https://arxiv.org/html/2409.19709v2)의 §III-B–E, §IV-B/F, §V-F를 중심으로 확인했다.
- 조사 경로: [RBQ10 문헌 참조 기록](/home/jay/RBQ10_RL_compare_ws/reports/literature-stairs-20261026-01/implementation.json).

## Notes / Marginalia Check

웹 본문만 사용했으며 사용자 PDF 필기는 확인할 수 없었다.

## Claims To Verify

DreamWaQ++와 원래 DreamWaQ의 센서 계약을 혼동하지 않는다. §IV-F가 참조한 선행 보상의 전체 계수는 이 페이지에서 재전사하지 않았다.

## Promoted To Wiki Pages

- [[2024 - DreamWaQ++ Multimodal Locomotion]] — 입력·보상·적용 한계.
- [[Terrain Memory for Legged Locomotion]] — 외부 관측 기억의 비교.
- [[index]] — 전체 출처 카탈로그.
