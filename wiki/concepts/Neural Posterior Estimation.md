---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - neural-posterior-estimation
  - simulation-based-inference
  - uncertainty
sources:
  - https://arxiv.org/abs/1905.07488
  - https://proceedings.mlr.press/v164/muratore22a.html
---

# Neural Posterior Estimation

## Definition

Neural Posterior Estimation, NPE는 simulator로 만든 $(\theta, D)$ pair를 사용해 conditional density estimator $q_\psi(\theta \mid D)$를 학습하는 SBI 계열 방법이다.

## Why It Matters

작은 로봇 motion에서는 torque waveform 하나가 여러 parameter 조합으로 설명될 수 있다. NPE는 단일 추정값 대신 posterior를 출력하므로, parameter ambiguity와 insufficient excitation을 진단 결과에 반영할 수 있다.

## In This Wiki

$$
q_\psi(\pi_E,\phi_f^{eff}\mid q,\dot q,\tau)
$$

학습 data generation은 temperature를 포함하지 않는다.

$$
\pi_E^{(i)} \sim p(\pi_E), \quad
\phi_f^{eff,(i)} \sim p(\phi_f^{eff})
$$

## Implementation Notes

- 초기 구현: temporal encoder + diagonal Gaussian posterior head.
- 확장 구현: normalizing flow posterior head.
- 입력 window에는 $q$, $\dot q$, $\tau$를 넣고, $\ddot q$는 filtering 또는 learned acceleration estimator로 처리한다.
- Posterior covariance가 크면 fault 판정을 유보한다.

## Related Papers

- [[2019 - Automatic Posterior Transformation for Likelihood-Free Inference]]
- [[2022 - Neural Posterior Domain Randomization]]

## Related Concepts

- [[Simulation-Based Inference]]
- [[Differentiable Dynamics]]
