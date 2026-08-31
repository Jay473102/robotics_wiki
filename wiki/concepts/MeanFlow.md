---
type: concept
status: draft
created: 2026-09-01
updated: 2026-09-01
tags:
  - flow-matching
  - generative-models
  - amortized-optimization
sources:
  - raw/papers/2608.26076v1.pdf
  - https://arxiv.org/abs/2505.13447
---

# MeanFlow

## Definition

Flow 기반 생성 모델에서 순간 속도 $v(x, t)$ 대신 시간 구간의 **평균 속도** $u(x, s, t) = \frac{1}{t-s}\int_s^t$ (flow map의 chord)를 신경망으로 학습하는 few-step 생성 프레임워크 (Geng et al. 2025). 평균 속도를 알면 한 번의 chord-form jump가 구간 전체의 적분을 대체하므로 1~수 회 네트워크 평가로 샘플링이 끝난다.

## Why It Matters

Diffusion·[[Flow Matching]]의 다단계 샘플링은 로봇의 반응형 closed-loop 실행과 양립하지 않는다. MeanFlow는 (1) teacher-free, simulation-free이고, (2) consistency/shortcut model과 달리 평균 속도라는 probability path의 잘 정의된 성질을 target으로 하므로 최적해가 네트워크와 무관하게 특성화되며, (3) 학습된 chord jump는 고정 스텝 Lie-Euler 적분의 truncation error를 갖지 않는다 — 잔차는 오직 근사 오차다.

## Key Ideas

- **Semigroup (interval-splitting) consistency**: 정확한 flow map은 $\Phi_{s,t} = \Phi_{r,t} \circ \Phi_{s,r}$을 만족한다. SplitMeanFlow(Guo et al. 2025)는 이를 Euclidean에서, Riemannian MeanFlow(Woo et al. 2026)는 manifold에서 대수적 consistency 목적 함수로 쓴다. 미분 항(JVP, covariant derivative)이 없어 원래 MeanFlow 손실보다 고차원에서 안정적이다.
- **Anchor 필요성**: semigroup identity는 data-free라 zero-displacement 자명해를 가진다. 시간 대각선에서의 CFM anchor가 데이터 분포에 고정하는 역할을 한다.
- **Endpoint parameterization**: 평균 속도를 직접 예측하는 대신 clean endpoint를 예측하고 평균 속도·flow map을 closed form으로 유도하는 쪽이 안정적이라고 보고된다 (Woo et al.).
- **로봇 응용**: manipulation policy 1-step화 (MP1, Sheng et al. 2025), Lie group 제약 grasp 생성 ([[GraspMF Few-Step Grasp Generation]]). 단백질 backbone 생성($SE(3)^N$)이 manifold 정식화의 원류다.

## Related Papers

- [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]] — $SO(3) \times \mathbb{R}^3$에서 semigroup consistency + CFM anchor로 grasp 생성. 물리 시뮬레이션·실기로 few-step 품질을 검증한 사례.

## Related Concepts

- [[Flow Matching]] — 기반 프레임워크. MeanFlow가 그 다단계 샘플링 한계를 겨냥한다.
- [[Generative Grasp Synthesis]] — 응용 문제 영역.
- [[Amortized NeuralSDF-Mesh Collision Detection]] — 추론: "반복 절차를 학습된 한 번의 예측으로 amortize"한다는 구조적 유사성. 그쪽은 KKT 최적화, 이쪽은 ODE 적분을 대체한다.

## Contradictions / Updates

- 2026-09-01: manifold 위 MeanFlow의 목적 함수 설계에 경쟁 정식화가 있다. Zhong et al. (ICML 2026)은 covariant derivative 기반 decomposed objective를, Woo et al./GraspMF는 대수적 semigroup consistency를 쓴다. GraspMF ablation에서 전자가 SR −25pt로 열등했으나 저자 측 재현이므로 검증 필요.

## Open Questions

- 평균 속도 few-step화가 VLA action expert 추론 가속으로 이어지는가? MP1이 Euclidean policy에서 시도했으나 위키에 원문 미확보.
- Semigroup consistency가 다단계 refinement 없이도 데이터 manifold의 암묵적 제약(예: contact feasibility)을 보존하는 메커니즘은 무엇인가?
