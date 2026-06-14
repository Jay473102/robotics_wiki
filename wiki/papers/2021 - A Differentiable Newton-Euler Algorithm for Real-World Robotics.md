---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - differentiable-dynamics
  - robot-dynamics
  - parameter-identification
sources:
  - https://arxiv.org/abs/2110.12422
title: A Differentiable Newton-Euler Algorithm for Real-World Robotics
authors: Michael Lutter; Johannes Silberbauer; Joe Watson; Jan Peters
year: 2021
venue: arXiv
doi: 10.48550/arXiv.2110.12422
url: https://arxiv.org/abs/2110.12422
---

# A Differentiable Newton-Euler Algorithm for Real-World Robotics

## TL;DR

DiffNEA는 Newton-Euler 기반 dynamics 계산을 미분 가능하게 구성해, complex friction model과 constraints가 있는 real-world mechanical system의 parameter를 gradient-based optimization으로 식별하는 접근이다.

## Relevance

NPE가 posterior를 빠르게 추정하더라도, real torque residual을 줄이는 local refinement가 필요할 수 있다. Differentiable dynamics는 $\pi_E$와 $\phi_f^{eff}$를 직접 gradient로 조정하는 MAP refinement에 적합하다.

## Connection To Note

$$
\theta^* =
\arg\min_\theta
\sum_t \rho(\tau_t^{meas} - \hat{\tau}_t(q,\dot q,\hat{\ddot q};\theta))
+ \lambda_\theta \|\theta-\theta_0\|^2
$$

## Related

- [[Differentiable Dynamics]]
- [[Robot Dynamics Parameter Identification]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
