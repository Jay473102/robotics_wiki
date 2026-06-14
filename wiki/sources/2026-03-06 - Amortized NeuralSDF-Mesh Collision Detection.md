---
type: source
status: ingested
created: 2026-06-15
updated: 2026-06-15
tags:
  - source
  - paper
  - collision-detection
  - neural-sdf
  - contact-simulation
sources:
  - raw/papers/0c0760_a300ee12f6054b399ed0e4b4af409ca6.pdf
---

# Amortized NeuralSDF-Mesh Collision Detection Source

## Source

- Raw file: `raw/papers/0c0760_a300ee12f6054b399ed0e4b4af409ca6.pdf`
- Title: "Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation"
- Authors: Jinhee Yun, Jeongmin Lee, Sunkyung Park, Dongjun Lee
- Affiliation: Seoul National University; Holiday Robotics
- Date in PDF metadata: 2026-03-06
- Venue / identifier: 검증 필요. PDF 안에서 arXiv ID, DOI, 학회명은 확인하지 못했다.

## Extraction Summary

이 논문은 NeuralSDF와 triangle mesh 사이의 collision detection을 반복 최적화로 풀지 않고, KKT optimality condition을 학습 loss로 사용한 amortized model이 한 번의 forward pass로 contact point를 예측하도록 만든다.

핵심 문제는 NeuralSDF가 voxel SDF보다 연속적이고 메모리 효율적이지만, SDF query마다 neural network forward pass가 필요해 반복 최적화 기반 contact detection에서는 느리다는 점이다. 논문은 NeuralSDF-triangle collision을 barycentric coordinate에 대한 constrained optimization으로 정의하고, 여기서 나온 조건을 이용해 unsupervised learning objective를 구성한다.

## Evidence Notes

- 논문은 NeuralSDF-mesh collision을 triangle 단위로 분해하고, 각 triangle 안에서 signed distance가 최소가 되는 contact point를 찾는 문제로 정식화한다.
- 모델은 auto-decoder 구조와 dynamic code cloud 기반 shape feature를 사용해 category-level generalization을 시도한다.
- 실험은 Mug-Rack, Bottle-Holder, Gear-Gear, Bolt-Nut contact simulation scenario를 포함한다.
- Table II 기준 NeuralSDF+Ours는 NeuralSDF+Frank-Wolfe보다 빠르고, VoxelSDF+Frank-Wolfe보다 훨씬 적은 메모리를 쓰지만 contact 수/품질은 완전히 동일하지 않다.
- 한계로는 training triangle size 분포 밖의 mesh에서 성능 저하 가능성, NeuralSDF 표현 품질 의존성, high-precision contact에서 추가 refinement 필요성이 제시된다.

## Notes / Marginalia

- PDF 내부에서 `/Annots`, `/Text`, `/Highlight`, `/Ink` marker를 검색했지만 사용자 highlight/text/ink note는 확인하지 못했다.

## Created / Updated

- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]]
- [[NeuralSDF Collision Detection]]
- [[Amortized NeuralSDF-Mesh Collision Detection]]

## Open Questions

- 이 방법이 기존 simulator의 narrow-phase collision pipeline에 들어갈 때 batching, GPU/CPU transfer, contact solver coupling까지 포함한 end-to-end latency가 얼마나 줄어드는가?
- 학습된 contact predictor를 warm start로 쓰고 Frank-Wolfe refinement를 붙이는 hybrid 방식이 contact stability와 속도 사이에서 어떤 Pareto frontier를 만드는가?
