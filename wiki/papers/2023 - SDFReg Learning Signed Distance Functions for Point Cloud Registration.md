---
type: paper
status: active
created: 2026-08-01
updated: 2026-08-01
tags:
  - point-cloud-registration
  - signed-distance-field
  - neural-implicit-representation
  - optimization
sources:
  - raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf
  - https://arxiv.org/abs/2304.08929
title: "SDFReg: Learning Signed Distance Functions for Point Cloud Registration"
authors: Leida Zhang, Zhengda Lu, Kai Liu, Yiqun Wang
year: 2023
venue: arXiv preprint (2304.08929, v2 2024-01-10), venue 미표기
doi: 10.48550/arXiv.2304.08929
url: https://arxiv.org/abs/2304.08929
---

# SDFReg - Learning Signed Distance Functions for Point Cloud Registration

## TL;DR

Target point cloud를 neural SDF로 표현하고, source point cloud를 그 implicit surface에 정렬함으로써 대응점 탐색 없이 rigid registration을 푼다. SDF 학습과 registration을 번갈아 최적화하는 coarse-to-fine 전략으로, noise, partial visibility, 20배 density 차이가 있는 imperfect point cloud에서 기존 방법보다 강건하다.

## Problem

Point cloud registration은 서로 다른 pose의 두 point cloud를 정렬하는 $\Theta \in SE(3)$를 찾는 문제다. 기존 접근은 두 갈래이며 둘 다 imperfect data에서 무너진다.

- **Correspondence-based** (ICP, DCP 등): 대응점을 먼저 찾고 변환을 푼다. 대응점 탐색이 noise, incompleteness, density 변화에 직접 노출된다.
- **Direct** (PointNetLK, FMR, DeepGMR 등): 대응점 없이 feature 차이를 최소화한다. Clean data에서는 잘 되지만 outlier가 feature 기반 distance metric을 왜곡한다.

전통적 direct 방법 중 implicit polynomial fitting 계열도 있었으나, polynomial의 표현력 한계로 smooth surface에서만 검증되었고 복잡한 물체나 장면에는 쓰지 못했다.

## Core Idea

두 point cloud 사이의 정렬을 **point cloud와 neural implicit surface 사이의 정렬**로 치환한다.

$$\hat{\Theta} = \arg\min_{R \in SO(3), t \in \mathbb{R}^3} \sum_{i=1}^{N} \mathrm{Dist}^2(R p_i + t, f_c)$$

여기서 $f_c$는 target point cloud $Q$를 표현하는 implicit surface이고, 점과 표면 사이의 orthogonal distance는 SDF 값 그 자체다.

$$\mathrm{Dist}(R p_i + t, f_c) = \mathrm{SDF}(R p_i + t)$$

이 형태에서는 대응점이 필요 없다. Distance가 rigid parameter에 직접 연결되고, SDF가 미분 가능하므로 gradient 기반 최적화로 바로 풀린다.

## Method

### Registration 최적화

Jacobian은 chain rule로 얻는다.

$$J(i,j) = \frac{\partial}{\partial \xi_j}(R p_i + t) \cdot \nabla \mathrm{SDF}(R p_i + t)$$

$\nabla \mathrm{SDF}$는 network backpropagation으로 얻는다. Distance error가 non-linear least squares 형태이므로 Levenberg-Marquardt로 증분을 푼다.

$$(J^T J + \lambda\,\mathrm{diag}(J^T J))\,\Delta\xi = J^T D$$

$\Delta\xi \in \mathbb{R}^6$는 $se(3)$ twist이고, $\Delta\Theta = \exp(\Delta\xi^\wedge)$로 사상해 source point cloud를 갱신한다. 최종 추정 $\Theta_{est}$는 반복 증분의 누적이다.

### SDF 학습

Self-supervised loss로 SDF $\Phi(x \mid Q)$를 학습한다. Query point $x$의 표면 위 최근접점 $t = \arg\min_{q \in Q}\|x - q\|_2$를 정답으로 두고, 예측 SDF 값으로 재구성한 $\hat{t}$가 $t$에 가까워지도록 한다.

