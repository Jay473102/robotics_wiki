---
type: method
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [method, reinforcement-learning, robotics, perception, sim-to-real]
sources:
  - https://arxiv.org/html/2606.25765v2
  - https://arxiv.org/html/2309.14341v1
  - https://arxiv.org/html/2306.14874v1
  - https://arxiv.org/html/2409.19709v2
  - https://arxiv.org/html/2502.10363v3
  - https://arxiv.org/html/2609.28959v1
---

# Open Stair Reward Design and Evaluation

열린 계단의 저속 보행은 진행, 발의 이동, 접촉 직전 감속, 실제 착지, 지지 유지, 목표에서 정지를 함께 평가해야 한다. 아래 절차는 문헌 비교와 RBQ10 관측에서 정리한 **구현·검증 방법**이며, 어느 한 논문의 보상 계수를 그대로 재현한 것이 아니다.

## 보상 항목과 문헌 연결

| 목적 | 문헌에서 참고할 내용 | RBQ10에서 확인할 점 |
|---|---|---|
| 진행과 과속 억제 | [[2023 - Extreme Parkour with Legged Robots]]의 세계좌표 진행 | 명령 속도, 실제 속도, 정체 시간을 함께 기록 |
| 열린 공간 진입 회피 | [[2026 - StairMaster Hollow Stair Locomotion]]의 hollow-volume 비용 | 발판 아래 공간과 정상적인 공중 이동을 구분 |
| 엣지 회피 | StairMaster와 Extreme Parkour의 접촉 조건부 벌점 | 접촉점의 전후·측면 여유를 따로 확인 |
| 충분한 발 높이 | [[2025 - BeamDojo Sparse Foothold Locomotion]] 부록의 높이 항 | 실제 상판·시작 지지면·스윙 최고점의 좌표 기준 |
| 부드러운 착지 | [[2026 - TactileStep Sole Tactile Locomotion]]의 접촉 전후 비용 | 하강 속도·가속도와 충격을 다른 구간에서 계산 |
| 안정적인 지지 | BeamDojo의 발바닥 중첩, TactileStep의 면적·CoP | 기하학적 proxy와 실제 압력 측정을 구분 |
| 덜 부산스러운 동작 | [[2023 - ANYmal Parkour]]의 발·몸체 가속도, action rate | 진행을 멈춰 정규화 비용만 줄이는 해를 점검 |
| 탐색 유지 | [[2024 - DreamWaQ++ Multimodal Locomotion]]의 style reward 완화 | 움직임 비용이 목표 수행보다 지배적이지 않은지 확인 |

원문 위치: [StairMaster Method](https://arxiv.org/html/2606.25765v2), [Extreme Parkour §3.1](https://arxiv.org/html/2309.14341v1), [ANYmal Table S2](https://arxiv.org/html/2306.14874v1), [DreamWaQ++ §IV-F](https://arxiv.org/html/2409.19709v2), [BeamDojo Tables VII–VIII](https://arxiv.org/html/2502.10363v3), [TactileStep §3.3](https://arxiv.org/html/2609.28959v1).

## 적용 절차

1. **측정 계약부터 고정한다.** 발 위치가 링크 원점인지 collider 최저점인지, 속도가 세계좌표 물질점 속도인지, 힘이 합력인지 압력 분포인지 기록한다.
2. **접촉 조건을 구분한다.** 정상 스윙, 접촉 전 하강, touchdown, 하중을 받는 stance에 맞는 비용을 활성화한다. 추론: 사후 접촉 단계 판정은 미리 정한 보행 순서와 다르다.
3. **단위를 맞춘다.** 지속 비용은 초당 rate, 착지 한 번의 비용은 event amount로 정의한다. 실제 reward manager가 곱하는 $\Delta t$와 중복되지 않는지 확인한다.
4. **저장 궤적으로 크기를 점검한다.** 낮은 스윙·충분한 스윙·느린 하강·미끄럼·정상 정지·전진 중 정체를 비교한다. 빠르게 구간을 통과할수록 총 벌점이 감소하는 역효과도 검사한다.
5. **같은 조건으로 새 정책을 평가한다.** 완주·실패·timeout, 진행 거리, 명령 중 정체, 착지 안전도와 충격을 함께 제시한다. 완료하지 못한 구간은 평가하지 못한 것으로 남긴다.

이 절차의 단위·reset·노출 시간 점검은 [RBQ10 보상 검증 기록](/home/jay/RBQ10_RL_compare_ws/reports/stair-lift-penalty-20261027-01/verification.json)과 [명령 중 정체 분석](/home/jay/RBQ10_RL_compare_ws/reports/fused-joint-training-20261027-01/nonprogress16.json)에 근거한다. 일반화한 절차는 에이전트의 방법론적 정리다.

## RBQ10 발 높이 항의 기록

2026-10-27 추가한 구현은 다음과 같다. **아래 숫자는 RBQ10 설계값이며 논문에서 정한 보편값이 아니다.**

| 항목 | 해당 구현 |
|---|---|
| 요구 높이 | 가까운 다음 높은 상판 + 5cm. 해당 상판이 없으면 마지막 지지면 + 5cm |
| 스윙 비용 | 관측한 최고 높이의 부족분을 접촉 때 한 번 계산. `swing_clearance_rate` 가중치 −0.1 |
| 전혀 들지 않는 해 | 전진 명령 중 1.5초간 충분한 lift가 없으면 비용을 시작하고, 추가 1.5초에 걸쳐 상한으로 증가. `no_lift_cost` 가중치 −1 |
| 제외 조건 | 정상 STOP와 비활성 구간. 지지발 자체에는 스윙 높이 부족 비용을 적용하지 않음 |
| 당시 검증 | 테스트 74개와 기존 16개 실패 궤적 재계산. 이 기록의 optimizer update는 0 |

근거: [설정·검증 결과](/home/jay/RBQ10_RL_compare_ws/reports/stair-lift-penalty-20261027-01/verification.json), [실제 높이 판정 코드](/home/jay/RBQ10_RL_compare_ws/training/stair_lift_penalty.py).

충분히 든 뒤 느리게 내려오는 구간에 높이 부족 비용이 계속 쌓이지 않도록 최고점을 사용한다. 다만 제자리에서 충분히 드는 동작까지 전진으로 보장하지는 않으므로 진행 목적을 함께 확인해야 한다.

## 실패 해석에서 피할 것

- 발 속도 감소를 곧바로 안정적인 보행 개선으로 부르기. 정지한 정책도 값이 작다.
- 발판 접촉이 0회인 정책의 불안전 접촉률을 0%로 보고하기. 분모가 없으면 비교 불가다.
- 몸체가 특정 X 좌표를 넘은 구간만 집계해, 그 뒤 뒤로 밀린 정체를 누락하기.
- 초기 상태를 계단 중간에 배치한 부분 과제 성공을 전체 계단 완주로 합산하기.
- 합력·최저점으로 CoP·지지 면적을 실제 측정했다고 주장하기.

위 항목은 [단일 출력망 평가 기록](/home/jay/RBQ10_RL_compare_ws/reports/fused-joint-training-20261027-01/completed-run-report.json)의 해석 한계를 재사용 가능한 점검으로 정리한 것이다.

## 연결

- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌과 실험 맥락.
- [[Perceptive Legged Locomotion]], [[Terrain Memory for Legged Locomotion]] — 관측과 기억의 전제.
- [[index]] — 전체 카탈로그.
