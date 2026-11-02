---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, robotics, sim-to-real]
sources:
  - https://arxiv.org/abs/2408.13740v3
  - https://arxiv.org/html/2408.13740v3
title: "PIE: Parkour with Implicit-Explicit Learning Framework for Legged Robots"
authors: [Shixin Luo, Songbo Li, Ruiqi Yu, Zhicheng Wang, Jun Wu, Qiuguo Zhu]
year: 2024
venue: IEEE Robotics and Automation Letters; accepted 2024
doi: 10.48550/arXiv.2408.13740
url: https://arxiv.org/abs/2408.13740v3
---

# PIE

명시적인 물리량 추정과 잠재 특징을 함께 학습해, depth와 고유감각으로 관절 명령을 생성한다. Actor·critic·estimator를 한 단계에서 동시에 학습하며 DEEP Robotics Lite3에 배포한다. [초록 및 본문 §III](https://arxiv.org/abs/2408.13740v3)

## 입력과 출력

Actor는 고유감각과 추정 속도·발 clearance·높이맵 특징·잠재 벡터를 받는다. Critic에는 정답 속도와 지형 scandots가 추가된다. 행동은 12차원이며 기본 서기 자세에 더해 관절 목표각을 만든다. **단일 단계 학습도 특권 critic을 사용할 수 있다.** [§III-A](https://arxiv.org/html/2408.13740v3)

## 보상과 평가

Table I에는 선속도·yaw 추종, 수직속도, roll/pitch 각속도, 자세, 관절 가속도·출력, 비발 부위 충돌, action rate와 2차 차분 smoothness가 있다. 시뮬레이션 ablation과 실물 장애물·계단 실험을 수행한다. [Table I 및 §IV](https://arxiv.org/html/2408.13740v3)

검증 필요: Table I의 collision 식과 가중치는 모두 음수로 표기되어 있다. 이를 문자 그대로 곱해 충돌을 보상하면 의도와 어긋나므로 구현 시 부호를 대조해야 한다.

## RBQ10 연결

[로컬 LF2WB 구현 기록](/home/jay/RBQ10_RL_compare_ws/training/lf2wb/README.md)은 PIE 보상 계열을 참조하고 위 부호를 해석한 방식을 명시한다. 추론: 이 구현의 파라미터와 성능을 원저자의 재현 결과로 표기해서는 안 된다.

## 연결

- [[2024-08-25 - PIE Source]] — v3 및 보상 표의 검증 항목.
- [[2026 - Look Forward to Walk Backward]] — 동시 학습에 지형 기억을 결합한 관련 문헌.
- [[2026-11-03 - Does Quadruped RL Need Depth Cameras]] — actor와 critic 입력 구분.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌 비교.
- [[index]] — 전체 문헌 카탈로그.
