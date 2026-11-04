---
type: concept
status: active
created: 2026-11-03
updated: 2026-11-05
tags:
  - reinforcement-learning
  - robot-learning
  - manipulation
  - contact-simulation
sources:
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
  - https://arxiv.org/html/2610.13354v1
  - https://alpha-nist.github.io/
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
---

# Reset-State Curricula for Sparse-Reward RL

## Definition

에피소드의 시작 상태 분포를 설계하거나 학습 진척에 따라 재가중하여 sparse task reward를 만날 기회를 만드는 접근이다. 여기서 curriculum은 반드시 사람이 정한 단계 순서를 뜻하지 않는다. AlphaNIST는 cached reset coverage와 adaptive sampling을 결합하지만 정책에 stage ID나 행동 순서를 주지 않는다. 근거: [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]], §IV-A–B, Tier A.

## Why It Matters

완료 순간에만 task reward가 생기면 초기 정책이 유용한 접촉 상태를 거의 방문하지 못할 수 있다. AlphaNIST의 bank는 느슨하게 놓인 물체부터 in-hand·partial assembly까지 포함한다. [프로젝트 설명](https://alpha-nist.github.io/)은 near-complete reset이 전체 작업을 해결하기 전에도 마무리 동작을 연습하게 한다고 설명한다. 이는 expert action trajectory를 제공하는 것과 다르다.

## Key Ideas

### 상태 범위, 연습 빈도, 목표를 분리한다

| 구성 요소 | 결정하는 것 | AlphaNIST 사례 |
|---|---|---|
| Reset bank | 어떤 시작 상태를 사용할 수 있는가 | 조립 종류와 robot·board·part 초기 상태의 cache |
| Sampling rule | 각 상태에서 얼마나 자주 연습하는가 | 최근 성공률에 따른 beta sampling |
| Task reward | 무엇을 완료로 인정하는가 | 완성된 조립과의 오차가 임계값 미만 |
| Control cost | 어떤 제어 출력을 억제하는가 | action 크기·관절 속도·토크 비용 |

근거: §IV, Eqs. (3)–(6). 이 구분을 유지해야 reward 변경과 training-distribution 변경의 효과를 혼동하지 않는다.

### 정책의 현재 능력에 맞춰 빈도를 바꾼다

AlphaNIST는 entry $i$의 최근 $L$회 성공률 $\hat p_i$를 이용한다.

$$
q_i\propto\varepsilon_q+\sqrt{\hat p_i(1-\hat p_i)},\qquad\varepsilon_q>0.
$$

가중치는 $\hat p_i=0.5$에서 가장 크고, 확실히 성공하거나 계속 실패하는 상태도 선택 가능성이 남는다. 새로운 episode outcome이 성공률과 다음 reset 확률을 바꾼다. Uniform ablation은 동일 bank에서 $q_i=1/M$로만 바꾼다 (§IV-B).

추론: 이 가중치는 학습에 유용할 가능성을 성공률로 근사한다. 실제 gradient 개선량을 측정하거나, bank에 없는 상태를 새로 생성하는 규칙은 아니다.

### No demonstrations는 no priors가 아니다

AlphaNIST는 expert action, scripted manipulation primitive, 정책의 stage label을 쓰지 않는다. 그러나 다음 정보는 학습 전에 공급된다 (§III–IV).

- 조립 부품과 mating geometry, 완성된 상대 pose.
- 접촉·관절 제약을 포함한 simulator와 robot model.
- Pickup, transport, near-mating 등을 포함하는 reset coverage.
- 성공 임계값, 제어 비용과 종료 조건.

따라서 “어떻게 움직일지 가르치지 않는다”와 “문제에 대한 사전 정보를 전혀 주지 않는다”는 서로 다른 주장이다. Reset bank가 expert trajectory가 아니라는 점도, 유용한 상태를 만드는 engineering이 사라졌다는 뜻은 아니다.

### 평가 시작 분포를 따로 고정한다

AlphaNIST scaling 평가는 학습 중 sampling weight를 그대로 쓰지 않고 frozen mixed-reset bank에서 task별 uniform sampling을 사용한다. Stochastic action으로 task당 32회, 5 evaluation seed를 실행한다. 성공률은 여러 reset family를 함께 포함하므로, 모든 에피소드가 loose part에서 시작한 값으로 읽으면 안 된다 (§V, Fig. 7).

추론: bank 전체 평균과 함께 시작 상태 종류별 성공률·완료 시간·실패 원인을 나누면 부분 수행 능력과 전체 작업 능력을 구분하기 쉽다. 이는 재사용 가능한 평가 제안이며 이 논문의 추가 실험 결과는 아니다.

### 다른 로봇에 옮길 때의 조건

추론: [[Open Stair Reward Design and Evaluation]]처럼 중간 초기화가 가능한 문제에서도 “시작 상태가 물리적으로 유효한가”, “그 상태까지 실제로 도달 가능한가”, “중간 시작의 성공을 전체 완주로 집계하는가”를 점검할 수 있다. 조립에서의 binary reward 결과만으로 보행의 접촉·지지·진행 보상을 제거할 근거가 생기지는 않는다.

검증 필요: 임의 상태로 재설정하기 어려운 실물 시스템, 낙하·충돌이 비가역적인 과제, 새로운 morphology에서 동일 전략이 얼마나 유효한지는 별도 근거가 필요하다. AlphaNIST 자체의 결과는 simulation에 한정된다 (§VI).

## Related Papers

- [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]] — diverse resets와 SGS를 20-task 공유 조립 정책에 결합한 사례.
- [[2026-10-09 - AlphaNIST Source]] — 원자료와 검증 범위를 보존한 source note.

