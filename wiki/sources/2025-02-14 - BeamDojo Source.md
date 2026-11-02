---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, humanoid, perception]
sources:
  - https://arxiv.org/abs/2502.10363v3
  - https://arxiv.org/html/2502.10363v3
---

# BeamDojo Source

발판 중첩 보상, double critic, 발 높이 보상을 비교하는 휴머노이드 원자료다.

## Source

- 최초 제출: 2025-02-14. 사용 버전: v3, 2025-04-27. RSS 2025는 [arXiv 서지](https://arxiv.org/abs/2502.10363v3)에서 확인.
- Evidence tier: A. [본문](https://arxiv.org/html/2502.10363v3) §IV와 부록 Tables VII–VIII를 확인했다.
- 조사 경로: [RBQ10 문헌 참조 기록](/home/jay/RBQ10_RL_compare_ws/reports/literature-stairs-20261026-01/implementation.json).

## Notes / Marginalia Check

HTML을 사용했다. 사용자 필기나 annotation을 포함한 PDF는 제공되지 않았다.

## Claims To Verify

하체 출력 12차원이라는 공통점이 G1과 RBQ10의 동역학·발 형상이 같다는 뜻은 아니다. 발바닥 표본 기반 중첩과 실제 압력 분포도 구분해야 한다.

## Promoted To Wiki Pages

- [[2025 - BeamDojo Sparse Foothold Locomotion]] — 보상과 학습 구조.
- [[Open Stair Reward Design and Evaluation]] — 발 높이·지지 품질 평가.
- [[index]] — 전체 출처 카탈로그.
