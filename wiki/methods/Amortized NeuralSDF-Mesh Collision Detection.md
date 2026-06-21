---
type: method
status: draft
created: 2026-06-15
updated: 2026-06-21
tags:
  - amortized-optimization
  - collision-detection
  - neural-sdf
  - contact-simulation
sources:
  - raw/papers/2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation.pdf
  - raw/chats/내용 파악 요약.pdf
---

# Amortized NeuralSDF-Mesh Collision Detection

## Summary

Amortized NeuralSDF-Mesh Collision Detection은 NeuralSDF와 mesh 사이의 contact point를 반복 최적화로 매번 찾는 대신, triangle 단위 최적화 문제의 해를 neural network가 직접 예측하도록 학습하는 방법이다. 핵심은 KKT optimality condition을 loss로 사용해 label 없이 contact predictor를 학습하는 것이다.

## Procedure

1. Mesh를 triangle set으로 본다.
2. NeuralSDF-triangle collision을 barycentric coordinate 최적화 문제로 쓴다.
3. KKT 조건에서 contact point가 만족해야 하는 optimality condition을 유도한다.
4. Vertex-level shape feature와 triangle-level shape feature를 입력으로 받는 auto-decoder형 model을 학습한다.
5. Simulation step에서는 candidate triangle마다 model forward pass로 contact point를 예측한다.
6. 필요한 경우 예측 contact를 Frank-Wolfe 같은 iterative solver의 warm start로 사용한다.

## Losses

논문이 강조하는 핵심 loss는 optimality loss다. 이는 contact point $p$에서 NeuralSDF gradient와 triangle vertex 관계가 KKT 조건을 만족하도록 만든다. Minimum signed distance loss도 함께 쓰이며, ablation 결과 optimality loss 제거 시 성능이 크게 나빠진다.

## When Useful

- Contact-rich simulation에서 동일한 category 물체를 반복적으로 다룰 때.
- VoxelSDF 메모리 비용이 너무 크거나 thin/complex geometry가 voxel resolution에 잘 잡히지 않을 때.
- NeuralSDF의 연속 표현이 필요하지만 반복 query 비용을 줄여야 할 때.
- Gradient-based manipulation/planning에 differentiable contact feature가 필요할 때.

## Failure Modes

- Triangle size가 training range와 다르면 contact prediction 품질이 떨어질 수 있다.
- NeuralSDF가 형상을 잘못 표현하면 contact도 잘못 예측된다.
- High-precision contact나 safety-critical collision avoidance에서는 approximate predictor만으로 부족할 수 있다.
- False negative contact는 simulation penetration이나 planning safety issue로 이어질 수 있다.

## Related Papers

- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]]

## Related Concepts

- [[NeuralSDF Collision Detection]]
- [[Differentiable Dynamics]]
- [[Physical AI]]
- [[2026-06-21 - What Does KKT Mean in Amortized NeuralSDF Contact Prediction]]

## Open Questions

- Candidate triangle selection까지 포함한 full broad-phase/narrow-phase pipeline에서 실시간성이 유지되는가?
- Conservative contact detection을 위해 uncertainty estimate나 fallback refinement를 어떻게 붙일 수 있는가?
