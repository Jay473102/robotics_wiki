---
type: paper
status: active
created: 2026-09-01
updated: 2026-09-01
tags:
  - grasping
  - flow-matching
  - generative-models
  - manipulation
sources:
  - raw/papers/2608.26076v1.pdf
  - https://arxiv.org/abs/2608.26076
title: Fast Generative Grasping via Lie Group-Constrained MeanFlow
authors: S. Talha Bukhari, Yi Wei, Ruiqi Ni, Zachary Kingston, Aniket Bera
year: 2026
venue: arXiv preprint (2608.26076, v1 2026-08-26), IEEE journal 양식이나 venue 미표기
doi:
url: https://arxiv.org/abs/2608.26076
---

# GraspMF - Fast Generative Grasping via Lie Group-Constrained MeanFlow

## TL;DR

Grasp 분포 학습에 쓰이는 diffusion·flow 모델은 수십~수백 NFE가 필요해 반응형 실행에 부적합하다. GraspMF는 MeanFlow(구간 평균 속도 예측)를 bi-invariant metric을 갖는 product Lie group $G = SO(3) \times \mathbb{R}^3$ 위에 정식화하여, **5 NFE 이하로** ACRONYM에서 SOTA diffusion/flow baseline과 대등 이상의 grasp 성공률을 밀리초 단위 latency(15.5ms @ T=5, 6.3ms @ T=1)로 달성한다. 학습은 네트워크 미분 항이 전혀 없는 대수적 semigroup consistency와 시간 대각선의 Riemannian CFM anchor의 합으로 구성된다.

## Problem

물체 하나에 대한 안정적 grasp의 집합은 $SE(3)$ 위의 multimodal 분포다. Point estimate 회귀 대신 분포를 학습하면 여러 유효 grasp을 샘플링하고 collision avoidance, reachability 같은 downstream 목적과 결합할 수 있다. 하지만:

- Diffusion([[2026 - pi0.7 Steerable Generalist Robotic Foundation Model|pi 계열]]이 쓰는 flow matching 포함, 로봇 조작의 지배적 생성 모델 계열)은 step-by-step refinement로 유효 grasp의 암묵적 contact 제약을 해소하는 대신 추론에 수십~수백 integration step이 필요하다.
- Consistency model, shortcut model은 샘플링을 가속하지만 self-referential target을 최적화하므로 기저 transport vector field와의 정렬이 보장되지 않는다.
- Manifold 제약이 있는 상황에서 few-step 샘플링이 contact 제약을 보존하는지는 물리 시뮬레이션·실기 검증이 없었다.

## Core Idea

MeanFlow는 순간 속도 대신 시간 구간 $[s,t]$의 **평균 속도** $u(H,s,t) = \frac{1}{t-s}\log_G(H^{-1}\Phi_{s,t}(H))$를 학습한다. 평균 속도는 probability path의 잘 정의된 성질이고, teacher-free·simulation-free로 학습되며, 한 번의 chord-form jump가 flow map을 직접 평가하므로 1~수 스텝 생성이 된다.

이를 grasp pose가 사는 $SE(3)$에 적용하되, $SE(3) = SO(3) \ltimes \mathbb{R}^3$은 semidirect product라 bi-invariant Riemannian metric이 없으므로, 선행 연구와 같이 diffeomorphic한 직적군 $G = SO(3) \times \mathbb{R}^3$ 위에서 모델링한다. Product metric이 block-diagonal이라 회전과 병진이 분리되어 flow map이 회전 geodesic + 병진 secant로 나뉜다.

## Method

### Endpoint parameterization

네트워크 $X_\theta(H, s, t) = \hat{H}_1$은 평균 속도가 아니라 **clean grasp endpoint를 직접 예측**한다. 평균 속도와 flow map은 closed form으로 유도된다.

