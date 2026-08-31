---
type: question
status: draft
created: 2026-08-01
updated: 2026-08-01
tags:
  - question
  - signed-distance-field
  - neural-implicit-representation
  - point-cloud-registration
  - collision-detection
sources:
  - raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf
  - raw/papers/2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation.pdf
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
---

# Can One SDF Representation Serve Perception and Contact?

지각(point cloud registration)에서 만든 SDF를 접촉 계산(collision detection)에 그대로 재사용할 수 있는가?

## Short Answer

현재 위키의 근거로는 **판단할 수 없다.** 두 축이 같은 SDF 표현을 쓴다는 점은 확실하지만, 요구하는 정확도 기준과 query 특성이 다르고, 이를 직접 비교한 자료가 아직 없다. 열린 질문:

## Why This Question Matters

로봇 파이프라인은 보통 지각과 시뮬레이션/제어를 분리된 표현으로 다룬다. 지각은 point cloud와 pose를, 접촉 계산은 mesh나 voxel SDF를 쓴다. 두 단계 사이에서 표현이 변환되며 오차와 지연이 생긴다.

만약 하나의 SDF가 둘 다를 감당한다면:

- Registration의 부산물로 얻은 연속 SDF를 collision query에 바로 쓸 수 있다. 표현 변환 단계가 사라진다.
- 관측한 물체를 실시간으로 시뮬레이터에 넣는 경로가 짧아진다. Sim-to-real의 real-to-sim 방향에 직접 영향을 준다.
- 반대로 요구 정확도가 다르다면, 지각용 SDF를 접촉에 쓰는 순간 solver instability가 생길 수 있다. 이 경우 분리 유지가 옳다.

이 판단은 향후 로봇 인식-시뮬레이션 파이프라인 설계에서 반복해 등장한다.

## Current Answer

### 확인된 것 (Tier A)

- SDFReg는 registration 과정에서 target point cloud의 연속 SDF $\Phi(x \mid Q)$를 만들며, 이는 shape feature로 조건화되어 미지 category에도 적용된다. ([[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]])
- Collision detection 쪽 연구들도 동일한 형태의 neural SDF를 query한다. ([[NeuralSDF Collision Detection]], [[Amortized NeuralSDF-Mesh Collision Detection]])
- 양쪽 모두 $\nabla\Phi$를 최적화에 사용한다. Registration에서는 pose Jacobian, contact에서는 contact normal이다.
- 양쪽 모두 query당 network forward pass 비용이 병목이다.

### 차이 (Tier A 근거 기반 정리)

| | 지각 (registration) | 접촉 (collision) |
|---|---|---|
| Query 지점 | 표면 근처로 수렴해 가는 source point | 표면 근처와 관통 내부 |
| 필요한 정확도 | 집계된 pose 오차가 작으면 됨 | 국소 penetration 값이 solver 안정성을 좌우 |
| 부호 영역 | 주로 외부 | 내부 부호와 크기가 결정적 |
| Query 빈도 | registration 1회당 최대 30 iteration | 시뮬레이션 step마다 다수 |

추론: 이 표에서 핵심 비대칭은 정확도 요구다. Registration은 개별 SDF 오차가 여러 점에 걸쳐 평균화되지만, contact solver는 국소 penetration 오차 하나에 불안정해질 수 있다. 즉 **지각용 SDF → 접촉용은 위험하고, 접촉용 SDF → 지각용은 상대적으로 안전할 가능성**이 있다. 이것은 위키 안 자료의 성질을 비교한 추론이며 실험으로 확인된 바 없다.

### 확인되지 않은 것

- SDFReg 논문은 계산 비용을 전혀 보고하지 않는다. 재사용의 실익을 계산할 근거가 없다.
- SDF 근사 오차가 contact solver instability로 이어지는 경로는 [[NeuralSDF Collision Detection]]과 [[Signed Distance Field Collision Detection]]에서 이미 열린 질문으로 남아 있다. 이 질문은 그 위에 얹혀 있다.
- 부분 관측(partial scan)으로 만든 SDF는 보이지 않는 뒷면이 부정확하다. 접촉 계산은 그 뒷면에서도 정확해야 할 수 있다. 이것이 가장 실질적인 장애물로 보인다. 검증 필요:

## Evidence / Sources

- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]] — 지각 축.
- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]] — 접촉 축, query 비용 문제.
- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]] — 정확한 거리 query를 위한 자료구조.
- [[Neural Implicit Surface Representation]] — 두 축의 공통 표현을 정리한 개념 페이지.

## Important Caveats

- 세 논문은 서로를 인용하지 않고 다른 공동체에서 나왔다. 비교는 이 위키에서 처음 이루어진 것이며 원저자들의 주장이 아니다.
- 세 논문 모두 계산 비용을 같은 기준으로 보고하지 않아 정량 비교가 불가능하다.
- 이 질문에 답하려면 최소한 다음이 필요하다. (1) 동일 물체에 대해 registration용 SDF와 접촉용 SDF의 국소 오차 분포 비교, (2) 그 오차를 contact solver에 넣었을 때의 안정성 측정, (3) partial observation 조건에서의 뒷면 오차 측정.

## Linked Pages

- [[Neural Implicit Surface Representation]]
- [[Point Cloud Registration]]
- [[Signed Distance Field Collision Detection]]
- [[NeuralSDF Collision Detection]]
- [[SDFReg Point Cloud Registration]]
- [[Amortized NeuralSDF-Mesh Collision Detection]]
- [[Tetra-Encoded Signed Distance Field]]
