---
type: method
status: active
created: 2026-11-03
updated: 2026-11-05
tags:
  - method
  - reinforcement-learning
  - manipulation
  - contact-simulation
  - gpu-simulation
sources:
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
  - https://arxiv.org/html/2610.13354v1
  - https://alpha-nist.github.io/
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
---

# AlphaNIST Binary-Reward Assembly

## TL;DR

다양한 조립 초기 상태를 저장한 reset bank, 성공률에 따른 샘플링, 공통 완료 보상으로 하나의 PPO 정책을 학습한다. 손의 접근·재파지·삽입 순서는 직접 지정하지 않는다. **Binary인 것은 task reward이며, 전체 보상에는 매 스텝 제어 비용이 포함된다.** 근거: [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]], §IV, Eqs. (3)–(6), Tier A.

## Problem Setting

[[NIST Assembly Task Board 1]]의 20개 assembly pair를 공유 정책으로 다룬다. 기본 실험은 에피소드마다 한 pair를 조립하는 multi-task 문제이고, 여러 pair를 한 에피소드에서 조립하는 실험은 별도로 학습한다. 관측의 표면 점군이 형상 차이를 전달하며 discrete task ID나 stage ID는 정책에 주지 않는다 (§III–IV).

## Procedure

1. **Reset bank 구성:** 조립 종류 $e_i$와 초기 simulator state $\bar s_i$를 함께 저장한다. Loose part, pickup, transport, near-mating, partially assembled 상태를 포함한다. 이 목록은 시작 상태의 범위이며 실행할 행동 순서가 아니다 (§IV-B).
2. **연습할 상태 선택:** 각 entry에서 최근 $L$회 에피소드의 성공률 $\hat p_i$를 추정하고 다음 가중치를 bank 전체에서 정규화한다. 중간 성공률의 상태를 더 자주 뽑되 $\varepsilon_q>0$으로 모든 entry의 선택 가능성을 남긴다 (Eq. 4).

$$
\mathcal D_{\mathrm{reset}}=\{(e_i,\bar s_i)\}_{i=1}^{M},\qquad
q_i\propto\varepsilon_q+\sqrt{\hat p_i(1-\hat p_i)}.
$$

3. **공통 완료 판정:** 현재 상대 pose와 완성된 조립 pose 사이의 논문상 assembly error $d_{\mathrm{asm}}^e$를 사용한다. 단일 pair에서는 다음 성공 보상을 한 번 지급하고 종료한다. $\epsilon=0.001\,\mathrm m$는 이 오차 정의의 임계값이다 (§IV-C, Eq. 5).

$$
r_t^{\mathrm{succ}}=\mathbf 1\!\left[d_{\mathrm{asm}}^e(s_{t+1})<\epsilon\right].
$$

4. **제어 비용 추가:** 모든 task에 같은 계수 $c$를 적용한다. Action, joint velocity, applied torque의 비용은 조립 중간 진척을 직접 보상하지 않는다. Horizon 또는 관절 속도·토크 한계 위반도 종료 조건이다 (Eq. 6).

$$
r_t=r_t^{\mathrm{succ}}
-c\left(\lVert a_t\rVert_2^2+\lVert\dot q_t\rVert_2^2+\lVert\tau_t\rVert_2^2\right),\qquad c\geq0.
$$

5. **Rollout와 PPO 갱신:** Isaac Lab에서 로봇 상태, 이전 action, part·mating geometry·robot의 표면 점군을 입력한다. Actor와 critic은 파라미터를 따로 가진 SimBa 네트워크다. 에피소드 결과로 reset 성공률을 갱신하고, 수집한 transition으로 공유 정책과 value를 학습한다 (§IV-D, Algorithm 1).
6. **관절 제어:** 7-DoF Franka Panda와 parallel-jaw gripper를 시뮬레이션한다. 정책은 25 Hz로 7D 상대 관절 목표 $q_t^{\mathrm{target}}=q_t+\Delta q_t$와 1D gripper 명령을 출력한다. 하위 implicit impedance controller는 libfranka stiffness/damping과 hardware-aligned dynamics를 사용한다 (§IV-D).
7. **병렬화:** 1K–256K 환경에서 synchronous PPO를 사용한다. Multi-GPU 실행은 GPU당 4K 환경이며 gradient를 평균한다. Iteration마다 환경당 32 step을 수집하고 5 epoch, epoch당 4 minibatch로 갱신한다 (§IV-E).

