---
type: method
status: draft
created: 2026-06-16
updated: 2026-06-21
tags:
  - collision-detection
  - signed-distance-field
  - gpu-simulation
  - contact-simulation
sources:
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
  - raw/notes/논문 학습 자료 요청.pdf
---

# TE-SDF Collision Detection

## Summary

TE-SDF Collision Detection은 [[Tetra-Encoded Signed Distance Field]]를 GPU collision detector로 사용하는 방법이다. Preprocessing에서 tetrahedron별 encoded face set을 만들고, runtime에는 Node-TES 또는 Face-TES query를 통해 contact feature를 생성한다.

## Workflow

1. Surface mesh를 tetrahedralize한다.
2. 각 tetrahedron에 대해 closest face가 될 수 있는 encoded face set $E_t$를 계산한다.
3. 필요하면 distance-ordered truncation으로 최대 encoded face 수 $E_{\max}$를 제한한다.
4. Runtime broad/middle phase가 생성한 candidate pair에 대해 Node-TES 또는 Face-TES narrow phase를 실행한다.
5. 생성된 contact feature를 GPU-accelerated dynamics solver에 넘긴다.

## Implementation Notes

- 논문은 GPU thread를 sampling point 또는 node-tetrahedron pair에 할당하는 식으로 construction/query를 병렬화한다.
- Face-TES narrow phase에서는 encoded faces를 thread-wise로 중복 fetch하면 register pressure와 local memory spill이 생길 수 있어 warp-wise parallelism을 사용한다.
- Distance-ordered truncation은 near-surface collision에는 충분할 수 있지만, deep penetration SDF accuracy에는 손실을 만들 수 있다.

## When To Use

- Tight tolerance assembly처럼 voxel resolution을 높이면 메모리가 폭증하는 경우.
- 한 scene에 복잡한 mesh가 많고 GPU simulation 안에서 많은 collision query가 필요한 경우.
- Exact mesh surface distance에 가까운 SDF query가 필요하지만 dense voxel grid는 비싼 경우.

## Failure Modes

- Tetrahedral mesh 품질이 나쁘면 encoded face set과 query stability가 흔들릴 수 있다.
- Contact feature 수가 많아져 solver coupling 비용이 늘 수 있다.
- Deep penetration 상황에서는 aggressive truncation이 inaccurate SDF를 만들 수 있다.

## Related

- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]
- [[Signed Distance Field Collision Detection]]
- [[NeuralSDF Collision Detection]]
- [[Amortized NeuralSDF-Mesh Collision Detection]]
