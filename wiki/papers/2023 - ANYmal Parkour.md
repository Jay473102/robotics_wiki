---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, robotics, sim-to-real]
sources:
  - https://arxiv.org/abs/2306.14874v1
  - https://arxiv.org/html/2306.14874v1
  - https://www.research-collection.ethz.ch/entities/publication/192e4e2a-a24d-432a-99f6-6993e6fc870d
title: "ANYmal Parkour: Learning Agile Navigation for Quadrupedal Robots"
authors: [David Hoeller, Nikita Rudin, Dhionis Sako, Marco Hutter]
year: 2023
venue: Science Robotics 9(88), 2024; arXiv first submitted 2023
doi: 10.1126/scirobotics.adi7566
url: https://arxiv.org/abs/2306.14874v1
---

# ANYmal Parkour

지각·여러 보행 기술·상위 navigation을 학습하는 계층형 시스템이다. ANYmal D에서 연속 장애물 통과를 보이며, 하나의 출력망이 모든 기술을 직접 생성하는 구성과 구분해야 한다. [논문 초록](https://arxiv.org/abs/2306.14874v1)

## 입력과 구조

Depth 카메라와 LiDAR 점군을 다중 해상도 지형 표현으로 복원한다. 상위 정책은 걷기·뛰기·오르기·내려가기·웅크리기 기술을 선택하고 명령을 전달한다. 가려진 구조는 이전 지각 출력을 현재 좌표로 옮겨 누적한다. [본문 §IV-B](https://arxiv.org/html/2306.14874v1)

## 보상에서 참고할 항목

Supplementary Table S2에는 목표 위치·heading, 관절 속도·토크·한계, **몸체 가속도, 발 가속도, action rate, 과도한 접촉력**, 충돌·stumble, 기다리지 않기와 목표 도착 후 서 있기 항목이 있다. [Table S2](https://arxiv.org/html/2306.14874v1)

움직임 억제만이 아니라 진행과 도착 후 정지를 구분한 구성이 RBQ10 검토에 유용하다. 추론: 각 보상의 활성 조건과 단위를 읽어야 하며, ANYmal의 계수를 RBQ10에 그대로 복사할 근거는 없다.

## 한계와 열린 질문

논문은 여러 네트워크의 개별 학습과 상호 의존성에 따른 재학습 부담을 논의한다. [§III-A](https://arxiv.org/html/2306.14874v1) 추론: 이 계층형 구조의 성공을 RBQ10 단일 출력망의 우월성이나 열위에 대한 직접 증거로 사용할 수 없다.

## 연결

- [[2023-06-26 - ANYmal Parkour Source]] — 2023 preprint와 2024 저널을 구분.
- [[Perceptive Legged Locomotion]] — 지도 기반 계층형 사례.
- [[Open Stair Reward Design and Evaluation]] — 가속도·정지 보상의 적용 조건.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌 비교.
- [[index]] — 전체 문헌 카탈로그.