$$\bar{u}_\theta(H,s,t) = \tfrac{1}{1-s}\log_G(H^{-1}X_\theta(H,s,t)), \qquad \Phi_\theta(H,s,t) = \mathrm{Exp}_H\!\left(\tfrac{t-s}{1-s}\mathrm{Log}_H(\hat{H}_1)\right)$$

Endpoint regression의 안정성과 two-time flow map 구조를 함께 가진다. $t{=}s$ 대각선에서는 순간 속도로, $t{=}1$에서는 single-step 예측으로 환원된다.

### 학습 목적 함수 (두 항 + 보조항)

1. **CFM anchor** ($s{=}t$): geodesic interpolant $H_t$에서 예측 endpoint를 데이터 grasp $H_1$으로 회귀. Marginal-conditional argument에 의해 최적해가 시간 대각선에서 marginal velocity와 일치 → 정식화를 데이터 분포에 고정한다.
2. **Semigroup consistency**: 정확한 flow map의 성질 $\Phi_{s,t} = \Phi_{r,t} \circ \Phi_{s,r}$을 학습된 map에 요구. Two-step 합성을 stop-gradient target으로 두고 single-step 평균 속도와 비교한다. **순수 대수적** — forward 평가, $\exp_G$, $\log_G$만 쓰고 covariant derivative·JVP·네트워크 편미분이 없어 고차원에서 안정적으로 스케일한다 (SplitMeanFlow, Riemannian MeanFlow의 관찰). Semigroup 항 단독으로는 zero-displacement 자명해를 가지므로 anchor가 필수다.
3. **보조 SDF regression**: 중간 feature에서 물체 ground-truth SDF 값을 clipped $\ell_1$로 회귀 → flow map을 물체 기하에 grounding. [[Neural Implicit Surface Representation]]의 기하 특징 공유와 같은 계열.

안정화 장치: $\lambda_{semi}$를 첫 1000 epoch 동안 0→1 선형 annealing (data anchor가 먼저 지배), 두 손실 모두 metric norm 대신 인자별 $\ell_1$, anchor scale $1/(1{-}t)$ clamp, $r \to 1$ down-weight $w(r)$, anchor 시간은 $0.98\,\mathrm{Beta}(1.9,1.0) + 0.02\,U[0,1]$, semigroup triplet은 interval-first 샘플링에 $r = (s{+}t)/2$.

회전 인자에 대한 주의: 병진에서는 semigroup 분해가 정확히 Euclidean interval split이 되지만, 회전에서는 BCH 전개의 bracket 항 때문에 두 chord가 같은 축이 아닌 한 근사다.

### Architecture / Inference

- SE3Dif의 경량 backbone 재사용: VNN point cloud encoder (N=1024) + keypoint 기반 pose 표현 + 두 시간 인자의 random Fourier feature. 출력 12-D (9-D 회전 + 3-D 병진), 회전은 SVD로 $SO(3)$에 projection.
- 추론은 uniform partition에서 flow map 반복. 스텝당 정확히 1 NFE + closed-form exp/log 한 쌍. 잔차 오차는 수치 truncation error가 아니라 $\bar{u}_\theta - u$의 근사 오차다.
- 학습: Adam 1e-4, 유효 batch 400 (물체 2 × grasp 200), RTX 5080 16GB 1장에서 ~48시간 (~10K epoch).

## Data / Embodiment

- 학습·평가: [[ACRONYM]] 10개 카테고리 416 인스턴스, ~780K 유효 grasp. 90/10으로 ID 분할, 별도 6개 카테고리(Car, Donut, Laptop, Pencil, RubiksCube, Spoon)로 OOD 평가.
- Prior $\rho_0$: $SO(3)$ Haar measure × $\mathcal{N}(0, I_3)$. Point cloud centroid 중심 정규화 + random $SO(3)$ augmentation.
- 실기: Franka Research 3 (7-DoF) + Franka Hand + 손목 Orbbec Femto Mega RGB-D. SAM으로 segmentation, VAMP의 RRT-Connect로 궤적 계획.

