---
type: concept
status: draft
created: 2026-08-01
updated: 2026-08-01
tags:
  - neural-implicit-representation
  - signed-distance-field
  - neural-sdf
  - point-cloud-registration
  - collision-detection
sources:
  - raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf
  - raw/papers/2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation.pdf
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
---

# Neural Implicit Surface Representation

## Definition

Neural Implicit Surface Representation은 3D 형상을 삼각형이나 voxel 같은 명시적 원소가 아니라, 공간의 점을 입력받아 스칼라를 내는 학습된 연속 함수로 표현하는 방식이다. 표면은 그 함수의 level set으로 정의된다.

가장 널리 쓰이는 형태가 signed distance function이다.

$$\Phi: \mathbb{R}^3 \to \mathbb{R}, \qquad \Phi(x) \approx \mathrm{SDF}(x), \qquad \text{surface} = \{x : \Phi(x) = 0\}$$

부호는 내부(음)와 외부(양)를 구분하고, 절대값은 가장 가까운 표면까지의 거리다.

## Why It Matters

이 위키에서 SDF는 서로 다른 두 축에서 각각 등장했다. 접촉 계산 축([[Signed Distance Field Collision Detection]], [[NeuralSDF Collision Detection]], [[Tetra-Encoded Signed Distance Field]])과 지각 축([[Point Cloud Registration]])이다. 이 페이지는 두 축이 **같은 표현을 공유한다**는 사실을 명시적으로 두기 위해 존재한다.

공유되는 성질은 세 가지다.

1. **연속성과 미분 가능성** — $\nabla\Phi$를 backpropagation으로 얻을 수 있고, 이 gradient가 그대로 최적화에 쓰인다. 접촉에서는 contact normal이 되고, registration에서는 pose Jacobian의 구성 요소가 된다.
2. **거리 자체가 의미를 가진다** — penetration depth이자 정렬 오차다. 별도의 metric 설계가 필요 없다.
3. **Non-convex 형상을 분해 없이 다룬다** — convex decomposition이나 mesh 단순화를 거치지 않는다.

공통 비용도 있다. Query마다 network forward pass가 필요하고, 이것이 두 축 모두에서 병목이 된다.

## Key Ideas

### 정규화

Eikonal 항이 gradient norm을 1로 강제해 함수가 실제 거리장이 되도록 만든다.

$$\mathcal{L}_{eikonal} = \frac{1}{|X|}\sum_j (\|\nabla\Phi(x_j)\|_2 - 1)^2$$

이것 없이는 부호는 맞아도 크기가 거리가 아닌 함수로 수렴할 수 있고, 그러면 gradient 기반 최적화가 왜곡된다. SDFReg ablation에서 Eikonal 유무가 rotation MAE 4.14 대 2.59로 나타난다.

### 조건부 SDF와 일반화

$\Phi(x \mid z)$처럼 shape feature $z$로 조건화하면 형상마다 network를 다시 학습하지 않아도 된다. 미지 category에 대해 pose를 추론해야 하는 registration에서 이 성질이 필수적이다.

### Query 비용을 줄이는 전략

같은 병목에 대해 위키 안에 세 가지 다른 대응이 있다.

| 전략 | 접근 | 대표 |
|---|---|---|
| 자료구조로 국소화 | tetrahedron별 candidate face set을 미리 encoding | [[Tetra-Encoded Signed Distance Field]] |
| 반복 최적화를 학습으로 대체 | iterative solve를 amortized predictor로 치환 | [[Amortized NeuralSDF-Mesh Collision Detection]] |
| 반복을 학습 루프 안에 넣음 | SDF 최적화와 pose 최적화를 교대 | [[SDFReg Point Cloud Registration]] |

추론: 앞의 둘은 query 비용을 줄이는 방향이고 세 번째는 오히려 비용을 감수하고 정확도를 얻는 방향이다. 세 논문 모두 자신의 비용을 같은 기준으로 보고하지 않아 직접 비교는 불가능하다.

## Related Papers

- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]] — registration의 distance metric으로 사용.
- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]] — contact 계산에 사용.
- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]] — exact-distance query를 위한 encoding.

## Related Concepts

- [[Signed Distance Field Collision Detection]]
- [[NeuralSDF Collision Detection]]
- [[Tetra-Encoded Signed Distance Field]]
- [[Point Cloud Registration]]
- [[Differentiable Dynamics]]
- [[Physical AI]]

## Contradictions / Updates

없음. 현재 링크된 세 논문은 서로 다른 응용을 다루며 충돌하는 주장이 없다.

## Open Questions

- 지각에서 만든 SDF를 접촉 계산에 그대로 쓸 수 있는가? → [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]
- Registration에 충분한 SDF 정확도와 contact solver 안정성에 필요한 SDF 정확도는 같은 수준인가?
- 세 전략(TE-SDF, amortization, 교대 최적화)의 query 비용을 공통 기준으로 비교한 자료가 있는가?
