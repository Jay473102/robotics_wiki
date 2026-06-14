---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - friction
  - temperature
  - fault-diagnosis
sources:
  - raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md
  - raw/papers/robotics-10-00083-v3.pdf
---

# Temperature-Friction Baseline

## Definition

Temperature-friction baseline은 정상 상태 로봇에서 joint temperature와 effective friction estimate 사이의 관계를 real data로 fitting한 기준 함수다.

$$
g^{real}(T) \approx \phi_f^{normal}
$$

## Why It Matters

마찰 계수, 특히 viscous friction은 온도에 따라 변할 수 있다. 이를 보정하지 않으면 정상 warm-up에 따른 friction 변화와 마모/윤활 문제에 따른 fault를 혼동할 수 있다.

[[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]는 UR3/UR5 실험에서 joint temperature 상승에 따라 viscous friction coefficient가 각각 약 20%, 17% 감소했다고 보고한다. 이 결과는 고장진단에서 온도 보정 baseline을 따로 두어야 한다는 근거로 사용할 수 있다.

## Design Rule

이 위키의 현재 방법론에서는 temperature-friction relation을 simulation에 넣지 않는다. Simulation은 inverse estimator pretraining에만 쓰고, $g^{real}(T)$는 정상 실제 데이터로만 구축한다.

## Recommended Models

- 초기 구현: joint-wise linear model.
- 더 안정적인 구현: monotonic spline.
- uncertainty-aware 구현: Gaussian Process 또는 uncertainty를 내는 spline/ensemble.

## Fault Component

$$
\Delta\phi_f^{fault} = \phi_f^{eff,*} - g^{real}(T)
$$

Baseline uncertainty $\Sigma_g(T)$는 fault score에 반드시 포함한다.

## Related

- [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
- [[Robot Dynamics Parameter Identification]]