## Evaluation

100개 샘플 grasp 기준 3개 지표: **SR** (Isaac Gym에서 open→approach→close→lift 후 5초 shake 생존), **EMD** ($SO(3)$ geodesic + $\lambda{=}0.1$ 가중 병진 거리로 ground truth 100개와의 분포 커버리지), **latency** (RTX 5080, 물체당 100 grasp batch).

## Results

### ACRONYM 본 실험 (Table I, II)

| Method | NFE | Latency | SR ID | SR OOD | EMD ID | EMD OOD |
|---|---|---|---|---|---|---|
| SE3Dif (T=70) | 140 | 600.1ms | 70.40 | 57.60 | 0.4649 | 0.4880 |
| BRIDGER (T=40) | 40 | 120.6ms | 59.38 | 63.77 | 0.6057 | 0.5589 |
| EGF (T=20) | 80 | 187.9ms | 85.48 | 65.09 | 0.3866 | 0.4805 |
| VSIGD (T=70) | 140 | 1124.4ms | 68.57 | 69.05 | 0.4966 | 0.4675 |
| **GraspMF (T=5)** | **5** | **15.5ms** | **87.40** | **71.73** | 0.3702 | **0.4191** |
| **GraspMF (T=1)** | **1** | **6.3ms** | 81.11 | 66.34 | **0.3698** | 0.4218 |

- T=5에서 SR·EMD 모두 최고 또는 2위권이면서 latency는 최선 baseline 대비 ~12×(EGF)~73×(VSIGD) 낮다. Abstract의 "39×"는 SE3Dif(600.1ms) 대비.
- SE3Dif/VSIGD는 predictor-corrector로 스텝당 2 NFE, EGF는 RK-MK 4차로 스텝당 4 NFE를 쓰는 것이 latency 격차의 큰 부분.

### Sampling budget 안정성 (Fig. 4)

$T \in \{1,...,100\}$ 전 구간에서 GraspMF OOD SR 평균 70.15%, 표준편차 1.63. Baseline은 low budget에서 붕괴: T=1/T=5에서 SE3Dif 6.65%/18.58%, VSIGD 7.04%/20.86%, EGF는 T=1에서 27.48%. SR-latency 평면에서 GraspMF가 Pareto frontier를 이룬다. 이것이 "semigroup consistency가 few-step에서도 contact 제약을 보존한다"는 주장의 직접 근거다.

### Ablation (T=5, Table III)

| 제거 요소 | SR ID 변화 | SR OOD 변화 |
|---|---|---|
| 보조 SDF regression 제거 | −3.8 | −5.1 |
| Semigroup weight annealing 제거 | −2.4 | −5.8 |
| SVD → Gram-Schmidt projection | +0.1 | −4.7 |
| Semigroup loss → decomposed objective (Zhong et al.) | **−25.15** | **−19.44** |

Semigroup consistency 정식화 자체가 최대 기여 요소. SVD projection은 Procrustes 최적해 + 9-D redundancy의 정규화 효과로 Gram-Schmidt 대비 OOD에서 우위 (latency는 13.5 vs 15.5ms로 GS가 빠름).

### 부분 관측 (single-view, Table IV)

Raycast single-view로 학습·평가 시 GraspMF가 OOD SR 최고(68.46%), ID는 BRIDGER(88.84%)가 GraspMF(86.08%)를 2.76pt 앞선다. 단 GraspMF가 7.8× 빠르다. GraspMF의 OOD EMD는 최악(0.5923)인데, 논문은 가시 표면 기준으로 제한된 reference grasp set 밖의 mode를 생성해도 실행은 성공할 수 있다는 metric 한계로 설명한다.

### 실기 (Table V)

가정용 물체 3종 × 10회: GraspMF T=5에서 9/9/10, T=10에서 9/10/10. EGF도 10/8/10으로 강하지만 latency가 ~12× 높다. 추가 학습·domain adaptation 없이 전이.

