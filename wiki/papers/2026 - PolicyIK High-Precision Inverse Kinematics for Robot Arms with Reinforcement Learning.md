---
type: paper
status: active
created: 2026-11-05
updated: 2026-11-05
tags: [paper, reinforcement-learning, robot-learning, manipulation, vla]
sources:
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
  - https://arxiv.org/abs/2611.05372v1
  - https://tinaliu0123.github.io/PolicyIK/
  - https://github.com/Tinaliu0123/PolicyIK/tree/3459223d3cd523c9e35875f6567787ff0ffe9788
title: "PolicyIK: High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning"
authors: [Yuhan Liu, Xinqi Liu, Zixuan Dong, Keith W. Ross, Shenji Wan]
year: 2026
venue: arXiv preprint
doi: 10.48550/arXiv.2611.05372
url: https://arxiv.org/abs/2611.05372v1
---

# PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning

## TL;DR

목표 end-effector pose에 **도달하고 유지하는** 관절 reference 제어기를 RL로 학습한다. 누적 명령 상태를 관측하고, 미세 오차용 표현·gain·지속 보상을 결합한다. Simulation 단일 시도 strict success는 93.49%, 재시도 포함은 98.92%다. 실물 OpenArm에서는 25초 안에 60과제 중 54개에 도달하고 43개를 마지막 5초 동안 유지했다. **Simulation strict는 평균 오차, 실물 holding은 구간 전체 오차 기준이며 실물 계측은 encoder+FK다.** [§4–5, Tables 1, 3]

## Problem

기하학적으로 맞는 관절 해라도 유한한 servo gain, 중력, 마찰, 관절 한계 때문에 실제 end-effector가 목표에서 벗어날 수 있다. 이 논문은 joint reference를 계속 수정하는 closed-loop IK를 다루며, 목표 근처로 이동하는 능력과 정밀하게 머무는 능력을 별도로 평가한다. [§1, §3]

## Core Idea

이전 reference $z_{t-1}$에 정책 action을 누적한다. 관측에 $d_t=z_{t-1}-q_t$를 포함하여, 측정 관절값이 같아도 servo command가 다를 수 있다는 사실을 정책에 전달한다. Action이 0이면 reference가 유지되므로 중력 등을 보상하는 offset을 보존할 수 있다. [§4.1]

$$
z_t=\operatorname{clip}\!\left(z_{t-1}+\eta\,\beta(e_p,e_R)a_t,\;q_{\mathrm{lo}},q_{\mathrm{hi}}\right).
$$

추론: 이는 goal pose에서 기하학적 joint solution 하나를 출력하는 모델보다, 실행 중의 servo 상태와 오차를 함께 다루는 [[Learned Closed-Loop Inverse Kinematics]]로 이해하는 편이 정확하다. Jacobian·온라인 최적화가 실행 경로에 필요 없다는 설명은 FK나 robot model도 필요 없다는 뜻이 아니다.

## Method

- **관측:** 7-DoF simulation의 54D 입력에는 joint position/velocity, goal position, keypoint 차이, coarse/fine pose error, best-so-far 정보, command-state gap, 이전 action이 들어간다. Actor와 critic이 같은 관측을 쓴다. [§4.2, Appendix A]
- **정밀 제어:** coarse 오차 scale은 1 cm·20°, fine은 0.5 mm·0.25°다. 위치·방향 오차에 따라 action gain을 줄여 이동 속도와 목표 근처의 미세 조정을 조절한다. [§4.1–4.2]
- **Dense reward:** tracking + progress + dwell에서 motion·joint-limit 비용을 뺀다. Best-so-far progress는 같은 오차 개선을 반복 보상하지 않도록 구성한다. 1 mm·0.2° 안에 머무는 매 step에 dwell reward를 지급하고 **성공 즉시 종료하지 않는다**. [§4.3, Eq. (7), Appendix B]
- **Simulation PPO:** 4,096개 환경, policy 30 Hz·physics 60 Hz, 12초 rollout 안에서 4초마다 goal을 바꾸고 arm은 reset하지 않는다. 13,000 epochs, 약 12.8억 transitions를 사용한다. 배포 actor는 256-unit ELU 두 층이며 마지막 20개 저장 checkpoint를 exponential weighting으로 평균한다. [§4.4, Appendices A–B]
- **실물 학습:** OpenArm에서는 직접 FlashSAC+HER로 학습하며 near-goal/reverse curriculum과 latent-alignment critic을 사용한다. 120,000 online transitions 외에 scripted large-rotation 150과제·22,500 demonstration transitions를 사용하고 replay batch의 25%를 demo에서 가져온다. Simulation PPO 정책을 그대로 이전한 결과가 아니다. [§4.5, Appendix H]

