---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - neural-posterior-estimation
  - likelihood-free-inference
  - normalizing-flows
sources:
  - https://arxiv.org/abs/1905.07488
title: Automatic Posterior Transformation for Likelihood-Free Inference
authors: David S. Greenberg; Marcel Nonnenmacher; Jakob H. Macke
year: 2019
venue: arXiv
doi: 10.48550/arXiv.1905.07488
url: https://arxiv.org/abs/1905.07488
---

# Automatic Posterior Transformation for Likelihood-Free Inference

## TL;DR

APT는 sequential neural posterior estimation 계열 방법으로, adaptively proposed simulations와 neural conditional density estimator를 이용해 likelihood-free posterior를 학습한다.

## Relevance

작은 robot motion에서는 $\pi_E$와 $\phi_f^{eff}$ posterior가 넓거나 비정규적일 수 있다. APT/NPE 계열은 단일 point estimate보다 이런 불확실성을 더 직접적으로 표현한다.

## Connection To Note

노트에서는 APT를 직접 구현 대상으로 확정하지는 않지만, high-dimensional time-series data에도 적용 가능한 NPE reference로 사용한다. 초기 구현은 diagonal Gaussian posterior head로 시작하고, posterior가 복잡하면 flow-based estimator를 고려한다.

## Related

- [[Neural Posterior Estimation]]
- [[Simulation-Based Inference]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