## Assumptions / Requirements

- 조립 geometry, 완성 pose, 유효한 중간 상태와 접촉을 재현하는 simulator가 필요하다. Demonstration action은 없지만 task 정의와 reset 설계라는 사전 정보는 있다 (§IV-B–C).
- Hardware-aligned 한계는 시뮬레이션 행동 범위를 제한한다. 실제 인지 오차·latency·접촉 모델 차이에 대한 성능 보장은 아니다 (§VI).
- 검증 필요: 공개 공식 구현으로 reset 생성·검증 세부와 $L$, $\varepsilon_q$, $c$를 확인해야 한다. 이 페이지에서 미기재 값을 추정하지 않는다.

## Inputs / Outputs

- 입력: reset bank와 성공 판정, 로봇 상태·이전 action·표면 점군. 별도의 stage label이나 expert action label은 사용하지 않는다 (§IV).
- 출력: 관절·gripper 명령을 내는 공유 정책. Regrasp, tapping, 주변 형상을 이용한 재배향은 관찰된 학습 행동이며 별도 primitive 목록이 아니다 (§V-C).
- Multi-pair 학습: 모든 active pair가 완료될 때만 task 보상을 지급한다. Pair 수마다 정책을 학습·평가하며 제한 시간은 pair당 15초다 (§V-D, Table I).

## Failure Modes

- **초기 상태와 전체 과제 혼동:** 부분 조립에서 시작한 성공도 보고 집계에 포함된다. Loose-part 시작의 전체 작업 성능은 별도로 확인해야 한다 (§V).
- **보상 일반화 과장:** 논문이 비교한 dense 조건은 reach·alignment 항을 각각 0.01로 더한 설정이다. 모든 dense reward가 열등하다는 결론은 아니다 (§V, Eq. 7).
- **구조 전이 과장:** 20개 학습 task를 공유하는 결과를 새로운 geometry나 실물 보드에 대한 일반화로 확대하지 않는다 (§VI).

## Evidence

64K 환경·25K iteration에서 공유 sparse 정책의 **학습 성공률 98.2%**, specialist 평균 81.4%를 보고한다. 별도의 256K scaling 평가에서는 beta sampling 97.4%, uniform sampling 84.3%다. 평가 분포와 절차가 다르므로 두 수치를 같은 지표로 합치지 않는다 (§V-A–B, Figs. 5–7).

10-pair 정책은 Table I에서 84%를 보고한다. 모든 결과는 simulation이며 20-pair 전체 보드 수행과 실물 검증은 향후 과제다 (§V-D–VI). 원자료 기록은 [[2026-10-09 - AlphaNIST Source]].

## Related Concepts

- [[Reset-State Curricula for Sparse-Reward RL]] — uses: 시작 상태의 범위와 연습 빈도를 분리한다.
- [[Object Singulation]] — 후속 조립을 위해 물체를 밀어 접근 가능한 위치로 옮기는 행동과 연결된다. 얽힌 물체 분리 benchmark를 검증한 결과는 아니다.
- [[Physical AI]] — 접촉 dynamics와 실제 배치 조건을 함께 다뤄야 하는 학습 사례.
- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] — answers: 이 학습 절차가 제공하는 조건부 근거와 전이 한계.

## Open Questions

- Reset bank에 없는 시작 상태·새 geometry·sensor point cloud에서도 성능을 유지하는가?
- Reset 생성 비용까지 포함하면 task 추가의 engineering 비용은 얼마나 감소하는가?
- 같은 interaction budget에서 bank coverage와 adaptive sampling의 기여를 어떻게 분리할 것인가?

## PolicyIK와의 목적·종료 조건 비교

[[PolicyIK Joint-Reference Control]]은 dense tracking·progress·dwell reward를 함께 쓰고, 허용 오차에 진입해도 종료하지 않아 지속 유지를 학습한다. AlphaNIST의 단일 pair 완료 시 1회 보상·종료와는 목적과 종료 조건이 다르다 ([[2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning]], §4.3, Eq. (7); AlphaNIST §IV-C).

추론: 두 결과는 특정 과제의 학습·평가 설계 사례로 비교해야 한다. 어느 한쪽만으로 모든 조작에서 sparse 또는 dense reward가 우월하다고 판단할 수 없다. [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]]에 이 구분을 연결했다.
