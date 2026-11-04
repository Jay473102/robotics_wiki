---
type: question
status: active
created: 2026-11-05
updated: 2026-11-05
tags: [question, robotics, manipulation, reinforcement-learning]
sources:
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
  - https://arxiv.org/abs/2611.05372v1
---

# How Should Pose Reaching and Holding Be Evaluated

## Short Answer

**도달 여부, 마지막 구간의 평균 오차, 구간 전체의 유지 성공을 따로 보고해야 한다.** 같은 1 mm·0.2° threshold라도 평균에 적용하는지 모든 sample에 적용하는지에 따라 다른 지표다. 시간·retry budget, 시작/목표 분포, pose 계측 방식까지 함께 명시해야 비교할 수 있다. 근거: [[2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning]], §5, Appendices C, H.7, J, Tier A.

## Why This Question Matters

목표를 잠깐 통과한 정책, 목표 주변에서 진동하는 정책, 정착 후 유지하는 정책은 서로 다르다. PolicyIK의 OpenArm 25초 평가는 60과제 중 reached 54개와 held 43개를 별도로 보고한다. 성공한 한 시점이나 task 간 median만으로 안정적인 정밀 유지를 주장할 수 없다. [Table 3]

## Current Answer

| 지표 | PolicyIK에서의 판정 | 이 지표만으로 알 수 없는 것 |
|---|---|---|
| Simulation strict success | 마지막 1초의 위치·방향 **평균** 오차 ≤1 mm·0.2° | 매 순간 두 threshold 안에 있었는가 |
| Simulation containment | 마지막 1초 **모든 sample**이 두 threshold 안 | 더 긴 시간의 drift·진동 |
| OpenArm reached | trial 중 연속 0.5초 이상 두 threshold 만족 | 마지막까지 유지했는가 |
| OpenArm held | 25초 budget의 마지막 5초(20–25초) 전체에서 두 threshold 만족 | 더 짧은 시간 안에 같은 유지가 가능한가 |
| Median pose error | task별 마지막 1초 평균 오차의 task 간 중앙값 | 실패 비율·tail error·최악 task |

Simulation single attempt는 strict 93.49%와 containment 92.4%다. 조건이 다른 OpenArm holding 43/60을 simulation 성공률과 직접 빼서 sim-to-real gap으로 해석하지 않는다. OpenArm 정책은 별도 실물 학습이고 평가 시간·집계 방식도 다르다. [§5.1–5.2]

### 시간과 재시도는 성능의 일부다

- Simulation deployment 98.92%는 평균 1.212 attempts를 사용하며, 각 attempt를 원래 start에서 다시 시작한다. 단일 attempt의 93.49%와 구분한다. 성공이 없으면 마지막 attempt를 집계한다. [Table 1, Appendix C]
- OpenArm의 마지막 5초 holding은 15초 budget에서 27/60, 25초에서 43/60이다. 충분한 settling time을 제공했는지에 따라 결과가 달라진다. [Appendix H.7, Table 10]
- OpenArm도 40초 trial을 기록하여 그 안에서 15초·25초 budget을 평가한다. xArm7의 holding은 40초 trial 중 **20–25초** 구간이며, OpenArm의 25초 budget과 같은 유지 구간이다. 기록 종료 직전의 35–40초로 잘못 옮겨 적지 않는다. [Appendices I–J]

추론: 비교 실험에서는 single-attempt 성능과 고정된 총 wall-clock·retry budget의 성공률을 함께 제시하는 것이 유용하다. Reset·통신·goal 수정 시간까지 실제 시간에 포함할지는 명시적으로 정해야 한다. 이는 재사용 가능한 평가 제안이며 논문의 추가 결과가 아니다.

### FK 오차와 실제 tool 정확도를 구분한다

PolicyIK의 실물 pose는 joint encoder와 modeled gripper-frame FK에서 계산한다. 같은 모델로 goal과 measured pose를 계산하면 모델 내부의 추종 오차는 측정할 수 있지만, tool calibration·link flex·기구학 오차에 의한 실제 위치 오차를 독립적으로 검증하지는 못한다. [§5.2, Appendix I]

추론: 외부 tracker 또는 독립 metrology가 있는 실험에서는 encoder/FK error와 외부 tool-pose error를 나란히 기록하고, calibration 조건·payload·온도·추종 주기를 함께 보고하는 편이 좋다. 논문에 없는 외부 계측 성공 결과를 가정하지 않는다.

### 실행 제약과 학습 데이터도 비교한다

OpenArm에서는 PolicyIK와 classical baseline의 제어 주기·reference lead bound·관절 margin이 완전히 같지 않다. 동일한 60과제와 시간 예산만으로 actuator command 제약까지 통제한 비교라고 부르지 않는다. 실물 학습에는 near-goal curriculum 외 scripted demo replay가 있다. [Appendices H–I]

추론: [[Reset-State Curricula for Sparse-Reward RL]]에서 정리한 학습 시작 분포와 평가 분포의 구분을 적용하고, goal 난이도·joint-limit 근접성·큰 회전 여부별 결과도 나누면 실패 원인을 해석하기 쉽다.

## Evidence / Sources

- [[2026-11-03 - PolicyIK Source]] — 원본 버전·공식 코드와 독립 재현 범위.
- [[PolicyIK Joint-Reference Control]] — 성공 후에도 종료하지 않는 dwell reward와 누적 reference.
- [[Learned Closed-Loop Inverse Kinematics]] — servo 상태와 정착 동작을 포함하는 제어 문제.
- [[Vision-Language-Action Models]] — 하위 pose tracking 정확도와 상위 manipulation 성공률을 나눠야 하는 응용.
- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] — 한 번의 완료와 지속 유지의 목적 차이를 보상 비교에 반영한다.

## Important Caveats

위 수치는 저자 보고다. 14 μm의 마지막 1초 net motion은 최대 진동폭·외부 절대 정확도가 아니며, 0.035 ms actor forward 시간도 전체 loop latency가 아니다. xArm7 standard set에서는 DLS/QP/MPC 역시 60/60이므로 모든 로봇·지표에서 학습 제어기가 우월하다고 결론내리지 않는다. [§5.1.1, Appendix J]

## Open Questions

- 외부 계측과 장시간 유지 기준에서도 같은 순위가 나타나는가?
- 동일 예산·command constraint에서 재시도의 이점과 controller 자체의 이점을 어떻게 분리할 것인가?