수식·구현 조건은 [[PolicyIK Joint-Reference Control]]에 정리했다.

## Data / Embodiment

- Main simulation은 7-DoF OpenArm이다. 200,000개 sampled joint configuration에서 FK pose를 만들고 floor/self-collision 등을 필터링하여 train start 157,504개, train goal 104,599개를 구성한다. [Appendix A]
- 평가는 collision-free start–goal 4,120쌍으로 고정한다. 학습 configuration과 겹치지 않으며 eval goal이 train goal과 위치 1 mm·방향 0.2° 둘 다 가까운 경우를 배제한다. 같은 workspace의 분포 내 held-out 평가이며 새로운 로봇 일반화 평가는 아니다. [Appendices A, C]
- 학습 중 joint position/velocity noise는 uniform ±0.01이며 main simulation 평가는 관측 noise가 없다. [Appendix A]
- VLA 실험은 side-mounted OpenArm용으로 정책을 다시 학습한다. xArm7에서도 simulation-trained·hardware-trained 정책을 별도로 만든다. [Appendices G, J]

## Evaluation

Simulation 1회는 160 step, 약 5.3초다. **Strict success**는 마지막 30 step(1초)의 평균 위치·방향 오차가 각각 1 mm·0.2° 이내인 경우다. Coarse threshold는 1 cm·2°다. **Containment**는 마지막 1초의 모든 sample이 strict threshold 안에 있는 별도 지표다. ±는 학습 seed 3개의 평균±표본 표준편차이며, median error는 실패도 포함한 모든 task에서 계산한다. [§5.1, Appendix C]

Deployment는 원래 시작 상태로 reset한 뒤 corrected-goal과 transient-goal retry를 수행한다. 성공 판정은 원래 goal을 기준으로 하며 첫 성공 attempt, 성공이 없으면 마지막 attempt를 집계한다. Transient retry는 최대 8회다. 따라서 deployment 수치를 단일 시도 baseline과 같은 시간 예산의 성능으로 읽지 않는다. [Appendix C]

## Results

### Simulation pose control

| Controller | Strict success (%) | Median position (mm) | Median orientation (°) | 평균 attempt 수 |
|---|---:|---:|---:|---:|
| DLS | 50.41 | 0.94 | 0.15 | 1.000 |
| QP | 56.21 | 0.57 | 0.11 | 1.000 |
| MPC | 56.33 | 0.54 | 0.10 | 1.000 |
| PolicyIK | 93.49±0.20 | 0.25±0.02 | 0.04±0.00 | 1.000 |
| PolicyIK + deployment | 98.92±0.23 | 0.25±0.02 | 0.04±0.00 | 1.212 |

근거: Table 1. 단일 시도 containment는 92.4%다. 성공 task의 마지막 1초 **net motion** 중앙값은 14 μm·0.002°이며 이를 최대 진동폭이나 외부 계측 정확도로 바꿔 해석하지 않는다. Actor forward의 0.035 ms는 AMD EPYC 9454의 CPU core 하나에서 batch 1인 결과이며 전체 제어 loop latency가 아니다. [§5.1.1]

Command-state feedback 제거 시 strict는 84.26%, 그 상태에서 reference를 measured joint에 다시 붙이면 30.77%다. 마지막 variant는 coarse success 95.9%로, 대략 도달하는 것과 정밀 유지가 다를 수 있음을 보인다. Fine pose/gain 제거는 각각 strict success를 약 4–5%p 낮춘다. [§5.1.2, Table 7]

### VLA controller integration

고정 pi0.5-LIBERO와 공통 Panda operational-space model adapter를 사용해 변형한 LIBERO-Object 10과제를 평가했다. 과제당 50개 initial state×3 runs, 총 1,500 episode다. PolicyIK는 95.7%, hand-tuned DLS는 96.7%, default DLS와 hand-tuned QP는 각각 90.8%다. **VLA 하위 제어기로의 호환성을 보이지만 모든 튜닝 baseline보다 높은 결과는 아니다.** [§5.1.3, Table 2, Appendix G]

### Real OpenArm

