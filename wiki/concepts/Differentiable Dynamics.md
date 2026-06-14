---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - differentiable-dynamics
  - robot-dynamics
  - parameter-identification
sources:
  - https://arxiv.org/abs/2110.12422
---

# Differentiable Dynamics

## Definition

Differentiable dynamics는 rigid-body dynamics, friction, constraints 등의 계산 graph를 parameter에 대해 미분 가능하게 만들어, gradient-based optimization으로 model parameter를 조정하는 접근이다.

## Why It Matters

NPE는 빠르게 posterior를 추정하지만, simulation-to-real mismatch와 local torque residual이 남을 수 있다. Differentiable dynamics 기반 MAP refinement는 NPE posterior mean 또는 sample을 초기값으로 받아 실제 torque residual을 줄이는 후처리로 쓸 수 있다.

## MAP Refinement

$$
\theta^* =
\arg\min_\theta
\sum_t \rho(\tau_t^{meas} - \hat{\tau}_t(q,\dot q,\hat{\ddot q};\theta))
+ \lambda_\theta \|\theta-\theta_0\|^2
$$

## Identifiability Check

$$
J_\theta = \frac{\partial \hat{\tau}}{\partial \theta}
$$

$$
H = J_\theta^T \Sigma_\tau^{-1} J_\theta + \Sigma_\theta^{-1}
$$

$H$가 ill-conditioned이면 fault가 아니라 insufficient information으로 처리하는 것이 안전하다.

## Related Paper

- [[2021 - A Differentiable Newton-Euler Algorithm for Real-World Robotics]]

## Related Concepts

- [[Robot Dynamics Parameter Identification]]
- [[Neural Posterior Estimation]]
