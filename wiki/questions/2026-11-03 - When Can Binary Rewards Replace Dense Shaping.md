---
type: question
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [question, reinforcement-learning, robot-learning, manipulation]
sources:
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
  - https://arxiv.org/html/2610.13354v1
---

# When Can Binary Rewards Replace Dense Shaping

## Short Answer

**완료 보상만으로 학습 신호를 얻을 기회가 충분할 때 유효한 대안이 될 수 있다.** AlphaNIST는 성공에 가까운 상태까지 포함한 reset bank, 성공률 기반 sampling, 다양한 조립 과제와 대규모 PPO 경험 수집을 함께 사용했다. 따라서 이 결과는 기존 문제에서 중간 보상만 지우면 학습이 좋아진다는 근거가 아니다. [§IV–V]

## Why This Question Matters

중간 보상은 탐색을 돕지만, 목표와 다른 중간 상태를 좋아하게 만들 수도 있다. 특히 여러 형상을 한 정책으로 학습할 때 같은 reach/alignment 항이 유용한 행동을 일관되게 유도하는지 확인해야 한다. AlphaNIST 저자들은 이런 충돌을 결과의 **가능한 설명**으로 제시했으며, 충돌 원인을 완전히 분리한 증명으로 제시하지 않았다. [§V-A]

## Current Answer

| 질문 | AlphaNIST에서 확인한 내용 | 다른 문제에 적용할 때 남는 질문 |
|---|---|---|
| 성공을 한 번이라도 경험할 수 있나? | in-hand·near-mating·partial assembly reset 포함 | 실제 배포 시작 상태까지 이어지는 학습 경로가 있는가? |
| 어려운 상태에 경험을 배분하나? | 성공률이 중간인 reset을 더 자주 선택하되 모든 상태에 양의 확률 유지 | 희귀 실패·거의 불가능한 상태를 영구히 배제하지 않는가? |
| 중간 목적이 서로 충돌하나? | joint dense가 joint sparse보다 낮은 성공률 | 현재 shaping이 실제로 최종 목표와 충돌한다는 근거가 있는가? |
| 운동 비용은 없애도 되나? | action·관절 속도·토크 비용과 한계 초과 종료는 유지 | 과제 진행과 에너지·충격·안전 목적을 어떻게 분리할 것인가? |
| 성공률의 분모가 같은가? | 혼합 reset 평가와 학습 중 성공률을 구분 | 항상 정상 초기 상태에서 시작한 전체 과제 성공도 별도 측정하는가? |

## RBQ10 / Locomotion에 대한 연결

**추론:** [[Open Stair Reward Design and Evaluation]]에 적용하려면 기존 보상을 한 번에 삭제하기보다 reset coverage, sampling, 진행 shaping을 각각 분리한 ablation이 필요하다. AlphaNIST의 조립 결과는 계단 보행의 접촉 안정성이나 착지 충격 비용이 불필요함을 보이지 않는다.

재사용 가능한 검증 질문은 다음과 같다.

1. 같은 관측·초기화·예산에서 완료 목적과 현재 shaping의 우열을 비교했는가?
2. 계단 중간 reset에서의 부분 과제 성공과 바닥에서 시작한 전체 완주를 따로 보고했는가?
3. 학습 성공률 외에 정체, timeout, 넘어짐, 접촉 위치, 착지 충격을 함께 기록했는가?
4. reset·sampling 변경의 효과를 보상 변경의 효과로 잘못 해석하지 않았는가?

이 질문들은 에이전트의 실험 설계 제안(Tier C)이다. RBQ10에서 sparse-only 보상의 우월성을 검증한 결과가 아니다.

## Evidence / Sources

- [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]] — Eqs. (4)–(7), Figs. 5–7의 조건별 결과.
- [[AlphaNIST Binary-Reward Assembly]] — 완료 보상 외에 유지되는 제어 비용과 학습 절차.
- [[Reset-State Curricula for Sparse-Reward RL]] — 초기 상태·경험 배분·목표의 분리.

## Important Caveats

논문은 시뮬레이션 결과다. 98.2% 학습 성공, frozen mixed-reset 평가, 별도 10-pair 정책의 84% 성공을 하나의 공통 성능 지표로 합치지 않는다. dense baseline도 특정 두 shaping 항과 고정 계수에 국한된다.