| Controller | Reached / 60 | Held / 60 | Median position (mm) | Median orientation (°) |
|---|---:|---:|---:|---:|
| DLS | 48 | 17 | 0.65 | 0.13 |
| Resolved-rate QP | 48 | 16 | 0.57 | 0.14 |
| Kinematic MPC | 46 | 15 | 0.81 | 0.18 |
| Adapted OpenArm QP | 32 | 11 | 0.99 | 0.23 |
| PolicyIK | 54 | 43 | 0.50 | 0.12 |

근거: Table 3, 60 full-pose tasks·25초 budget(40초 trial의 첫 25초 평가). Reached는 1 mm·0.2°를 연속 0.5초 이상 만족한 적이 있는 경우, held는 **마지막 5초 전체**에서 두 threshold를 만족한 경우다. Median은 각 task 마지막 1초 평균 오차의 task 간 중앙값이다. 15초 budget의 마지막 5초 holding은 27/60으로 낮아진다. 오차는 modeled gripper frame에서 encoder+FK로 계산한다. [§5.2, Appendices H.7, I]

### xArm7 transfer scope

xArm7용으로 별도 학습한 simulation·hardware 두 정책은 standard 60과제와 large-rotation 60과제에서 각각 60/60을 기록한다. 40초 trial 중 20–25초 구간을 1 mm·0.2° holding으로 판정하며 controller/task당 1회다. Standard set에서는 DLS/QP/MPC도 60/60이고 일부 baseline의 median error가 더 작다. 따라서 다른 로봇에서 같은 학습 설계를 적용할 수 있다는 근거이며, OpenArm 정책의 zero-shot 전이나 모든 정밀도 지표의 우월성을 보인 것은 아니다. [Appendix J, Table 13]

## Limitations

- **계측:** encoder+FK의 작은 오차는 calibration·link flex·tool offset까지 포함한 외부 Cartesian 정확도를 보증하지 않는다. [§5.2, Appendices H.7, I]
- **비교 조건:** OpenArm PolicyIK는 10 Hz, classical controller는 50 Hz이며 reference lead bound·관절 margin도 다르다. 같은 task와 시간·FK 지표를 사용하지만 제어기의 실행 제약이 완전히 같지는 않다. [Appendix H.5, Table 11, Appendix I]
- **범위:** 분포 내 pose task, 재학습한 mount·robot별 정책, 변형한 VLA benchmark의 결과를 미지 환경·장애물 회피·새 morphology 전체로 확대하지 않는다. [Appendices A, G, J]
- **검증 수준:** 공개 코드 문서를 확인했지만 자체 학습·실험을 재현하지 않았다. Hardware의 여러 training seed에 걸친 불확실성도 확인되지 않았다.

## Connections

- [[Learned Closed-Loop Inverse Kinematics]] — pose 오차와 내부 command state를 포함한 제어 개념.
- [[PolicyIK Joint-Reference Control]] — action·observation·reward·배포 절차.
- [[Vision-Language-Action Models]] — VLA의 pose action을 실제 joint reference로 실행하는 하위 계층.
- [[Reset-State Curricula for Sparse-Reward RL]] — near-goal 경험 분배와 실제 task 시작 분포의 구분. PolicyIK 하드웨어에는 demo replay도 있다.
- [[AlphaNIST Binary-Reward Assembly]] — 성공 시 종료하는 sparse assembly objective와 dense tracking·지속 유지 objective의 차이.
- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] — 보상 효과를 과제·종료·초기화 조건별로 해석해야 하는 보강 사례.
- [[2026-11-05 - How Should Pose Reaching and Holding Be Evaluated]] — 평균 오차·지속 유지·재시도·실물 계측을 분리하는 평가 질문.
- [[2026-11-03 - PolicyIK Source]] — 원본·버전·annotation·공식 구현 확인 기록.

## Contradictions / Updates

- 2026-11-05: v1을 바탕으로 생성했다. AlphaNIST의 sparse reward 결과와 PolicyIK의 dense reward 결과는 목적·과제·평가가 달라 직접적인 반증 관계로 보지 않는다.

## Notes / Marginalia

공개 원본의 Link annotation 외 필기·강조 subtype을 발견하지 못했다. 검사 방법과 한계는 source note에 기록했다.

## Open Questions

- 외부 pose 계측, payload 변화, 장기 drift에서도 FK 기준 이점이 유지되는가?
- 동일한 command 제약·총 시간·retry budget으로 비교하면 reaching과 holding의 이점은 각각 얼마나 남는가?
