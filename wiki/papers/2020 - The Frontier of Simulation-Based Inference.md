---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - simulation-based-inference
  - likelihood-free-inference
  - inverse-problems
sources:
  - https://arxiv.org/abs/1911.01429
title: The frontier of simulation-based inference
authors: Kyle Cranmer; Johann Brehmer; Gilles Louppe
year: 2020
venue: PNAS / Sackler Colloquia proceedings
doi: 10.1073/pnas.1912789117
url: https://arxiv.org/abs/1911.01429
---

# The Frontier of Simulation-Based Inference

## TL;DR

복잡한 simulator는 high-fidelity sample을 만들 수 있지만, 그 자체가 곧바로 tractable likelihood를 주지는 않는다. 이 논문은 이런 simulator-driven inverse problem을 Simulation-Based Inference 관점에서 정리한다.

## Relevance

로봇 parameter estimation에서도 dynamics simulator는 torque sequence를 생성할 수 있지만, real sensor noise, delay, friction, unmodeled residual 때문에 정확한 likelihood를 쓰기 어렵다.

## Connection To Note

노트의 NPE 기반 tool inertia/friction 추정은 이 SBI 관점을 로봇 torque window에 적용한다.

$$
q_\psi(\pi_E,\phi_f^{eff}\mid q,\dot q,\tau)
$$

## Related

- [[Simulation-Based Inference]]
- [[Neural Posterior Estimation]]
- [[2026-06-15 - Small-Motion Tool Inertia and Friction Fault Diagnosis]]