## Related Concepts

- [[AlphaNIST Binary-Reward Assembly]] — implemented-by: bank·sampler·보상을 분리한 실제 학습 절차.
- [[NIST Assembly Task Board 1]] — evaluated-on: reset·episode 조건을 명시해야 비교 가능한 조립 benchmark.
- [[Physical AI]] — simulator 초기화 편의와 실제 시스템의 실행 조건 사이의 차이를 다룬다.
- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] — answers: sparse objective가 성립하는 조건과 검증 항목.

## Contradictions / Updates

- 2026-11-03: AlphaNIST v1을 바탕으로 생성했다. Reset curriculum을 expert demonstration이나 미리 지정한 조작 단계와 동일시하지 않으며, 이 문서의 타 과제 적용 제안은 `추론:`으로 구분했다.

## Open Questions

- Reset 생성·검증 비용과 학습 GPU 비용을 함께 계량하면 어느 부분이 병목인가?
- Near-goal 상태의 학습이 loose-start 전체 작업으로 연결되지 않을 때 무엇을 바꿔야 하는가?
- 평가 bank와 학습 bank의 중복, 새로운 geometry, 실제 시작 분포를 어떻게 분리해 보고할 것인가?

## PolicyIK의 near-goal curriculum과 비교

[[PolicyIK Joint-Reference Control]]의 OpenArm 실물 학습은 목표 근처 시작에서 범위를 넓히는 reverse curriculum과 near-goal replay를 사용한다. 하지만 dense tracking·progress·dwell reward 및 scripted demonstration replay도 함께 쓴다. Demo 150과제·22,500 transitions에서 batch의 25%를 가져오므로 AlphaNIST의 demonstration-free reset bank와 동일한 조건이 아니다 ([[2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning]], §4.5, Appendix H; Tier A).

추론: 성공 근처 경험을 늘리는 학습 분포 설계는 sparse-only objective에만 쓰이는 기법이 아니다. Reset 분포·replay 분포·시범 데이터·보상 목적을 따로 기록해야 각 요소의 기여를 해석할 수 있다. 도달과 지속 유지의 평가 차이는 [[2026-11-05 - How Should Pose Reaching and Holding Be Evaluated]]를 참고한다.
