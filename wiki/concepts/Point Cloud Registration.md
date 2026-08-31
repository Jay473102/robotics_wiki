---
type: concept
status: draft
created: 2026-08-01
updated: 2026-08-01
tags:
  - point-cloud-registration
  - perception
  - optimization
sources:
  - raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf
---

# Point Cloud Registration

## Definition

Point cloud registration은 서로 다른 pose에서 얻은 두 point cloud를 같은 좌표계로 정렬하는 rigid transformation $\Theta \in SE(3)$를 찾는 문제다.

$$\hat{\Theta} = \arg\min_{R \in SO(3),\, t \in \mathbb{R}^3} \|T(RP + t), T(Q)\|_2^2$$

$T$가 무엇이냐에 따라 접근이 갈린다. 대응점 기반에서는 같은 개수/순서로 sampling된 대응 관계, direct 방법에서는 feature 추출 함수, implicit 방법에서는 표면까지의 거리 함수다.

## Why It Matters

로봇에서 registration은 "내가 보는 것이 무엇이고 어디에 있는가"를 결정하는 단계다. 3D reconstruction, autonomous driving의 localization, bin picking의 물체 pose 추정, 조립 검사가 모두 여기에 의존한다. Registration 오차는 downstream의 grasp planning과 motion planning으로 그대로 전파된다.

실제 로봇 센서 데이터는 항상 imperfect하다. Depth sensor noise, 시점 하나에서 얻는 2.5D partial scan, 거리에 따른 density 변화가 기본값이다. 따라서 clean benchmark 정확도보다 **열화 조건에서의 강건성**이 실용적 판단 기준이 된다.

## Key Ideas

### 접근 분류

- **Correspondence-based**: 대응점을 먼저 찾고 변환을 푼다.
  - 반복 최적화형: ICP 계열. 대응점 탐색과 변환 추정을 번갈아 한다.
  - 학습 feature형: DCP 등. 학습된 feature로 대응을 찾고 변환을 한 번에 푼다.
  - 약점: 대응점 탐색이 noise, incompleteness, density 변화에 직접 노출된다.
- **Direct (correspondence-free)**: 대응점 없이 변환을 추정한다.
  - Feature metric형: PointNetLK, FMR, DeepGMR. feature 차이를 최소화한다. Outlier가 distance metric을 왜곡한다.
  - Implicit surface형: 전통적으로는 implicit polynomial fitting. 표현력 한계로 smooth surface에만 통했다. Neural implicit representation이 이 한계를 풀었다. → [[SDFReg Point Cloud Registration]]

### 평가

- 회전 오차: $\arccos((\mathrm{trace}(R_{gt}^{-1}\hat{R})+1)/2)$, degree.
- 병진 오차: $\|t_{gt} - \hat{t}\|_2$, meter.
- MAE와 RMSE를 함께 본다. **MAE는 좋은데 RMSE가 크게 벌어지면 소수의 큰 실패가 있다는 뜻**이고, 로봇 적용에서는 이 tail이 평균보다 중요하다.
- 강건성은 clean/noise/partial/density 조건 전체에 걸친 표준편차로 본다.

### 열화 조건

- Gaussian noise: 좌표별 독립 noise.
- Partial visibility: 완전한 3D model 대 2.5D scan. 실제 로봇에서 가장 흔한 조건이다.
- Density 변화: 센서 거리, 해상도 차이. 20배 차이에서 실행조차 못 하는 방법이 있다.
- 낮은 overlap: 현재 위키에 있는 자료로는 다루지 못한 영역. 열린 질문:

## Related Papers

- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]] — neural SDF를 target 표현으로 써서 대응점 없이 정렬한다.

## Related Concepts

- [[Neural Implicit Surface Representation]] — implicit 방식 registration의 표현 기반.
- [[Signed Distance Field Collision Detection]] — 같은 SDF 표현을 접촉 계산에 쓰는 축.
- [[Tangled-Prone Bin Picking]] — 물체 pose 추정 정확도가 직접 영향을 주는 응용.
- [[Physical AI]]

## Open Questions

- Overlap이 50% 이하로 떨어질 때 correspondence-free 방법의 한계는 어디인가?
- Registration 오차가 grasp 성공률로 전파되는 관계를 정량화한 자료가 있는가?
- 로봇 온라인 loop에서 요구되는 registration latency 예산은 얼마인가? 위키 안에 근거 자료가 아직 없다.
- Deformable object에 대한 registration은 어떻게 다뤄야 하는가? → [[Robotic Cloth Manipulation]]과 연결될 여지가 있다.
