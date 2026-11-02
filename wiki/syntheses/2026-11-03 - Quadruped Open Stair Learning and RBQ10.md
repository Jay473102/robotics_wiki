---
type: synthesis
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [robotics, reinforcement-learning, perception, sim-to-real, policy-learning]
sources:
  - https://arxiv.org/html/2606.25765v2
  - https://arxiv.org/html/2309.14341v1
  - https://arxiv.org/html/2306.14874v1
  - https://arxiv.org/html/2409.19709v2
  - https://arxiv.org/html/2502.10363v3
  - https://arxiv.org/html/2609.28959v1
  - https://arxiv.org/html/2408.13740v3
  - https://arxiv.org/html/2603.03138v1
---

# Quadruped Open Stair Learning and RBQ10

열린 계단에 가장 직접적인 문헌은 **StairMaster**다. 나머지는 지각 입력, 기억, 엣지 회피, 발 높이, 부드러운 착지, 학습 구조를 비교하는 자료다. 추론: RBQ10에서는 신경망 구조 변경과 함께 실제 센서 경로·접촉 보상·저속 진행·정지를 각각 검증해야 한다.

## 범위와 읽는 순서

[기존 보상 설계 기록](/home/jay/RBQ10_RL_compare_ws/reports/literature-stairs-20261026-01/implementation.json)에서 확인한 **핵심 6편**과 [관련 구현 기록](/home/jay/RBQ10_RL_compare_ws/training/lf2wb/README.md)에 연결된 **PIE·LF2WB 2편**을 정리했다. 전체 분야를 빠짐없이 조사한 survey는 아니다.

1. 열린 계단의 직접 해법: [[2026 - StairMaster Hollow Stair Locomotion|StairMaster]].
2. 엣지·동작·착지 보상: [[2023 - Extreme Parkour with Legged Robots|Extreme Parkour]], [[2023 - ANYmal Parkour|ANYmal Parkour]], [[2024 - DreamWaQ++ Multimodal Locomotion|DreamWaQ++]], [[2025 - BeamDojo Sparse Foothold Locomotion|BeamDojo]], [[2026 - TactileStep Sole Tactile Locomotion|TactileStep]].
3. 동시 학습과 지형 기억: [[2024 - PIE Implicit-Explicit Parkour|PIE]], [[2026 - Look Forward to Walk Backward|LF2WB]].

## 논문 비교

| 문헌 | 대상 | 핵심 입력·구조 | 이번 과제에서 읽을 부분 |
|---|---|---|---|
| [[2026 - StairMaster Hollow Stair Locomotion|StairMaster]] | Go2, 열린 계단 | Depth·고유감각, cross-attention·SRU, 교사→학생→RL | Hollow·edge 비용과 센서 결손 |
| [[2023 - Extreme Parkour with Legged Robots|Extreme Parkour]] | A1, parkour | Scandots 교사→depth 학생, 단일 관절 정책 | 세계좌표 진행과 엣지 여유 |
| [[2023 - ANYmal Parkour|ANYmal Parkour]] | ANYmal D, 장애물 | Depth·LiDAR 지형 표현, 여러 기술과 상위 정책 | 발·몸체 가속도, 정체·정지 목적 |
| [[2024 - DreamWaQ++ Multimodal Locomotion|DreamWaQ++]] | 4족, 장애물·계단 | 점군·고유감각 기억과 융합 | Style reward 완화와 센서 신뢰도 |
| [[2025 - BeamDojo Sparse Foothold Locomotion|BeamDojo]] | G1, 드문 발판 | Elevation map, 두 단계 RL·두 critic | 발바닥 중첩과 발 높이 |
| [[2026 - TactileStep Sole Tactile Locomotion|TactileStep]] | G1, 착지·지지 | Depth·고유감각·발바닥 촉각 | 접촉 단계, 충격·면적·CoP |
| [[2024 - PIE Implicit-Explicit Parkour|PIE]] | Lite3, parkour | Depth 추정기와 비대칭 PPO 동시 학습 | 명시·암묵 추정과 12차원 관절 출력 |
| [[2026 - Look Forward to Walk Backward|LF2WB]] | Lite3, 전후진 | 전방 depth·Delta-rule 지형 기억 | 가림 이후 기억 유지와 비교 실험 |

