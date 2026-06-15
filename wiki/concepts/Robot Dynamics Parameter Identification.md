---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - robot-dynamics
  - parameter-identification
  - rigid-body-dynamics
sources:
  - raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md
  - raw/papers/2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification.pdf
---

# Robot Dynamics Parameter Identification

## Definition

Robot dynamics parameter identification은 measured torque와 joint trajectory를 이용해 rigid-body dynamics, friction, motor inertia 등의 parameter를 추정하는 절차다.

표준 형태는 다음과 같다.

$$
\tau = Y(q,\dot q,\ddot q)p
$$

## Classical Workflow

1. Persistent excitation trajectory를 설계한다.
2. Regressor $Y$의 condition number를 낮춘다.
3. LS/WLS/CWLS 등으로 base parameter를 식별한다.
4. 식별된 parameter로 torque prediction을 수행한다.

[[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]는 UR3/UR5에서 5th order Finite Fourier Series 기반 excitation trajectory와 LS/WLS 식별을 사용한다. PDF 기준 제조사 제공 정보만 쓸 때보다 torque estimation normalized error를 약 90% 줄였고, mounting configuration에 따라 regressor와 base dynamic parameter 수가 달라질 수 있음을 보인다.

## Limitation For Industrial Fault Diagnosis

Bulky end-effector가 있거나 작업 공간이 좁으면 충분한 excitation trajectory를 안전하게 수행하기 어렵다. 작은 작업 motion만으로 full base parameter를 다시 식별하면 $Y^T Y$가 ill-conditioned가 되어 torque noise가 큰 parameter error로 증폭될 수 있다.

## Alternative Used Here

- $\beta_R^0$: robot body parameter는 offline 식별 후 고정.
- $\pi_E$: tool inertia만 calibration.
- $\phi_f^{eff}$: online window에서 effective friction만 빠르게 추정.
- $g^{real}(T)$: real 정상 baseline으로 온도 효과를 분리.

## Related

- [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
- [[Differentiable Dynamics]]
- [[Temperature-Friction Baseline]]
