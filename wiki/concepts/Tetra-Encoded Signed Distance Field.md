---
type: concept
status: draft
created: 2026-06-16
updated: 2026-06-16
tags:
  - signed-distance-field
  - collision-detection
  - tetrahedral-mesh
  - contact-simulation
sources:
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
---

# Tetra-Encoded Signed Distance Field

## Definition

Tetra-Encoded Signed Distance Field, 줄여서 TE-SDF 또는 TES는 tetrahedral mesh의 각 tetrahedron에 대해 그 내부 query point에서 closest surface가 될 수 있는 surface face 집합 $E_t$를 저장하는 SDF representation이다.

## Why It Matters

Dense voxel SDF는 tight tolerance collision detection에서 memory cost가 커진다. TE-SDF는 tetrahedral mesh의 adaptive spatial discretization을 사용해 geometry가 복잡한 곳에 더 많은 tetrahedra를 배치하고, 각 tetrahedron 내부의 SDF query를 몇 개의 point-triangle distance 계산으로 줄인다.

## Key Ideas

- Tetrahedron $t$마다 encoded face set $E_t$를 둔다.
- Query point $x \in t$에 대해 전체 surface face set $F$ 대신 $E_t$만 검사해 $d(x,F)=d(x,E_t)$를 계산한다.
- Encoding 단계에서는 gap function과 Lipschitz pruning, GPU sampling을 사용해 후보 face를 찾는다.
- Distance-ordered truncation으로 encoded face 수를 제한하면 memory와 runtime을 줄일 수 있지만 deep interior SDF accuracy가 떨어질 수 있다.
- Near-surface exactness가 collision detection에서 특히 중요하다.

## Related Papers

- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]

## Related Concepts

- [[Signed Distance Field Collision Detection]]
- [[TE-SDF Collision Detection]]
- [[NeuralSDF Collision Detection]]

## Open Questions

- Tetrahedralization resolution과 encoded face truncation을 task tolerance에 맞게 자동 선택할 수 있는가?
- Deformable body simulation에서 runtime deformation이 커질 때 TE-SDF exactness-band는 얼마나 빨리 무너지는가?
- Exterior tetrahedral region을 어디까지 만들지 결정하는 task-aware 기준은 무엇인가?
