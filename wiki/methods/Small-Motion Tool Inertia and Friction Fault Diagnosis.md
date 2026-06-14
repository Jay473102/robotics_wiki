---
type: method
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - method
  - fault-diagnosis
  - robot-dynamics
  - friction
sources:
  - raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md
---

# Small-Motion Tool Inertia and Friction Fault Diagnosis

## TL;DR

작은 작업 motion만 허용되는 산업용 로봇에서 $\pi_E$와 $\phi_f^{eff}$를 posterior로 추정하고, real temperature baseline $g^{real}(T)$를 빼서 friction fault component를 얻는 방법론이다.

## Inputs

- Joint position $q$
- Joint velocity $\dot q$
- Measured torque or motor current-derived torque $\tau$
- Joint temperature $T$
- Pre-identified robot body model $\beta_R^0$
- Calibrated tool inertia $\pi_E^*$

## Outputs

- Effective friction estimate $\phi_f^{eff}$
- Fault component $\Delta\phi_f^{fault}$
- Uncertainty-aware fault score $S_f$
- Insufficient-motion flag

## Pipeline

1. 사전에 robot body parameter $\beta_R^0$를 식별한다.
2. Simulation에서 safe small motions와 sampled $\pi_E$, $\phi_f^{eff}$로 NPE를 pretrain한다.
3. Tool 장착 후 $\pi_E$를 calibration하고 online 단계에서는 고정한다.
4. 정상 warm-up 데이터에서 $g^{real}(T)$를 구축한다.
5. Online window마다 $\phi_f^{eff}$를 추정하고 $g^{real}(T)$를 빼 fault component를 계산한다.

## Diagnostic Score

$$
\Delta\phi_f^{fault} = \phi_f^{eff,*} - g^{real}(T)
$$

$$
S_f =
\Delta\phi_f^{fault,T}
(\Sigma_{est}+\Sigma_g+\Sigma_{sensor})^{-1}
\Delta\phi_f^{fault}
$$

## Failure Modes

- Motion이 너무 작으면 $\pi_E$와 $\phi_f$가 분리되지 않는다.
- Temperature baseline이 충분히 cover하지 못한 온도 영역에서는 false positive가 늘 수 있다.
- Residual model이 fault signal을 학습하면 진단 민감도가 떨어진다.
- Torque measurement가 current proxy라면 motor constant, gearbox loss, filtering delay가 추가 bias가 된다.

## Related

- [[2026-06-15 - Small-Motion Tool Inertia and Friction Fault Diagnosis]]
- [[Neural Posterior Estimation]]
- [[Differentiable Dynamics]]
- [[Temperature-Friction Baseline]]
- [[Robot Dynamics Parameter Identification]]
