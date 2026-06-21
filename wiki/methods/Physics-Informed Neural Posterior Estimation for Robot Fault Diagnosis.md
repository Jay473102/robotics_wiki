---
type: method
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - method
  - neural-posterior-estimation
  - fault-diagnosis
  - robot-dynamics
  - friction
sources:
  - raw/chats/AI 기반 로봇 고장진단.pdf
  - raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md
---

# Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis

## TL;DR

Physics-informed NPE for robot fault diagnosis는 작은 motion window $D=\{q,\dot q,\tau,T\}_{1:T}$에서 end-effector inertia $\pi_E$와 friction change $\Delta\phi_f$의 posterior를 직접 추정하고, differentiable inverse dynamics로 MAP refinement를 수행하는 방법이다.

## Model

Posterior estimator는 다음을 출력한다.

$$
q_\psi(\theta\mid D), \quad
\theta=[\pi_E,\Delta\phi_f,z_r]
$$

Physics decoder는 torque를 다음처럼 분해한다.

$$
\hat{\tau}_t =
\tau_R(q_t,\dot q_t,\hat{\ddot q}_t;\beta_R^0)
+ \tau_E(q_t,\dot q_t,\hat{\ddot q}_t;\pi_E)
+ \tau_f(\dot q_t,T_t;\phi_f^{normal}(T_t)+\Delta\phi_f)
+ r_\eta(h_t,z_r)
$$

## Architecture

1. Temporal encoder: TCN, GRU, Transformer 중 하나로 $D$를 encoding한다.
2. Acceleration latent/head: noisy $\ddot q$를 직접 쓰지 않고 $\hat{\ddot q}$를 추정하거나 smoothing한다.
3. Tool posterior head: $q_{\psi_E}(\pi_E\mid D_{tool})$.
4. Friction posterior head: $q_{\psi_f}(\Delta\phi_f\mid D_{diag},\pi_E,T)$.
5. Nuisance residual: $z_r$와 $r_\eta$로 nominal residual만 제한적으로 설명한다.
6. Differentiable physics decoder: robot body, tool, friction, residual torque를 합산한다.

## Training Data

- Synthetic parameter-randomized data: $\pi_E$, $\Delta\phi_f$, temperature, noise, trajectory family를 randomize한다.
- Nominal real data: $\Delta\phi_f=0$으로 보고 residual branch와 sim-to-real correction을 calibrate한다.
- Temperature sweep data: $\phi_f^{normal}(T)$ baseline을 실제 정상 데이터로 fitting한다.
- Diagnostic trajectory family: 실제 diagnosis에 쓸 task-like window, paired velocity probing, small dither, static pose set을 포함한다.

## Losses

Synthetic data에서는 posterior NLL을 쓴다.

$$
L_{NPE} = -\log q_\psi(\theta^{(s)}\mid D^{(s)})
$$

Torque reconstruction loss를 추가한다.

$$
L_\tau = \sum_t \|\tau_t^{(s)}-\hat{\tau}_t\|^2
$$

추가 regularization 후보:

- $L_a$: acceleration smoothing 또는 acceleration latent supervision.
- $L_{phys}$: physically plausible inertia/friction constraint.
- $L_{sep}$: $\pi_E$, $\Delta\phi_f$, $z_r$가 서로 역할을 빼앗지 않도록 분리하는 penalty.

## Inference

Tool calibration 단계:

$$
q_{\psi_E}(\pi_E\mid D_{tool}) \rightarrow \mu_E,\Sigma_E
$$

이후 differentiable MAP refinement:

$$
\pi_E^*=\arg\min_{\pi_E}\sum_t\|\tau_t-\hat{\tau}_t(\pi_E)\|^2-\lambda\log p(\pi_E)
$$

Diagnosis 단계:

$$
q_{\psi_f}(\Delta\phi_f\mid D_{diag},\pi_E^*,T)\rightarrow \mu_f,\Sigma_f
$$

Friction-only refinement:

$$
\Delta\phi_f^*
=\arg\min_{\Delta\phi_f}
\sum_t\|\tau_t-\hat{\tau}_t(\pi_E^*,\phi_f^{normal}(T)+\Delta\phi_f)\|^2
+\lambda_f\|\Delta\phi_f\|^2
$$

## Failure Modes

- Training trajectory family와 실제 diagnosis trajectory가 다르면 posterior가 과신될 수 있다.
- Residual branch가 너무 강하면 friction fault를 흡수한다.
- $\pi_E$와 $\Delta\phi_f$를 같은 window에서 동시에 자유롭게 추정하면 leakage가 생긴다.
- Torque가 motor current proxy이면 motor constant, gearbox loss, filtering delay가 covariance에 반영되어야 한다.

## Related

- [[Neural Posterior Estimation]]
- [[Slow-Fast Parameter Separation in Robot Fault Diagnosis]]
- [[Safe Diagnostic Trajectory Design]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
