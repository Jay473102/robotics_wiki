---
type: method
status: active
created: 2026-08-01
updated: 2026-08-01
tags:
  - method
  - point-cloud-registration
  - signed-distance-field
  - neural-implicit-representation
  - optimization
sources:
  - raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf
---

# SDFReg Point Cloud Registration

## TL;DR

Target point cloud를 neural SDF로 바꾸고, source point를 그 zero level set에 밀어넣는 방식으로 rigid transformation을 푼다. 대응점 탐색이 없고, SDF 학습과 pose 최적화를 번갈아 돌려 coarse-to-fine 정렬을 만든다.

원 논문은 [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]].

## Problem Setting

- 입력: source point cloud $P \in \mathbb{R}^{N \times 3}$, target point cloud $Q \in \mathbb{R}^{M \times 3}$.
- 출력: $\Theta \in SE(3)$.
- 가정: rigid transformation, 중간 정도의 초기 오정렬(축별 회전 45-60도 범위), 부분 overlap 허용.
- 노린 조건: noise, partial visibility, 큰 density 차이가 있는 imperfect point cloud.

## Procedure

1. **Target 인코딩** — encoder가 $Q$에서 feature $z$ (차원 256)를 뽑는다. 전체 절차에서 한 번만 실행한다.
2. **SDF 초기화** — decoder가 (source point 좌표, $z$)를 받아 SDF 값을 낸다. Query point는 공간 sampling이 아니라 source point cloud $P$ 자체로 시작한다.
3. **거리 계산** — 변환된 각 점의 표면까지 거리를 SDF 값으로 직접 읽는다. $\mathrm{Dist}(Rp_i + t, f_c) = \mathrm{SDF}(Rp_i + t)$.
4. **Jacobian 구성** — $J(i,j) = \frac{\partial}{\partial \xi_j}(Rp_i+t)\cdot\nabla\mathrm{SDF}(Rp_i+t)$. $\nabla\mathrm{SDF}$는 network backpropagation으로 얻는다.
5. **Pose 갱신 1스텝** — Levenberg-Marquardt로 $(J^TJ + \lambda\,\mathrm{diag}(J^TJ))\Delta\xi = J^TD$를 풀고, $\Delta\Theta = \exp(\Delta\xi^\wedge)$로 $P$를 갱신한다.
6. **Query point 누적** — 갱신된 point cloud를 query set에 더한다.
7. **교대 반복** — 2-6을 반복한다. $\epsilon = |D_n - D_{n-1}|/D_n < 0.001$ 이거나 $n > 30$이면 종료한다.

손실은 $\mathcal{L}_{reg} = \mathcal{L}_{c2f} + \lambda_e\mathcal{L}_{eikonal}$ ($\lambda_q = 0.01$, $\lambda_e = 0.001$).

## Assumptions / Requirements

- SDF backbone이 미지 category에 일반화되어야 한다. 원 논문은 GenSDF를 써서 shape마다 재학습하지 않는다.
- SDF가 매끄러워야 한다. Jacobian이 $\nabla\mathrm{SDF}$에 의존하므로 gradient가 안정적이어야 하고, 그래서 Eikonal 정규화가 필요하다.
- LM은 국소 최적화다. 초기 pose가 수렴 영역 안에 있어야 한다.
- Rigid 변환만 다룬다.

## Inputs / Outputs

| | |
|---|---|
| 입력 | source/target point cloud, 초기 pose |
| 중간 표현 | target feature $z$ (256), neural SDF $\Phi(\cdot \mid Q)$ |
| 출력 | $\Theta_{est} \in SE(3)$, 정렬된 source point cloud |
| 부산물 | target 형상의 continuous SDF |

마지막 항목이 중요하다. Registration의 부산물로 target의 연속 SDF가 남으며, 이는 다른 기하 계산에 재사용할 여지가 있다. 추론: 이 재사용 가능성은 논문이 다루지 않았고 [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]에서 다룬다.

## Failure Modes

- **큰 초기 오정렬**: LM 국소 수렴 실패. 논문은 45-60도 범위만 시험했다.
- **낮은 overlap**: query point 누적이 실제로 대응하지 않는 영역에 집중될 수 있다. 70% overlap만 검증되었다.
- **실시간 제약**: target마다 SDF 최적화 루프를 돌아야 한다. 비용 미보고.
- **Clean data**: 이점이 없다. 대응점 기반 방법이 더 정확할 수 있다.
- **회전 tail**: 3DMatch에서 median 3.16도 대비 RMSE 15.6도로, 실제 장면에서 큰 실패 사례가 남는다.

## Evidence

[[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]의 표 1-5. [[ModelNet40]] cross-category, [[3DMatch]] 실내 스캔, Stanford 3D Scan 일반화(정성). Ablation에서 coarse-to-fine이 주 기여, Eikonal이 보조로 확인된다.

## Related Concepts

- [[Point Cloud Registration]]
- [[Neural Implicit Surface Representation]]
- [[NeuralSDF Collision Detection]] — 같은 neural SDF query 패턴을 접촉 계산에 적용한 대응 사례.
- [[Amortized NeuralSDF-Mesh Collision Detection]] — 반복 최적화를 학습된 predictor로 대체하는 반대 방향의 설계 선택.

## Open Questions

- Coarse-to-fine query 누적을 overlap 추정과 결합하면 낮은 overlap에서도 버티는가?
- 30 iteration 상한을 줄이면 정확도가 어떻게 떨어지는가? 비용-정확도 곡선이 필요하다.
- Global registration으로 초기값을 주고 SDFReg를 정밀화 단계로만 쓰는 조합이 실용적인가?
