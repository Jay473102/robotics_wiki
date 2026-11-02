---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, robotics, sim-to-real]
sources:
  - https://arxiv.org/abs/2606.25765v2
  - https://arxiv.org/html/2606.25765v2
  - https://sivan666666.github.io/StairMaster/
title: "StairMaster: Learning to Conquer Risky Hollow Stairs for Agile Quadrupedal Robots"
authors: [Xincheng Tang, Youhan Xie, Zhengjie Shu, Wanyu Li, Lai Jiang, Wenkang Hu, Yitong Li, Ruigang Yang]
year: 2026
venue: arXiv preprint v2
doi: 10.48550/arXiv.2606.25765
url: https://arxiv.org/abs/2606.25765v2
---

# StairMaster

전면이 열린 계단의 발 끼임, 좁은 발판, 깊이 영상 결손을 함께 다루는 4족 보행 연구다. Unitree Go2에서 최대 55° 열린 계단 주행을 보고해, 이번 문헌 중 RBQ10 과제와 직접적인 관련성이 가장 높다. 각도는 저자 실험의 범위다. [논문 초록](https://arxiv.org/abs/2606.25765v2)

## 입력과 학습

| 구분 | 논문 설계 |
|---|---|
| 교사 | 고유감각과 특권 높이맵을 사용하는 PPO |
| 학생 | 실제 배포 가능한 depth 영상과 고유감각으로 교사 행동을 모방 |
| 추가 학습 | 학생을 PPO로 미세조정 |
| 기억 | Cross-attention으로 융합한 특징을 spatial gate가 있는 LSTM/SRU에 누적 |
| 출력 | 관절 목표각을 출력하고 하위 PD가 토크로 변환 |

센서 모델에는 픽셀 결손, 경계 오차, stereo matching 오차와 진동에 따른 영상 이동을 넣는다. [본문 Method 및 Experimental Setup](https://arxiv.org/html/2606.25765v2)

## 보상과 평가

- 3D waypoint를 이용한 몸체 pitch 유도로 다음 발판을 먼저 관측한다.
- 발이 미리 정의한 hollow volume에 들어가면 벌점을 준다.
- 접촉점이 발판 가장자리의 안전 여유보다 가까우면 벌점을 준다. **엣지를 밟으라는 정책이 아니다.**
- 형상 난이도와 간격을 바꾸는 curriculum, 센서·동역학 randomization을 함께 사용한다. [Customized Reward Design 및 Training Details](https://arxiv.org/html/2606.25765v2)

## RBQ10 적용과 한계

추론: LSTM만 추가하는 것으로 이 접근을 재현할 수 없다. 열린 공간의 충돌 형상, 센서 결손, 발판 이탈 비용, 학생 정책의 실제 학습 경로를 함께 맞춰야 한다. 논문의 특권 교사 입력과 RBQ10 배포 actor의 센서 입력은 별도 계약이다.

검증 필요: Go2의 결과를 RBQ10의 발 형상·구동기·저속 정지 조건으로 옮겼을 때의 성공률.

## 연결

- [[2026-06-24 - StairMaster Source]] — 사용한 버전과 서지 불일치를 기록.
- [[Terrain Memory for Legged Locomotion]] — 시야 밖 발판의 기억.
- [[Open Stair Reward Design and Evaluation]] — 보상 이식과 검증 절차.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 다른 문헌 및 프로젝트 결과와 비교.
- [[index]] — 전체 문헌 카탈로그.
