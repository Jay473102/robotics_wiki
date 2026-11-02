---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, robotics, sim-to-real]
sources:
  - https://arxiv.org/abs/2409.19709v2
  - https://arxiv.org/html/2409.19709v2
title: "DreamWaQ++: Obstacle-Aware Quadrupedal Locomotion With Resilient Multi-Modal Reinforcement Learning"
authors: [I Made Aswin Nahrendra, Byeongho Yu, Minho Oh, Dongkyu Lee, Seunghyun Lee, Hyeonwoo Lee, Hyungtae Lim, Hyun Myung]
year: 2024
venue: IEEE Transactions on Robotics 2026; arXiv first submitted 2024
doi: 10.1109/TRO.2026.3653774
url: https://arxiv.org/abs/2409.19709v2
---

# DreamWaQ++

고유감각과 외부 지각을 함께 사용하면서 센서 오차에도 대응하는 4족 보행 방법이다. **DreamWaQ++를 이름이 비슷한 blind 정책과 혼동하면 안 된다.** 계단·장애물·경사면을 다루며, 여러 로봇 형태로의 확장도 평가한다. [초록 및 서지 정보](https://arxiv.org/abs/2409.19709v2)

## 입력과 구조

- Depth 또는 LiDAR에서 얻은 3D 점들을 PointNet 기반 encoder와 confidence filter로 처리한다.
- 계층형 외부 관측 기억과 고유감각 history를 multimodal mixer로 융합한다.
- 배포 정책은 관절 목표각을 내고 하위 PD가 추종한다. [§III-B–E, §IV-B](https://arxiv.org/html/2409.19709v2)

## 보상과 실험의 의미

기존 DreamWaQ 보상에 더해 토크·관절 속도·가속도·action rate·smoothness 같은 style 보상의 크기를 학습 중 지수적으로 완화한다. 저자는 이런 정규화가 sim-to-real에 필요하지만 기본 동작에 머물게 할 수 있다고 설명한다. [§IV-F](https://arxiv.org/html/2409.19709v2)

추론: RBQ10에서 안정성 계수만 계속 높이면 발을 덜 움직이는 해를 선호할 가능성을 점검해야 한다. 이 논문은 특정 annealing 일정을 RBQ10에 그대로 쓰라는 근거가 아니라, 탐색과 정규화의 균형을 살펴볼 근거다.

## 한계와 열린 질문

형태별 실험은 원하는 발 높이·몸체 높이·접촉력 한계 등 로봇별 값을 조정한다. 열린 발판의 엣지 안전성과 저속 착지 품질은 별도 평가해야 한다. [§V-F](https://arxiv.org/html/2409.19709v2)

## 연결

- [[2024-09-29 - DreamWaQ++ Source]] — v2와 저널 게재 연도.
- [[Terrain Memory for Legged Locomotion]] — 점군 기억과 신뢰도 처리.
- [[2026-11-03 - Does Quadruped RL Need Depth Cameras]] — 학습·배포 입력의 구분.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌 비교.
- [[index]] — 전체 문헌 카탈로그.
