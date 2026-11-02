---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, perception, robotics]
sources:
  - https://arxiv.org/abs/2603.03138v1
  - https://arxiv.org/html/2603.03138v1
---

# LF2WB Source

프로젝트의 별도 지형 기억 구현이 참조하는 관련 문헌이다. 핵심 6편 목록에 포함된 논문이라고 소급하지 않는다.

## Source

- 최초 제출 및 사용 버전: 2026-03-03, v1. ICRA 2026 accepted는 [서지](https://arxiv.org/abs/2603.03138v1)에서 확인.
- Evidence tier: A. [본문](https://arxiv.org/html/2603.03138v1)의 §III 학습·기억, §IV 비교·배포, §V 한계를 확인했다.
- 조사 경로: [로컬 LF2WB README](/home/jay/RBQ10_RL_compare_ws/training/lf2wb/README.md).

## Notes / Marginalia Check

HTML을 사용했으며 사용자 PDF annotation은 확인하지 않았다.

## Claims To Verify

원문의 기억 backbone 비교와 RBQ10의 LSTM 학습 실패는 다른 실험이다. 원문의 고정 크기 추론과 로컬 구현의 실제 latency도 별도 검증 대상이다.

## Promoted To Wiki Pages

- [[2026 - Look Forward to Walk Backward]] — 논문 요약과 구현 차이.
- [[Terrain Memory for Legged Locomotion]] — 지형 기억의 역할.
- [[index]] — 전체 출처 카탈로그.
