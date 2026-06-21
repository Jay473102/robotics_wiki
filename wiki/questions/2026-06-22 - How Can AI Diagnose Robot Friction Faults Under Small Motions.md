---
type: question
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - question
  - fault-diagnosis
  - robot-dynamics
  - friction
  - neural-posterior-estimation
sources:
  - raw/chats/AI 기반 로봇 고장진단.pdf
  - raw/papers/2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification.pdf
---

# How Can AI Diagnose Robot Friction Faults Under Small Motions?

## Short Answer

가능하지만, 단순히 $q,\dot q \rightarrow \tau$를 학습하는 black-box model로 접근하면 안 된다. 작은 motion에서는 end-effector inertia error와 joint friction change가 torque residual 안에서 서로 섞이므로, robot body parameter, tool inertia, friction health parameter를 분리한 physics-informed posterior estimation 구조가 필요하다.

## Why This Question Matters

산업용 로봇에서는 dynamic parameter identification을 위해 충분히 큰 persistent excitation trajectory를 주기 어렵다. 특히 bulky end-effector가 있거나 작업공간이 좁으면 collision risk 때문에 기존 식별 궤적을 그대로 쓸 수 없다. 하지만 고장진단은 작업 중 작은 motion window에서도 friction 변화를 감지해야 한다.

## Current Answer

권장 decomposition은 다음이다.

$$
\hat{\tau}_t =
\tau_R(q_t,\dot q_t,\hat{\ddot q}_t;\beta_R^0)
+ \tau_E(q_t,\dot q_t,\hat{\ddot q}_t;\pi_E)
+ \tau_f(\dot q_t,T_t;\phi_f^{normal}(T_t)+\Delta\phi_f)
+ r_\eta(h_t,z_r)
$$

- $\beta_R^0$: robot body parameter. Tool 없이 또는 표준 tool로 offline calibration 후 고정한다.
- $\pi_E$: end-effector inertia. Tool 장착 시 또는 작업 전 calibration에서 slow parameter로 추정한다.
- $\Delta\phi_f$: friction change. 작업 중 sliding window마다 fast health parameter로 추정한다.
- $r_\eta$: cable drag, unmodeled flexibility, torque bias 등 nominal residual. Fault signal을 먹지 않도록 capacity와 update policy를 제한해야 한다.

고장진단은 절대 friction 값보다 정상 baseline 대비 변화로 보는 것이 안전하다.

$$
\Delta\phi_f^{fault}
= \phi_f^{estimated} - \phi_f^{normal}(T)
$$

진단 score는 posterior covariance를 포함해야 한다.

$$
S_f = \Delta\phi_f^{T}\Sigma_f^{-1}\Delta\phi_f
$$

작은 motion에서 정보가 부족하면 $\Sigma_f$가 커져야 하며, 이 경우는 "정상"이나 "고장"이 아니라 "진단 불확실"로 처리해야 한다.

## Evidence / Sources

- [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]: temperature와 mounting/tool configuration이 dynamic/friction parameter identification에 영향을 준다는 primary source.
- [[2026-06-22 - AI-Based Robot Fault Diagnosis Chat]]: bulky tool과 작은 작업 motion 조건에서 AI 기반 fault diagnosis 구조를 설계한 chat source.
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]: 기존 위키의 작은 motion 기반 tool inertia/friction diagnosis pipeline.

## Important Caveats

Chat source는 primary source가 아니다. `Provably-Safe, Online System Identification`, RMA, HiP-RSSM 등 외부 문헌 언급은 별도 검증 전까지 설계 후보로만 취급한다.

## Linked Pages

- [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]
- [[Slow-Fast Parameter Separation in Robot Fault Diagnosis]]
- [[Safe Diagnostic Trajectory Design]]
- [[Temperature-Friction Baseline]]
