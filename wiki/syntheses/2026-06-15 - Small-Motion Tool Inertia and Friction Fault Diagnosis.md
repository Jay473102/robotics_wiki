---
type: synthesis
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - fault-diagnosis
  - robot-dynamics
  - friction
  - simulation-based-inference
sources:
  - raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md
  - https://arxiv.org/abs/1911.01429
  - https://arxiv.org/abs/1905.07488
  - https://proceedings.mlr.press/v164/muratore22a.html
  - https://arxiv.org/abs/2110.12422
---

# Small-Motion Tool Inertia and Friction Fault Diagnosis

## Executive Summary

충분한 가진을 줄 수 없는 산업용 로봇에서는 full dynamic parameter identification보다, 사전 식별된 robot body model을 고정하고 end-effector inertia와 effective friction만 추정하는 구조가 더 실용적이다. 이 접근은 작은 작업 motion에서 발생하는 ill-posed inverse problem을 point estimate가 아니라 posterior 추정 문제로 다루고, 마지막에 differentiable dynamics 기반 MAP refinement로 물리 일관성을 보정한다.

가장 중요한 설계 원칙은 temperature-friction 관계를 simulation에서 만들지 않는 것이다. Simulation은 $q,\dot q,\tau \rightarrow \pi_E,\phi_f^{eff}$ inverse estimator를 pretrain하는 데만 쓰고, 온도에 따른 정상 마찰 변화 $g^{real}(T)$는 실제 정상 warm-up 데이터로 따로 fitting한다.

## Problem

기존 로봇 동역학 식별은 보통 다음 구조를 전제한다.

$$
\tau = Y(q,\dot q,\ddot q)p
$$

여기서 $p$는 링크 inertia, center of mass, Coulomb/viscous friction, motor inertia 등을 포함한다. 이 방식은 해석 가능하고 표준적이지만, regressor가 well-conditioned가 되도록 충분한 persistent excitation trajectory를 요구한다.

현장 제약은 다르다.

- end-effector가 커서 큰 motion은 TCP sweep과 충돌 위험을 키운다.
- 생산 중 고장진단을 위해 별도 excitation trajectory를 반복 수행하기 어렵다.
- 작은 작업 motion에서는 $\pi_E$와 $\phi_f$가 residual torque 안에서 서로 엉킬 수 있다.

## Proposed Decomposition

노트의 제안은 전체 base parameter를 다시 식별하지 않고 다음 세 항을 분리한다.

$$
\hat{\tau}_t =
\tau_R(q_t,\dot q_t,\hat{\ddot q}_t;\beta_R^0)
+ \tau_E(q_t,\dot q_t,\hat{\ddot q}_t;\pi_E)
+ \tau_f(\dot q_t;\phi_f^{eff})
+ r_\eta(h_t)
$$

- $\beta_R^0$: robot body offline identification 결과. online diagnosis 중 고정.
- $\pi_E$: unknown end-effector inertial parameters.
- $\phi_f^{eff}$: 현재 torque를 설명하는 effective friction.
- $r_\eta$: cable drag, backlash, torque bias, unmodeled flexibility 등 nominal residual.

초기 구현은 reduced end-effector parameter를 우선한다.

$$
\pi_E^{red} = [m, mc_x, mc_y, mc_z]
$$

Friction은 joint별로 다음 정도에서 시작한다.

$$
\phi_{f,j}^{eff} = [f_{c,j}^{+}, f_{c,j}^{-}, f_{v,j}]
$$

## Five-Stage Architecture

1. Robot-body offline identification: $\beta_R^0$를 사전에 식별한다.
2. Simulation pretraining: safe small motions와 sampled $\pi_E$, $\phi_f^{eff}$로 NPE를 학습한다.
3. Tool calibration: end-effector 장착 후 $\pi_E$를 먼저 추정해 online 단계에서 고정한다.
4. Real temperature-friction baseline: 정상 warm-up 데이터에서 $g^{real}(T)$를 구축한다.
5. Online diagnosis: 작업 중 sliding window에서 $\phi_f^{eff}$를 추정하고 정상 baseline과 비교한다.

## Diagnostic Score

$$
\Delta\phi_f^{fault} = \phi_f^{eff,*} - g^{real}(T)
$$

$$
S_f =
\Delta\phi_f^T
(\Sigma_{est}+\Sigma_g+\Sigma_{sensor})^{-1}
\Delta\phi_f
$$

## Why Posterior Instead Of Point Estimate

작은 motion에서는 하나의 torque waveform을 여러 parameter 조합이 설명할 수 있다. 따라서 단일 LS/MAP 값만 내면 고장과 부족한 excitation을 혼동하기 쉽다. [[Neural Posterior Estimation]]은 이 ambiguity를 posterior covariance나 multimodality로 드러낼 수 있다.

## Design Principle

Temperature-friction relation은 simulation에서 임의로 만들지 않는다.

잘못된 구조:

$$
T \sim p(T), \quad \phi_f = aT+b
$$

권장 구조:

$$
\phi_f^{eff} \sim p(\phi_f^{eff})
$$

그 다음 real normal data에서만:

$$
g^{real}(T) = \text{fit}(T, \phi_f^{eff})
$$

## Connections

- [[Simulation-Based Inference]]
- [[Neural Posterior Estimation]]
- [[Differentiable Dynamics]]
- [[Temperature-Friction Baseline]]
- [[Robot Dynamics Parameter Identification]]

## Open Questions

- Tool inertia와 friction이 작은 motion에서 얼마나 분리 가능한지 어떤 information threshold를 둘 것인가?
- $r_\eta$ residual network가 fault signal까지 흡수하지 않게 하려면 어떤 freeze/update policy가 필요한가?
- 초기 구현에서 diagonal Gaussian posterior로 충분한가, 아니면 normalizing flow가 필요한가?
- joint temperature sensor 위치와 실제 마찰면 온도 차이를 어떻게 보정할 것인가?
