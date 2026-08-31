---
type: method
status: active
created: 2026-09-01
updated: 2026-09-01
tags:
  - method
  - grasping
  - flow-matching
  - generative-models
sources:
  - raw/papers/2608.26076v1.pdf
---

# GraspMF Few-Step Grasp Generation

## TL;DR

Point cloud 조건부 grasp pose 분포를 product Lie group $G = SO(3) \times \mathbb{R}^3$ 위의 [[MeanFlow]]로 학습해, 1~5회 네트워크 평가로 유효 grasp을 샘플링하는 절차. 네트워크는 clean grasp endpoint를 직접 예측하고, 평균 속도와 flow map은 closed form으로 유도된다. 출처: [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]].

## Problem Setting

물체 point cloud $c \in \mathbb{R}^{N \times 3}$가 주어졌을 때 안정 grasp pose $H = (R, p) \in SE(3)$의 multimodal 분포에서 밀리초 단위로 샘플링해야 한다. Diffusion·flow 모델의 수십~수백 NFE는 반응형 closed-loop 실행과 양립하지 않는다.

## Procedure

**학습** (mini-batch마다 두 손실을 동시 평가):

1. Expert grasp $H_1 \sim p_{data}$, prior $H_0 \sim \rho_0$ (Haar $\times$ Gaussian) 샘플링.
2. **CFM anchor**: anchor 시간 $t$에서 geodesic interpolant $H_t$를 만들고, $X_\theta(H_t, t, t)$의 endpoint 예측을 left-trivialized tangent space에서 $H_1$으로 회귀 ($1/(1{-}t)$ 재가중, clamp 0.1).
3. **Semigroup consistency**: 시간 triplet $s \le r \le t$에서 two-step 합성 $\Phi_\theta(\Phi_\theta(H_s,s,r),r,t)$의 chord 속도를 stop-gradient target으로 두고 single-step 평균 속도 $\bar{u}_\theta(H_s,s,t)$를 맞춘다.
4. 보조 손실: 중간 feature에서 물체 SDF 값을 clipped $\ell_1$ 회귀.
5. $\lambda_{semi}$는 첫 1000 epoch 동안 0→1 annealing. 두 손실 모두 인자별 $\ell_1$ norm.

**추론** (sampling budget $T$):

1. $H_0 \sim \rho_0$에서 시작, uniform partition을 따라 $H_{t_{k+1}} = \Phi_\theta(H_{t_k}, t_k, t_{k+1})$ 반복.
2. 각 스텝은 1 NFE + closed-form exp/log 한 쌍. 회전은 geodesic, 병진은 secant로 분리 갱신.
3. $T{=}1$이면 $H_1 = X_\theta(H_0, 0, 1)$ 한 번으로 끝.

## Assumptions / Requirements

- Expert grasp annotation이 있는 학습 데이터 ([[ACRONYM]] 사용, ~780K grasps).
- $SE(3)$ 대신 bi-invariant metric이 있는 직적군 $SO(3) \times \mathbb{R}^3$ 채택 (선행 diffusion/flow grasp 연구와 동일한 선택).
- Chord가 $\exp_G$의 injectivity radius 안에 있어야 평균 속도가 잘 정의된다. Antipodal 회전은 measure-zero이고 안정 branch로 처리.
- 회전 인자의 semigroup 분해는 BCH bracket 항까지만 정확하다.

## Inputs / Outputs

- 입력: 물체(또는 segment) point cloud 1024점, centroid 정규화. 시간 인자 $(s, t)$.
- 출력: grasp pose 분포에서 샘플링된 $(R, p)$ 배치. 물체당 100개 병렬 생성 기준 15.5ms (T=5, RTX 5080).

## Failure Modes

- 단일 시점 부분 관측에서 ID 성능이 informative prior 방식(BRIDGER)에 밀린다. Centroid 정규화가 가시 표면 쪽으로 편향되는 것이 원인 중 하나.
- Semigroup 항 단독 학습은 zero-displacement 자명해로 붕괴 → anchor 없이는 성립하지 않는다.
- Annealing 없이 처음부터 self-consistency를 강제하면 OOD SR이 5.8pt 하락.

## Evidence

- Tier A: 논문 Table I-V, Fig. 2-5. ID SR 87.40% / OOD 71.73% (T=5), 전 budget에서 OOD SR 표준편차 1.63, 실기 Franka Research 3에서 물체 3종 9~10/10.

## Related Concepts

- [[MeanFlow]] — implemented-by: 이 방법이 MeanFlow의 Riemannian semigroup 정식화를 grasp에 구현한다.
- [[Flow Matching]] — depends-on: CFM anchor가 데이터 분포 고정에 필수다.
- [[Generative Grasp Synthesis]] — 문제 영역.
- [[Amortized NeuralSDF-Mesh Collision Detection]] — 반복 계산의 학습 기반 amortization이라는 공통 패턴.

## Open Questions

- Cluttered scene·dexterous hand로의 확장 경로는? 논문 future work는 dual-arm $SE(3) \times SE(3)$과 contact manifold를 언급한다.
- Rejection sampling + replanning loop와 결합했을 때의 실효 성능 (논문이 부분 관측 격차의 해법으로 제안만 함).
