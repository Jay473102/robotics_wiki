---
type: concept
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - fault-diagnosis
  - robot-dynamics
  - parameter-identification
  - friction
sources:
  - raw/chats/AI 기반 로봇 고장진단.pdf
---

# Slow-Fast Parameter Separation in Robot Fault Diagnosis

## Definition

Slow-fast parameter separation은 robot fault diagnosis에서 tool/end-effector inertia처럼 천천히 바뀌는 parameter와 joint friction처럼 health 상태에 따라 빠르게 바뀌는 parameter를 다른 시간 스케일로 추정하는 원칙이다.

## Why It Matters

Torque residual은 다음처럼 여러 원인이 합쳐져 나타난다.

$$
\Delta\tau = Y_E\Delta\pi_E + Y_f\Delta\phi_f + \epsilon
$$

작은 motion에서는 $Y_E\Delta\pi_E$와 $Y_f\Delta\phi_f$가 서로 보상될 수 있다. 그러면 tool inertia 오차를 friction fault로 오인하거나, 실제 friction 증가를 tool inertia correction으로 흡수할 수 있다.

## Key Ideas

- $\beta_R^0$: robot body parameter. Offline identification 후 고정한다.
- $\pi_E$: slow parameter. Tool 장착 시 또는 작업 전 calibration에서 추정하고 online diagnosis 중에는 가능하면 고정한다.
- $\Delta\phi_f$: fast health parameter. 작업 중 sliding window마다 추정한다.
- $z_r$: nuisance residual. Nominal data에서 제한적으로 학습하고 online adaptation은 막거나 강하게 제한한다.

## Practical Rule

고장진단 window에서 $\pi_E$와 $\Delta\phi_f$를 동시에 자유롭게 풀지 않는다.

권장 순서:

1. Robot-only calibration으로 $\beta_R^0$를 얻는다.
2. Tool calibration으로 $\pi_E^*$를 얻는다.
3. Online diagnosis에서는 $\pi_E=\pi_E^*$로 두고 $\Delta\phi_f$만 업데이트한다.
4. Fault decision은 $\Delta\phi_f$의 posterior covariance와 temperature baseline을 함께 본다.

## Related Concepts

- [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]
- [[Temperature-Friction Baseline]]
- [[Robot Dynamics Parameter Identification]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]

## Open Questions

- $\pi_E$ posterior uncertainty가 클 때 friction diagnosis를 얼마나 보류해야 하는가?
- Tool이 작업 중 변형되거나 payload가 바뀌는 경우 slow parameter assumption은 어떻게 완화해야 하는가?