## Limitations

논문에 명시적 limitation 절이 없다. 본문에서 직접 확인되는 제약:

- Parallel-jaw gripper 단일 물체 table-top 시나리오만 다룬다. Dexterous hand, cluttered scene, non-prehensile은 범위 밖 (future work에 dual-arm $SE(3){\times}SE(3)$, contact manifold 언급).
- 학습 데이터가 ACRONYM 10개 카테고리 416 인스턴스로 제한적이다.
- 회전 인자의 semigroup identity는 BCH bracket 항까지만 성립한다. 큰 회전 chord에서의 영향은 정량화되지 않았다.
- EMD의 view-dependent reference set 문제(위)로 부분 관측 하 coverage 평가가 불완전하다.
- 6.3ms latency가 가능케 한다는 closed-loop replanning은 실증되지 않았다 ("may achieve better performance").
- 검증 필요: 코드·모델 공개 여부 본문 미언급.

## Connections

- [[GraspMF Few-Step Grasp Generation]] — implemented-by: 이 논문의 방법을 절차로 정리한 페이지.
- [[Generative Grasp Synthesis]] — 이 논문이 속한 문제 영역.
- [[MeanFlow]] — uses: 평균 속도 기반 few-step 생성 프레임워크를 Lie group으로 가져온다.
- [[Flow Matching]] — extends: Riemannian CFM을 anchor로 포함하며, 다수 스텝 요구라는 flow matching의 약점을 겨냥한다.
- [[ACRONYM]] — evaluated-on.
- [[2025 - pi0.6 a VLA That Learns From Experience]], [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]] — VLA action head가 같은 flow matching 계열이므로, MeanFlow식 few-step화는 policy 추론 가속에도 잠재적으로 이식 가능 (논문도 MP1을 인용). 추론: 위키 차원의 연결이며 이 논문이 직접 다루지는 않는다.
- [[Amortized NeuralSDF-Mesh Collision Detection]] — 반복 최적화/적분을 학습된 predictor 한 번으로 대체한다는 amortization 패턴을 공유한다. 그쪽은 contact 계산, 이쪽은 생성 모델 샘플링.
- [[Neural Implicit Surface Representation]] — uses: 보조 SDF regression으로 기하 특징을 grounding한다. [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]의 "SDF를 여러 축에서 공유" 질문에 grasp 생성이라는 세 번째 용례를 더한다.

## Contradictions / Updates

- Concurrent work인 Zhong et al. (Riemannian MeanFlow for one-step generation on manifolds, ICML 2026)의 decomposed objective에 대해 이 논문은 gradient conflict, covariant derivative 비용, 성능 열위(Table III)를 주장한다. 저자 자신의 재현 기반이므로 해당 논문 입장과 교차 확인 전까지 일방 주장으로 취급.
- 위키 내 기존 페이지와 충돌 없음. Grasp 생성 축 자체가 이 ingest로 신설되었다.

## Notes / Marginalia

없음. PDF에 사용자 annotation이 없다 (하이퍼링크만 존재).

## Open Questions

- 6.3ms single-step 추론을 실제 closed-loop grasp replanning에 넣으면 동적 장면에서 성공률이 얼마나 오르는가?
- 평균 속도 few-step 정식화를 VLA action expert(flow matching 기반)에 적용하면 policy 추론 가속이 되는가? MP1(인용 [16])이 Euclidean에서 시도했다는데 manifold 제약 action space에서는 미검증.
- Semigroup consistency가 보존한다는 "암묵적 contact 제약"의 메커니즘은 무엇인가? 논문은 경험적 결과만 제시한다.
- Gram-Schmidt가 ID에서는 동급인데 OOD에서만 4.7pt 떨어지는 이유는? 일반화와 rotation projection의 상호작용은 열린 문제다.
