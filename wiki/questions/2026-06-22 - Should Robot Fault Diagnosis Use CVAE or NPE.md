---
type: question
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - question
  - cvae
  - neural-posterior-estimation
  - fault-diagnosis
sources:
  - raw/chats/AI 기반 로봇 고장진단.pdf
---

# Should Robot Fault Diagnosis Use CVAE or NPE?

## Short Answer

이 문제의 주 모델은 CVAE보다 [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]가 더 적합하다. 이유는 우리가 원하는 latent가 추상적인 $z$가 아니라 물리적으로 해석 가능한 $\pi_E$와 $\Delta\phi_f$이기 때문이다.

## Why This Question Matters

고장진단에서는 "latent dimension 4가 커졌다"보다 "joint friction parameter가 온도 보정 후 증가했고 posterior uncertainty가 낮다"가 필요하다. 따라서 latent representation이 물리 파라미터와 정렬되어야 한다.

## Current Answer

NPE는 다음 posterior를 직접 학습한다.

$$
q_\psi(\theta \mid D), \quad
\theta=[\pi_E,\Delta\phi_f,z_r]
$$

여기서 $D=\{q,\dot q,\tau,T\}_{1:T}$는 작은 motion window다. Output은 point estimate가 아니라 posterior다. 작은 motion에서는 여러 parameter 조합이 비슷한 torque를 설명할 수 있으므로 diagonal Gaussian에서 시작하되, normalizing flow나 mixture density head로 확장할 수 있다.

일반 CVAE 구조는 다음처럼 될 수 있다.

$$
q_\psi(z\mid q,\dot q,\tau), \quad
p_\theta(\tau\mid q,\dot q,z)
$$

문제는 $z$가 tool inertia, friction fault, temperature effect, residual을 뒤섞을 수 있다는 점이다. 그러면 fault attribution이 불안정해진다.

CVAE를 쓴다면 다음처럼 factorized physics-CVAE여야 한다.

$$
q_{\psi_E}(\pi_E\mid D_{tool})
$$

$$
q_{\psi_f}(\Delta\phi_f\mid D_{diag},\pi_E,T)
$$

$$
p_\theta(\tau\mid q,\dot q,\pi_E,\Delta\phi_f,z_r)
$$

즉 CVAE도 가능하지만, "좋은 torque generator"가 아니라 "물리 파라미터 posterior estimator"가 되도록 제약해야 한다.

## Evidence / Sources

- [[2026-06-22 - AI-Based Robot Fault Diagnosis Chat]]: CVAE보다 physics-informed NPE + differentiable MAP refinement를 추천하는 reasoning source.
- [[Neural Posterior Estimation]]: 작은 motion에서 parameter ambiguity를 posterior로 표현하는 기본 개념.

## Important Caveats

NPE도 학습 trajectory family가 실제 진단 trajectory와 맞지 않으면 그럴듯한 posterior를 hallucinate할 수 있다. 따라서 OOD check와 MAP refinement가 함께 필요하다.

## Linked Pages

- [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]
- [[Slow-Fast Parameter Separation in Robot Fault Diagnosis]]
- [[Simulation-Based Inference]]