$$\mathcal{L}_{self} = \frac{1}{|X|}\sum_j \|\hat{t}_j - t_j\|_2^2 + \lambda_q \frac{1}{M}\sum_{q \in Q} \|\Phi(q_i \mid Q)\|_1$$

$\ell_1$ 항은 target point cloud 위에서 SDF가 0이 되도록 강제한다. $\lambda_q = 0.01$.

Eikonal 항으로 gradient norm을 1로 정규화한다.

$$\mathcal{L}_{eikonal} = \frac{1}{|X|}\sum_j (\|\nabla\Phi(x_j)\|_2 - 1)^2$$

### Coarse-to-Fine 교대 최적화

이 논문의 핵심 기여다. 기존 SDF 학습은 공간에서 고정 sampling한 query point를 쓰기 때문에 registration 과정과 분리되어 있고, 정렬에 실제로 중요한 국소 영역의 SDF를 정밀하게 학습하지 못한다.

SDFReg는 대신:

1. Source point cloud $P$ 자체를 query point로 써서 SDF를 최적화한다. 초기에는 표면에서 먼 점들의 거리를 배운다.
2. Registration 1 iteration을 수행한다.
3. 갱신된 point cloud를 query point set에 **누적**한다.
4. 1-3을 번갈아 반복한다.

Registration이 진행될수록 query point가 표면 근처로 모이므로 자연히 coarse-to-fine이 된다.

$$\mathcal{L}_{c2f} = \frac{1}{K}\sum_{k \in K}\|\hat{t}_t - t_t\|_2^2 + \lambda_q\frac{1}{M}\sum_{q \in Q}\|\Phi(q_i \mid Q)\|_1$$

$K = N \times itrs$이며, query point는 공간에서 sampling하지 않는다.

최종 손실: $\mathcal{L}_{reg} = \mathcal{L}_{c2f} + \lambda_e \mathcal{L}_{eikonal}$, $\lambda_e = 0.001$.

### Architecture

Backbone은 GenSDF (Chou et al. 2022).

- **Encoder**: target point cloud 입력. 5개 ResNet block을 쓴 improved PointNet에 UNet 형태의 down/up convolution과 skip connection. 출력 feature $z$ 차원 256. 한 번만 실행한다.
- **Decoder**: source point 좌표와 $z$를 concat해 입력. 8-layer MLP, hidden 512, skip connection. 출력은 SDF 값.

GenSDF를 고른 이유는 미지 category의 shape에 대해 SDF를 처음부터 재학습하지 않아도 되기 때문이다. Registration은 대량의 미지 shape에 대해 pose를 추론해야 하므로 이 성질이 중요하다.

### Implementation

- 종료 조건: 상대 거리 오차 $\epsilon = |D_n - D_{n-1}| / D_n$가 $0.001$ 미만이거나 $n > 30$.
- 하드웨어: NVIDIA RTX 3090 24GB 단일 GPU.

## Data / Embodiment

로봇 embodiment는 없다. 3D geometry 수준의 연구이며 저자들은 응용처로 3D reconstruction, autonomous driving, intelligent robotics를 든다.

- [[ModelNet40]]: 12,311 CAD model, 40 class. PointNetLK 설정을 따라 20 class 학습 / 20 class cross-class 테스트. 1024점 균일 샘플링, $[0,1]^3$ 정규화, 축별 회전 $[0, 45°]$, 병진 $[-0.5, 0.5]$.
- [[3DMatch]]: Kinect로 촬영한 실내 RGB-D scan. PointNetLK-Revisited를 따라 7-Scenes와 SUN3D에서 8개 scene category를 테스트로 사용. 회전 $[0, 60°]$, 병진 $[0, 1.0]$으로 초기화.
- Stanford 3D Scanning Dataset: ModelNet 학습 모델을 그대로 적용해 일반화 확인. 정성 결과만 제시한다.

## Evaluation

$$\mathrm{Error}(R) = \arccos\!\left(\frac{\mathrm{trace}(R_{gt}^{-1}\hat{R}) + 1}{2}\right)\cdot\frac{180}{\pi}, \quad \mathrm{Error}(t) = \|t_{gt} - \hat{t}\|_2$$

