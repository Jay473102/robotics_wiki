---
type: concept
status: draft
created: 2026-06-16
updated: 2026-06-16
tags:
  - collision-detection
  - signed-distance-field
  - contact-simulation
sources:
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
  - raw/papers/2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation.pdf
---

# Signed Distance Field Collision Detection

## Definition

Signed Distance Field Collision Detection은 물체 표면까지의 signed distance를 나타내는 함수 $f_{\mathrm{SDF}}(x)$를 사용해 collision 여부, penetration depth, contact normal, contact point를 계산하는 접근이다.

## Why It Matters

로봇 manipulation, assembly, locomotion, contact-rich simulation에서는 non-convex object 사이의 접촉을 안정적으로 처리해야 한다. Mesh primitive끼리 직접 collision을 계산하거나 convex decomposition에 의존하면 복잡한 형상에서 어렵고, SDF는 복잡한 geometry를 implicit하게 다루면서 contact 계산으로 연결하기 쉽다.

## Key Ideas

- SDF 값이 음수이면 내부 penetration, 양수이면 외부, 0이면 surface로 해석한다.
- Node-SDF는 한 물체의 node를 다른 물체의 SDF에 query하는 단순한 방식이다.
- Face-SDF는 face 위에서 SDF를 최소화하는 최적화 문제로 contact를 찾기 때문에 edge-edge contact나 큰 face에서 더 robust할 수 있다.
- Voxel-SDF는 query가 빠르지만 resolution과 memory가 trade-off된다.
- [[NeuralSDF Collision Detection]]은 memory와 generalization 가능성을 얻는 대신 query마다 network inference 비용이 생긴다.
- [[Tetra-Encoded Signed Distance Field]]는 tetrahedron별 candidate face set을 encoding해 localized exact-distance query를 수행한다.

## Related Papers

- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]
- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]]

## Related Concepts

- [[Tetra-Encoded Signed Distance Field]]
- [[NeuralSDF Collision Detection]]
- [[Differentiable Dynamics]]
- [[Physical AI]]

## Open Questions

- Scene 안에서 voxel, analytic primitive, NeuralSDF, TE-SDF를 어떤 기준으로 hybrid하게 선택해야 하는가?
- SDF approximation error가 contact solver instability로 이어지는 경로를 어떻게 계측할 수 있는가?
- Safety-critical planning에서 SDF collision detector가 conservative bound를 제공하려면 어떤 representation이 필요한가?
