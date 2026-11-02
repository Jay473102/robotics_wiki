---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, perception, robotics]
sources:
  - https://arxiv.org/abs/2309.14341v1
  - https://arxiv.org/html/2309.14341v1
  - https://extreme-parkour.github.io/
---

# Extreme Parkour Source

진행 방향과 엣지 접촉 보상을 비교할 때 사용한 4족 parkour 문헌이다.

## Source

- 최초 제출 및 사용 버전: 2023-09-25, v1. ICRA 2024 발표는 [저자 프로젝트](https://extreme-parkour.github.io/)에서 확인.
- 원본: [서지](https://arxiv.org/abs/2309.14341v1), [본문](https://arxiv.org/html/2309.14341v1).
- Evidence tier: A. 확인 범위: §3 학습·보상, §4.3의 edge ablation과 평가 정의.
- 조사 경로: [RBQ10 문헌 참조 기록](/home/jay/RBQ10_RL_compare_ws/reports/literature-stairs-20261026-01/implementation.json).

## Notes / Marginalia Check

웹 본문을 사용했다. 사용자 필기 PDF가 없어 annotation 유무는 미확인이다.

## Claims To Verify

보상 이름의 clearance를 스윙 높이로 해석하지 않는다. 열린 계단의 저속 주행 성능은 이 논문의 일반 parkour 결과와 별도다.

## Promoted To Wiki Pages

- [[2023 - Extreme Parkour with Legged Robots]] — 논문 요약.
- [[Open Stair Reward Design and Evaluation]] — 엣지와 발 높이 구분.
- [[index]] — 전체 출처 카탈로그.