MAE와 RMSE로 보고한다. Baseline은 ICP, PointNetLK, DCP-V2, FMR, DeepGMR, IFR.

## Results

### ModelNet40 (unseen categories)

| 조건 | 지표 | Ours | IFR | DCP-V2 | 최고 baseline |
|---|---|---|---|---|---|
| Clean | R MAE / RMSE [deg] | 2.5886 / **3.1540** | **1.1474** / 5.0707 | 2.0072 / 3.5501 | — |
| Clean | t MAE / RMSE [m] | **0.0033** / **0.0048** | 0.0100 / 0.0554 | 0.0037 / 0.0050 | — |
| Noise | R MAE / RMSE | **3.9754** / **9.1780** | 4.9289 / 11.335 | 5.6346 / 12.850 | — |
| Noise | t MAE / RMSE | **0.0058** / **0.0089** | 0.0788 / 0.1271 | 0.0253 / 0.0381 | — |
| Partial (70%) | R MAE / RMSE | **4.1362** / **11.596** | 5.0400 / 11.728 | 26.927 / 43.275 | — |
| Partial | t MAE / RMSE | **0.0056** / **0.0103** | 0.0232 / 0.0233 | 0.0981 / 0.1168 | — |
| Density (20x) | R MAE / RMSE | 3.8191 / **8.839** | **3.4699** / 9.3591 | 39.617 / 59.627 | — |
| Density | t MAE / RMSE | **0.0084** / **0.0098** | 0.0395 / 0.1122 | 0.0091 / 0.0318 | — |

- Clean data에서는 우위가 없다. Rotation MAE는 IFR(1.1474)과 DCP-V2(2.0072)가 더 좋고, SDFReg는 RMSE에서만 앞선다. 논문도 "comparable to IFR and DCP"라고 인정한다.
- 우위는 imperfect data에서 나온다. 특히 translation 오차가 baseline 대비 한 자릿수 작다.
- Density 20배 차이 실험에서 DeepGMR은 실행 자체가 불가능하다.
- MAE는 좋은데 RMSE가 훨씬 큰 baseline(예: clean data의 IFR, MAE 1.15 대 RMSE 5.07)은 소수의 큰 실패 사례가 있다는 뜻이다. SDFReg의 강점은 평균 정확도보다 **실패 tail이 짧다**는 데 있다.

### Robustness (clean/partial/noise/density 전체에 걸친 분산)

| Method | SD(R) | SD(t) | AVG(R) | AVG(t) |
|---|---|---|---|---|
| IFR | 1.814 | 0.042 | 3.647 | 0.035 |
| **Ours** | **0.706** | **0.002** | **3.321** | **0.005** |

입력 품질에 따른 성능 변동이 가장 작다. 이 표가 논문의 핵심 주장을 가장 직접적으로 뒷받침한다.

검증 필요: 이 표의 baseline 인용 번호가 참고문헌 목록과 어긋난다 (`FMR [12]`, `DeepGMR [11]`). 행 이름 기준으로 읽었다.

### 3DMatch (실제 실내 스캔)

| Method | R RMSE / Median [deg] | t RMSE / Median [m] |
|---|---|---|
| ICP | 24.772 / 4.501 | 1.064 / 0.149 |
| IFR | 23.814 / 4.191 | 1.057 / 0.161 |
| **Ours** | **15.623 / 3.1562** | **0.065 / 0.013** |

Translation RMSE가 baseline 대비 16배 이상 작다. 다만 회전 RMSE 15.6도는 절대 기준으로는 여전히 크며, median 3.16도와의 격차는 실제 장면에서 실패 사례가 남아 있음을 뜻한다.

### Ablation (ModelNet40)

