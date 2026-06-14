---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - collision-detection
  - neural-sdf
  - contact-simulation
  - signed-distance-function
sources:
  - raw/papers/0c0760_a300ee12f6054b399ed0e4b4af409ca6.pdf
---

# NeuralSDF Collision Detection

## Definition

NeuralSDF Collision Detection은 물체 형상을 signed distance function $f_{\mathrm{SDF}}: \mathbb{R}^3 \to \mathbb{R}$으로 표현하되, 이 SDF를 neural network로 parameterize한 뒤 collision/contact를 계산하는 접근이다.

## Why It Matters

VoxelSDF는 query가 빠르지만 해상도와 메모리 비용에 묶인다. NeuralSDF는 연속 표현, 더 높은 geometry fidelity, category-level generalization 가능성이 있지만 query마다 network forward pass가 필요하다. Contact-rich robotics simulation에서는 한 step 안에서도 많은 collision query가 필요하므로, NeuralSDF의 표현력과 query 비용 사이의 trade-off가 핵심 문제가 된다.

## Key Ideas

- SDF는 표면까지의 signed distance를 반환하므로 contact point, penetration, normal 계산에 직접 연결된다.
- Non-convex geometry를 convex decomposition 없이 implicit하게 다룰 수 있다.
- NeuralSDF는 voxel grid보다 메모리 효율적일 수 있지만, iterative optimization과 결합하면 속도 병목이 된다.
- Mesh와의 collision은 triangle 단위로 분해해 NeuralSDF-triangle distance minimization으로 풀 수 있다.
- [[Amortized NeuralSDF-Mesh Collision Detection]]처럼 반복 최적화를 학습된 predictor로 대체하면 속도 병목을 줄일 수 있다.

## Related Papers

- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]]

## Related Concepts

- [[Differentiable Dynamics]]
- [[Physical AI]]
- [[Simulation-Based Inference]]

## Open Questions

- NeuralSDF collision detector가 safety-critical planning에서 conservative collision bounds를 제공할 수 있는가?
- NeuralSDF의 geometric error가 contact solver instability로 이어지는 경로를 어떻게 진단할 수 있는가?
- VoxelSDF, analytic SDF, mesh collision, NeuralSDF를 scene 안에서 hybrid하게 섞는 최적 기준은 무엇인가?
