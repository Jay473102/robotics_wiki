---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, robotics, sim-to-real]
sources:
  - https://arxiv.org/abs/2309.14341v1
  - https://arxiv.org/html/2309.14341v1
  - https://extreme-parkour.github.io/
title: Extreme Parkour with Legged Robots
authors: [Xuxin Cheng, Kexin Shi, Ananye Agarwal, Deepak Pathak]
year: 2023
venue: ICRA 2024; arXiv first submitted 2023
doi: 10.48550/arXiv.2309.14341
url: https://arxiv.org/abs/2309.14341v1
---

# Extreme Parkour with Legged Robots

Unitree A1의 전방 depth 카메라와 고유감각으로 장애물에 맞는 동작을 생성하는 단일 정책이다. 도약·틈 통과·경사면 등 동적 parkour가 대상이며, 저속 열린 계단 전용 연구는 아니다. 학회 발표는 ICRA 2024, 파일명의 2023은 최초 arXiv 연도다. [저자 프로젝트](https://extreme-parkour.github.io/)

## 입력과 학습

교사는 특권 scandots, 환경 정보와 waypoint 방향을 사용한다. 이후 depth에서 지형 특징과 heading을 추정하는 학생으로 증류한다. 관절각 명령까지 학습하는 구조이며, 훈련용 정답 지형을 배포 입력으로 간주하면 안 된다. [본문 §3](https://arxiv.org/html/2309.14341v1)

## 보상과 평가

- 세계좌표계에서 다음 waypoint 방향으로의 속도 성분을 보상하고 명령 속도에서 상한을 둔다.
- 접촉한 발이 지형 경계 **5cm 이내**에 있으면 벌점을 준다. 논문 명칭 $r_{clearance}$는 **수평 엣지 여유**이며 스윙 최고 높이 보상이 아니다.
- 시뮬레이션은 진행 거리와 edge violation을 함께 측정한다. 엣지 벌점을 제거한 비교 정책은 진행해도 위험한 경계 접촉이 늘어난다. [§3.1, §4.3 및 Tables 2–3](https://arxiv.org/html/2309.14341v1)

## RBQ10 적용과 한계

추론: 진행 보상만으로 엣지 접촉이 사라지지 않는다는 점이 유용하다. 다만 점프를 허용하는 최적 동작을 그대로 목표로 삼으면 사용자가 원하는 느린 발 이동과 달라질 수 있다. 발 높이, 착지 속도, 지지 중 미끄럼은 별도 측정이 필요하다.

## 연결

- [[2023-09-25 - Extreme Parkour Source]] — 원문과 발표 정보.
- [[2026 - StairMaster Hollow Stair Locomotion]] — 열린 계단 전용 확장과 비교.
- [[Open Stair Reward Design and Evaluation]] — 엣지 여유와 발 높이를 분리.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌 비교.
- [[index]] — 전체 문헌 카탈로그.
