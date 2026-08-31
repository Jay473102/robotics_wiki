---
type: concept
status: draft
created: 2026-09-01
updated: 2026-09-01
tags:
  - flow-matching
  - generative-models
  - robot-learning
sources:
  - raw/papers/2608.26076v1.pdf
  - https://arxiv.org/abs/2210.02747
---

# Flow Matching

## Definition

Prior 분포 $\rho_0$의 샘플을 target 분포 $\rho_1$로 운반하는 시간 의존 velocity field $v(x, t)$를 회귀로 학습하는 생성 모델 프레임워크 (Lipman et al., ICLR 2023). Conditional Flow Matching(CFM)은 데이터 쌍별 조건부 경로(예: 직선 또는 geodesic interpolant)의 조건부 속도를 target으로 쓰며, 그 회귀의 최적해가 marginal velocity와 일치한다는 성질로 simulation-free 학습을 얻는다. 추론은 ODE $\dot{x}_t = v_\theta(x_t, t)$의 수치 적분이다.

## Why It Matters

Diffusion과 함께 로봇 조작의 지배적 생성 모델 계열이다. Multimodal 분포(grasp 집합, demonstration의 action 분포)를 mode collapse 없이 학습하고, deterministic ODE 적분이라 diffusion의 stochastic sampling보다 적은 스텝으로 수렴하는 경향이 있다. π0 계열 VLA의 action expert가 flow matching으로 action chunk를 생성한다 ([[2025 - pi0.6 a VLA That Learns From Experience]], [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]).

## Key Ideas

- **Riemannian CFM**: manifold 위에서는 geodesic interpolant $H_t = \mathrm{Exp}_{H_0}(t \cdot \mathrm{Log}_{H_0}(H_1))$와 tangent velocity로 재정식화된다 (Chen & Lipman, ICLR 2024). Lie group에서는 left-trivialization으로 velocity를 Lie algebra 값 함수로 학습할 수 있다.
- **한계 — 스텝 수**: 유효 샘플이 나오려면 수십 스텝의 적분이 필요하다. $SO(3)$ toy 실험에서 flow matching은 수십 스텝, [[MeanFlow]]는 3스텝 안에 target support에 집중했다 (GraspMF Fig. 2, Tier A).
- **가속 계열**: rectified flow, progressive distillation, consistency/shortcut model, 그리고 평균 속도를 예측하는 [[MeanFlow]]. 앞의 셋은 self-referential target 또는 teacher가 필요하지만 MeanFlow는 둘 다 없다.

## Related Papers

- [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]] — Riemannian CFM을 anchor로 사용하고 few-step 한계를 극복 대상으로 삼는다.
- [[2025 - pi0.6 a VLA That Learns From Experience]], [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]] — flow matching 기반 action 생성의 대표 사용처.
- [[2026 - DIAL Decoupling Intent and Action via Latent World Modeling]] — 생성적 action decoding 축에서 인접.

## Related Concepts

- [[MeanFlow]] — extends: 순간 속도 대신 구간 평균 속도를 학습해 few-step 생성을 얻는다.
- [[Generative Grasp Synthesis]] — 이 프레임워크의 주요 로봇 응용 중 하나.
- [[Vision-Language-Action Models]] — action head 구현 기술로 사용된다.

## Contradictions / Updates

없음.

## Open Questions

- 로봇 policy에서 flow matching과 diffusion의 실질적 성능 차이는 어디서 갈리는가? 위키에 아직 정면 비교 자료 없음.