| Loss | MAE(R) | RMSE(R) | MAE(t) | RMSE(t) |
|---|---|---|---|---|
| $\mathcal{L}_{self}$ | 6.8108 | 19.513 | 0.0154 | 0.0518 |
| $\mathcal{L}_{c2f}$ | 4.1376 | 11.681 | 0.0062 | 0.0106 |
| $\mathcal{L}_{self} + \mathcal{L}_{eikonal}$ | 5.3418 | 16.263 | 0.0098 | 0.0186 |
| $\mathcal{L}_{c2f} + \mathcal{L}_{eikonal}$ | **2.5887** | **8.5548** | **0.0034** | **0.0049** |

Coarse-to-fine 전략이 주된 기여(MAE 6.81 → 4.14)이고 Eikonal 단독 효과는 그보다 작다(6.81 → 5.34). 둘을 합치면 2.59로, 개별 개선폭의 합으로 예측되는 값(약 2.67)과 사실상 같다. 즉 두 요소는 대체로 독립적으로 더해지며, 상호작용을 주장할 근거는 이 표에 없다.

## Limitations

논문에 별도의 limitation 절이 없다. 다음은 본문에서 직접 확인되는 제약이다.

- 계산 비용이 전혀 보고되지 않았다. 학습 시간, registration 1건당 시간, iteration당 비용이 모두 없다. Target마다 SDF를 최적화하는 구조이므로 이는 중대한 공백이다.
- 최대 30 iteration을 돌며 각 iteration에서 SDF를 갱신한다. 실시간 로봇 perception loop에 대한 적합성을 이 논문만으로 판단할 수 없다.
- Partial visibility 실험이 overlap 70% 한 조건뿐이다. 낮은 overlap에서의 거동은 미검증이다.
- Clean data에서는 기존 방법 대비 이점이 없다.
- 초기 pose 범위가 제한적이다 (ModelNet40 축별 $[0, 45°]$, 3DMatch $[0, 60°]$). 큰 초기 오정렬에서 LM 기반 국소 최적화가 수렴하는지는 다루지 않는다.
- Rigid transformation만 다룬다. Deformable registration은 범위 밖이다.

## Connections

- [[Point Cloud Registration]] — 이 논문이 속한 문제 영역.
- [[SDFReg Point Cloud Registration]] — implemented-by: 이 논문의 방법을 절차로 정리한 페이지.
- [[Neural Implicit Surface Representation]] — uses: SDF를 registration의 distance metric으로 사용한다.
- [[Signed Distance Field Collision Detection]] — 같은 SDF 표현을 접촉 계산에 쓰는 대응 축. SDF의 미분 가능성과 부호 있는 거리라는 성질을 공유한다.
- [[NeuralSDF Collision Detection]] — neural SDF를 query해 기하 계산을 수행하는 동일 패턴. 이쪽은 contact, SDFReg는 pose 추정에 쓴다.
- [[Amortized NeuralSDF-Mesh Collision Detection]] — extends 관점의 대비: 그쪽은 반복 최적화를 학습된 predictor로 대체해 속도를 얻고, SDFReg는 반복 최적화를 오히려 학습 루프 안에 넣는다.
- [[Tetra-Encoded Signed Distance Field]] — SDF query 비용을 자료구조로 줄이는 대안 경로.
- [[ModelNet40]], [[3DMatch]] — evaluated-on.

## Contradictions / Updates

현재 위키 안에 이 논문과 충돌하는 주장은 없다. SDF 관련 기존 페이지들은 모두 collision/contact 축이고, 이 논문은 perception/registration 축이라 상보적이다.

## Notes / Marginalia

없음. PDF에 사용자 annotation이 없다.

## Open Questions

- Target마다 SDF를 최적화하는 비용이 로봇 온라인 perception에서 감당 가능한가? 논문이 비용을 보고하지 않아 판단 근거가 없다.
- Registration에 쓴 SDF를 그대로 collision detection에 재사용할 수 있는가? → [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]
- Overlap이 50% 이하로 떨어지면 coarse-to-fine query 누적 전략이 잘못된 영역에 집중하지 않는가?
- 큰 초기 오정렬에서 LM 기반 국소 수렴이 실패하는 지점은 어디인가? Global registration과 결합해야 하는가?
- 본문(self-supervised)과 supplementary(semi-supervised)의 용어 불일치는 실제 절차 차이인가 단순 표기 오류인가?
