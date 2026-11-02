---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, humanoid, sim-to-real]
sources:
  - https://arxiv.org/abs/2502.10363v3
  - https://arxiv.org/html/2502.10363v3
title: "BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds"
authors: [Huayi Wang, Zirui Wang, Junli Ren, Qingwei Ben, Tao Huang, Weinan Zhang, Jiangmiao Pang]
year: 2025
venue: Robotics Science and Systems 2025
doi: 10.48550/arXiv.2502.10363
url: https://arxiv.org/abs/2502.10363v3
---

# BeamDojo

돌·좁은 보처럼 지지 가능한 부분이 드문 지형에서 발을 정확히 놓도록 학습한다. **Unitree G1 휴머노이드 연구**로, RBQ10에는 발 지지 평가와 학습 구성의 참고 문헌이다. [초록](https://arxiv.org/abs/2502.10363v3)

## 입력과 학습

배포에는 LiDAR 기반 elevation map을 사용한다. 첫 단계는 평지 물리와 과제 지형의 지각·발판 보상을 분리해 탐색하고, 두 번째는 실제 과제 지형에서 미세조정한다. 두 critic은 일반 보행 보상과 발판 보상을 분리해서 학습한다. 출력은 하체 12개 관절 목표각이며 PD로 실행한다. [§IV](https://arxiv.org/html/2502.10363v3)

## 보상에서 참고할 항목

- 발바닥의 여러 표본점이 안전한 지지 영역을 벗어나는 정도를 **접촉 때** 벌점으로 계산한다. 발 중심 한 점보다 발바닥 중첩을 직접 다룬다.
- 부록은 action rate와 2차 차분, 관절 가속도, air time, **수평 발 속도로 가중한 목표 높이 오차**도 포함한다. 표의 목표 발 높이는 0.1m다. [§IV-A, Tables VII–VIII](https://arxiv.org/html/2502.10363v3)

## RBQ10 적용과 한계

추론: 작은 4족 발의 collider 최저점 판정은 다각형 발바닥의 지지 면적과 같지 않다. 0.1m라는 높이도 계단 상판 기준 여유 0.1m로 바꿔 읽으면 안 된다. 좌표계·지형 기준·접촉 조건을 재정의해야 한다.

## 연결

- [[2025-02-14 - BeamDojo Source]] — v3와 RSS 발표 정보.
- [[2026 - TactileStep Sole Tactile Locomotion]] — 기하학적 발판 중첩과 실제 압력 지지의 비교.
- [[Open Stair Reward Design and Evaluation]] — 발 높이와 지지 영역 평가.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 형태 차이를 포함한 비교.
- [[index]] — 전체 문헌 카탈로그.
