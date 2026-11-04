---
type: method
status: draft
created: 2026-11-05
updated: 2026-11-05
tags:
  - method
  - robotics
  - manipulation
  - reinforcement-learning
  - robot-learning
  - robot-dynamics
sources:
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
  - https://arxiv.org/html/2611.05372v1
---

# PolicyIK Joint-Reference Control

## TL;DR

PolicyIK는 목표 pose를 관절 해 하나로 변환하는 대신, pose 오차와 이전 관절 명령을 관측하며 joint-position reference를 반복 갱신하는 goal-conditioned RL 제어 방법이다. 누적 reference, 허용 오차 규모의 관측·action gain, progress와 dwell 보상을 결합해 도달 후 정지를 학습한다. 아래는 v1 논문의 구현·실험 근거(Tier A)이며, 모든 로봇에 공통인 최적 설계라는 의미는 아니다. [원문 §§3–4](https://arxiv.org/html/2611.05372v1)

## Problem Setting

7-DoF 고정식 팔의 목표는 $T_g=(R_g,p_g)\in SE(3)$이며, measured joint state $(q_t,\dot q_t)$로부터 $T_t=FK(q_t)$를 계산한다. 위치 허용 오차는 $1\,\mathrm{mm}$, 회전각 허용 오차는 $0.2^\circ$다. 정책 아래에는 reference를 추종하는 PD position controller가 있다. 초기 reference는 측정 관절값으로 초기화한다. [원문 §3, App. A](https://arxiv.org/html/2611.05372v1)

## Procedure

### 1. 명령을 누적하고 command state를 관측한다

$$
z_t=\operatorname{clip}\!\left(z_{t-1}+\eta\,\beta(e_p,e_R)a_t,\ q^{lo},q^{hi}\right),\qquad d_t=z_{t-1}-q_t.
$$

$a_t$는 7차원 joint-reference increment, $\eta$는 action scale이다. $a_t=0$이면 직전 reference가 유지된다. measured-joint anchor인 $q_t+\Delta q_t$와 달리, 정지에 필요한 command–measurement offset을 매 스텝 다시 만들 필요가 없다. 같은 $q_t$와 action도 $z_{t-1}$에 따라 다른 다음 상태를 만들므로 $d_t$를 actor와 critic에 준다. [원문 §4.1, Eq. 2–3](https://arxiv.org/html/2611.05372v1)

시뮬레이션 관측은 $(q_t-\bar q,\dot q_t,p_g,\Delta k_t,v_t^c,v_t^f,h_t,d_t,a_{t-1})$의 54차원 연결이다. $h_t$는 아래 running-best error를 드러내는 관측이다. 보상과 transition에 필요한 이력을 명시적으로 입력한다.

### 2. 큰 이동과 미세 오차를 별도 규모로 표현한다

세 개의 비공선 local keypoint $c_i$에서 $\Delta k_{i,t}=(p_g+R_gc_i)-(p_t+R_tc_i)$를 계산한다. 추가로 current end-effector frame의 translation 및 rotation-vector error를 두 scale로 정규화하고 $[-1,1]$로 clip한다. [원문 §4.2, Eq. 4–5](https://arxiv.org/html/2611.05372v1)

| 관측 scale | Translation | Rotation |
|---|---:|---:|
| Coarse | $1\,\mathrm{cm}$ | $20^\circ$ |
| Fine | $0.5\,\mathrm{mm}$ | $0.25^\circ$ |

회전 오차 $0.2^\circ$는 coarse 범위의 1%지만 fine 범위의 80%다. 전체 workspace 분산으로만 normalization하면 작아지는 terminal residual을 별도 채널로 드러내는 설계다.

### 3. 오차가 작아지면 reference 갱신 gain을 낮춘다

$$
\beta=\max\{G(e_p;l_p,u_p),G(e_R;l_R,u_R)\},\quad
G(e;l,u)=\beta_{\min}+(1-\beta_{\min})\operatorname{clip}\!\left(\frac{e-l}{u-l},0,1\right).
$$

두 오차 중 하나라도 upper threshold를 넘으면 full gain이고, 둘 다 lower threshold 아래면 minimum gain이다. 시간에 따른 annealing이 아니라 현재 오차에 따라 미세 제어가 활성화된다. 시뮬레이션은 $\eta=0.0625$, $\beta_{\min}=0.1$, $(l_p,u_p)=(0.5,9.31)\,\mathrm{mm}$, $(l_R,u_R)=(0.415,2.328)^\circ$를 쓴다. [원문 Eq. 6, App. A](https://arxiv.org/html/2611.05372v1)

### 4. 접근, 새 최저 오차, 체류를 각각 보상한다

$$
\rho_t=\max\!\left(\frac{e_p(t)}{1\,\mathrm{mm}},\frac{e_R(t)}{0.2^\circ}\right),\quad
b_t=\min(b_{t-1},\rho_t),\quad
r_t=r_t^{track}+r_t^{progress}+r_t^{dwell}-c_t^{motion}-c_t^{limit}.
$$

- Tracking은 위치 거리와 keypoint-distance kernel의 dense reward로 접근을 유도한다.
- Progress는 $[U(\rho_t)-U(b_{t-1})]_+$의 new-best improvement, potential shaping, best-so-far 대비 backslide cost를 포함한다. $U$는 $\rho=1$ 주변에서 급격히 커지며 같은 정확도 수준을 반복 달성하는 것에 중복 improvement를 지급하지 않는다.
- $h_t=[\operatorname{clip}(b_{t-1}/20,0,1),\operatorname{clip}((\rho_t-b_{t-1})/20,0,1)]$로 reward history를 관측한다. 새로운 목표에서 running best를 초기화한다.
- Dwell은 $\mathbf{1}[\rho_t\leq1]$로 허용 오차 안에 머무는 매 스텝을 보상한다. 성공 직후 종료하지 않고 timeout까지 실행한다.
- Motion cost는 action 변화와 joint velocity를, limit cost는 접근 중 관절 한계 근접을 억제한다. Limit cost는 $\rho_t>10$에서만 적용한다.

따라서 PolicyIK를 binary-only reward RL로 분류하면 틀린다. Sparse success는 목표 정의이며 실제 학습에는 dense tracking·progress·regularization이 함께 들어간다. [원문 §4.3, Eq. 7–10, App. B](https://arxiv.org/html/2611.05372v1)

### 5. 학습·배치 조건을 구분한다

| 항목 | OpenArm simulation | OpenArm hardware |
|---|---|---|
| 학습 | PPO, 4,096 병렬 환경, 약 $1.28\times10^9$ transitions | FlashSAC + HER, simulation weights 없이 120,000 online transitions |
| 제어 | Policy 30 Hz / physics 60 Hz, PD, 기본 실험은 gravity feedforward 없음 | Policy 10 Hz, PD + gravity feedforward |
| 관측·action | 54차원, $\eta=0.0625$, $\beta_{\min}=0.1$ | 72차원, $\eta=0.03\,\mathrm{rad}$, $\beta_{\min}=0.03$ |
| Reference bound | Eq. 2의 joint-limit clip | 측정 관절이 한계 안에 있을 때 reference clip을 $2^\circ$ 완화; lead bound $0.25\,\mathrm{rad}$ |
| 정밀도 학습 | 12초 rollout에서 4초마다 목표 변경 | Reverse curriculum, near-goal replay, latent-alignment critic, demonstration replay |

Hardware replay는 batch의 25%를 scripted demonstration 150 tasks × 150 steps(22,500 transitions)에서 가져오고, 각 source 내 75%는 $\rho\leq10$인 near-goal step에서 뽑는다. 따라서 실제 팔에서 학습하지만 demonstration-free라는 뜻은 아니다. Reverse curriculum에 먼 시작·큰 회전 과제도 섞는다. [원문 §§4.4–4.5, Apps. B, H.2–H.5, Table 11](https://arxiv.org/html/2611.05372v1)

Simulation deployment는 checkpoint averaging을 사용하며, near-goal 실패에 corrected goal을 주고 다른 실패에는 transient goal을 이용한 추가 시도를 한다. 성공 평가는 항상 원래 목표 기준이다. 단일 시도 $93.49\pm0.20\%$와 deployment $98.92\pm0.23\%$는 같은 실행 예산이 아니며, 후자의 평균 시도 수는 1.212다. [원문 §4.4, App. C, Tables 1, 4](https://arxiv.org/html/2611.05372v1)

## Assumptions / Requirements

- FK 모델, joint encoder, goal pose와 reference의 일관된 좌표계, reference를 추종할 position controller가 필요하다.
- 추론: 실제 적용에서는 accepted reference를 command-state feedback에 반영하고 reset·goal 변경 시 command 및 reward history 초기화를 일관되게 처리해야 한다.
- Hardware baseline은 50 Hz, $0.20\,\mathrm{rad/s}$ reference-speed bound와 별도 lead bounds·5 mrad inward margin을 사용한다. PolicyIK의 10 Hz·$0.25\,\mathrm{rad}$ lead bound·$2^\circ$ reference relaxation과 동일한 command constraint 비교는 아니다. [원문 Apps. H.5, I, Tables 11–12](https://arxiv.org/html/2611.05372v1)

## Inputs / Outputs

- 입력: measured joint state, FK pose와 목표 pose, multiscale errors, 이전 accepted reference의 상대값, 이전 action, running-best features.
- 출력: 다음 joint-position reference. Torque policy, 충돌 회피 planner, 물체 pose estimator를 대신하지 않는다.

## Failure Modes

- Command-state feedback을 빼면 누적 명령이 숨은 상태가 된다. 시뮬레이션 strict success는 93.49%에서 84.26%로 낮아졌고, measured-joint anchor까지 바꾸면 30.77%였다. [원문 §5.1.2, Table 7](https://arxiv.org/html/2611.05372v1)
- Dwell을 빼면 한 번 허용 오차에 진입해도 다시 벗어날 수 있다. 진입 과제 중 final-second containment 실패는 2.4%에서 7.8%로 증가했다. [원문 §5.1.2, Table 7](https://arxiv.org/html/2611.05372v1)
- Joint limit 가까운 목표는 필요한 holding offset과 reference bound가 충돌한다. Hardware의 bound relaxation은 이 문제에 대한 구체적 구현이며 보편적 안정성 보장은 아니다. [원문 App. H.5–H.6](https://arxiv.org/html/2611.05372v1)

## Evidence

- Simulation 4,120개 held-out pair, 5.3초 단일 시도의 93.5%는 **마지막 1초 평균 오차** 기준이다. 마지막 1초 모든 sample이 두 허용 오차 안인 containment는 92.4%로 별도다. [원문 §§3, 5.1.1, App. C](https://arxiv.org/html/2611.05372v1)
- Physical OpenArm 60개 과제·25초 예산에서 reach 54/60, 마지막 5초 모든 sample을 만족하는 hold 43/60이다. Pose error는 encoder FK로 계산하므로 외부 계측 기준의 절대 TCP 정확도 검증과 구분한다. [원문 §5.2, Table 3](https://arxiv.org/html/2611.05372v1)
- xArm7은 해당 로봇용으로 따로 학습한 sim-trained/hardware-trained 정책의 결과다. OpenArm 정책의 zero-shot embodiment transfer 근거가 아니다. [원문 App. J, Table 13](https://arxiv.org/html/2611.05372v1)

## Related Concepts

- [[Learned Closed-Loop Inverse Kinematics]] — implemented-by: reference 갱신 정책으로 learned IK의 실행·정지 문제를 구체화한다.
- [[Reset-State Curricula for Sparse-Reward RL]] — uses: hardware reverse curriculum이 시작 상태 분포를 목표 근처부터 확장한다.
- [[AlphaNIST Binary-Reward Assembly]] — 추론: 정밀 조작 RL이라는 비교 축은 공유하지만, PolicyIK는 dense reward가 포함되므로 reward 설계를 동일시하지 않는다.
- [[Vision-Language-Action Models]] — uses: 시뮬레이션에서 $\pi_{0.5}$의 pose 명령을 실행하는 하위 제어기로 평가했다. Hand-tuned DLS보다 높은 성공률을 보인 결과는 아니다 (§5.1.3, Table 2).
- [[2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning]] / [[2026-11-03 - PolicyIK Source]] — 방법의 논문·원자료 근거.

## Open Questions

- 동일 제어 주기·reference speed·lead/bound 조건으로 맞추면 classical baseline 대비 이점은 얼마나 유지되는가?
- 외부 pose sensing, payload 변화, calibration 오차, 접촉과 장애물이 포함될 때 정밀 holding은 유지되는가?
- [[2026-11-05 - How Should Pose Reaching and Holding Be Evaluated]] — answers: 평균 terminal error, 순간 도달, 연속 holding을 분리하는 평가 원칙.