표의 출처는 각 논문 페이지의 버전 고정 원문 링크다. BeamDojo와 TactileStep은 **휴머노이드** 문헌이므로 4족의 발 형상·지지 패턴에 맞춘 해석이 필요하다.

## 이 묶음에서 읽히는 흐름

추론: 외부 지각을 추가하는 것에서 더 나아가, 현재 보이지 않는 지형의 기억과 관측 신뢰도를 다루고, 완주와 별도로 발 접촉 품질을 최적화하는 방향이 보인다. Teacher–student와 단일 단계 비대칭 학습이 함께 사용되므로 어느 하나만을 최근의 유일한 방식으로 정리하지 않는다.

여기서 혼동하기 쉬운 세 가지는 다음과 같다.

- **Depth 미사용과 특권 지도 미사용은 다르다.** [[2026-11-03 - Does Quadruped RL Need Depth Cameras]]
- **기억 구조와 안전한 발 디딤 목적은 다르다.** [[2026-11-03 - Why Does Memory Not Prevent Stair Edge Contacts]]
- **관절 PD와 상위 보행 계획기는 역할이 다르다.** 직접 관절 출력을 학습해도 하위 PD를 사용할 수 있다. [[Perceptive Legged Locomotion]]

## RBQ10에서 실제 확인한 범위

아래는 **2026-10-27의 특정 실험 기록**이다. 논문의 성능 수치나 2026-11-03 현재 모든 프로젝트 분기의 상태를 대표하지 않는다.

| 항목 | 해당 기록 |
|---|---|
| 학습 | 단일 12관절 출력망, 전체 actor 학습 가능, 120 update·3,932,160 transition |
| 과제 | 15cm 계단, 명령 0.2m/s, 제한 60초, 마지막 안정 정지 5초 |
| 동일 평가의 기존 정책 | 3/16 완주 |
| 새 단일 출력망 | 0/16 완주, 16/16 timeout |
| 명령 중 정체 | 새 정책은 실제 계단 정책 활성 구간의 약 89.3%에서 세계좌표 전진 속도 절댓값이 0.03m/s 미만 |

근거: [완료 보고서](/home/jay/RBQ10_RL_compare_ws/reports/fused-joint-training-20261027-01/completed-run-report.json), [정체 노출 시간 분석](/home/jay/RBQ10_RL_compare_ws/reports/fused-joint-training-20261027-01/nonprogress16.json). 공통으로 완료한 계단 진행 구간이 없어 발판 안전도 개선을 같은 거리에서 비교할 수 없었다. 발이 조용해진 것은 이 시험에서 보행 개선을 뜻하지 않았다.

그 뒤 추가한 발 높이·no-lift 비용은 **테스트와 기존 궤적 재계산**으로 확인했다. [해당 검증 기록](/home/jay/RBQ10_RL_compare_ws/reports/stair-lift-penalty-20261027-01/verification.json)은 새 학습 update가 0임을 명시한다. 따라서 이 기록으로 높이 보상 추가 후 완주율이 개선됐다고 주장할 수 없다.

## 다음 검토에 재사용할 내용

[[Open Stair Reward Design and Evaluation]]에 문헌별 보상 목적, 활성 조건, 시간 단위와 실패 해석을 정리했다. 우선 확인할 것은 안전 접촉 비용을 줄이면서도 실제로 진행하는지, 충분히 들고 천천히 내려놓는지, 오른쪽 앞발을 포함해 발별 결과가 균형적인지다. 이는 앞으로 평가할 질문이며 여기서 개선을 확정하지 않는다.

## 연결

- [[2026-11-03 - Chat Quadruped Open Stair Learning]] — 질문과 출처 추적.
- [[Perceptive Legged Locomotion]], [[Terrain Memory for Legged Locomotion]] — 공통 개념.
- [[Embodied AI]], [[Physical AI]] — 기존 위키의 상위 주제.
- [[index]] — 논문·출처 전체 목록.
