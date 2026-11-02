---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, perception, robotics]
sources:
  - https://arxiv.org/abs/2408.13740v3
  - https://arxiv.org/html/2408.13740v3
---

# PIE Source

프로젝트의 LF2WB 구현이 보상 참조로 연결한 관련 문헌이다. 핵심 6편의 보상 조사 목록과는 별도 경로로 확인했다.

## Source

- 최초 제출: 2024-08-25. 사용 버전: v3, 2024-09-03. RA-L accepted 표기는 [서지](https://arxiv.org/abs/2408.13740v3)에 있다.
- Evidence tier: A. [본문](https://arxiv.org/html/2408.13740v3)의 §III-A, Table I 및 Lite3 실험 설정을 확인했다.
- 조사 경로: [로컬 LF2WB README](/home/jay/RBQ10_RL_compare_ws/training/lf2wb/README.md).

## Notes / Marginalia Check

웹 본문을 사용했으며 사용자 필기 PDF는 제공되지 않았다.

## Claims To Verify

Table I collision 항목은 식과 계수가 모두 음수다. 논문 표기와 로컬 코드의 부호 해석을 구분해 기록한다.

## Promoted To Wiki Pages

- [[2024 - PIE Implicit-Explicit Parkour]] — 단일 단계 학습과 관절 출력.
- [[2026-11-03 - Does Quadruped RL Need Depth Cameras]] — 특권 critic과 배포 actor 구분.
- [[index]] — 전체 출처 카탈로그.
