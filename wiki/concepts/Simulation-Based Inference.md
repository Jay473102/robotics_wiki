---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - simulation-based-inference
  - bayesian-inference
  - inverse-problems
sources:
  - https://arxiv.org/abs/1911.01429
---

# Simulation-Based Inference

## Definition

Simulation-Based Inference, SBI는 simulator에서 sample은 만들 수 있지만 likelihood를 명시적으로 계산하기 어려운 문제에서 posterior, likelihood ratio, score 등을 학습해 inverse problem을 푸는 방법론이다.

## Why It Matters

로봇 동역학에서는 noise, delay, unmodeled friction, backlash, sensor bias 때문에 $p(D \mid \theta)$를 정확히 쓰기 어렵다. 하지만 parameter를 샘플링하고 forward/inverse dynamics로 synthetic torque sequence를 만드는 것은 가능하다.

## In This Wiki

$$
\theta = [\pi_E, \phi_f^{eff}]
$$

$$
D = \{q_t,\dot q_t,\tau_t\}_{t=1:T}
$$

$$
q_\psi(\theta | D) \approx p(\theta | D)
$$

## Related Papers

- [[2020 - The Frontier of Simulation-Based Inference]]
- [[2019 - Automatic Posterior Transformation for Likelihood-Free Inference]]

## Related Concepts

- [[Neural Posterior Estimation]]
- [[Robot Dynamics Parameter Identification]]
