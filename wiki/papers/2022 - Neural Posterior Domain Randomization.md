---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - domain-randomization
  - simulation-based-inference
  - robotics
sources:
  - https://proceedings.mlr.press/v164/muratore22a.html
title: Neural Posterior Domain Randomization
authors: Fabio Muratore; Theo Gruner; Florian Wiese; Boris Belousov; Michael Gienger; Jan Peters
year: 2022
venue: CoRL / PMLR 164
doi:
url: https://proceedings.mlr.press/v164/muratore22a.html
---

# Neural Posterior Domain Randomization

## TL;DR

NPDR는 domain randomization의 parameter distribution을 고정된 Gaussian/Uniform family로 제한하지 않고, real-world observations를 이용해 simulator parameter posterior를 Bayesian하게 적응시키는 robotics-oriented 방법이다.

## Relevance

노트의 방법은 NPDR을 그대로 쓰지는 않지만, simulation parameter posterior를 더 유연하게 다루는 발상과 연결된다.

## Connection To Note

$\phi_f^{eff}$와 $\pi_E$를 고정 분포에서 point sampling하는 대신 posterior 형태로 추정하고, uncertainty를 fault score에 반영하는 설계와 맞닿아 있다.

## Related

- [[Neural Posterior Estimation]]
- [[Simulation-Based Inference]]
- [[2026-06-15 - Small-Motion Tool Inertia and Friction Fault Diagnosis]]
