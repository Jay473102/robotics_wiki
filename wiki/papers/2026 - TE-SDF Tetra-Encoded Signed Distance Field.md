---
type: paper
status: draft
created: 2026-06-16
updated: 2026-06-16
tags:
  - collision-detection
  - signed-distance-field
  - contact-simulation
  - gpu-simulation
  - tetrahedral-mesh
sources:
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
title: "TE-SDF: Tetra-Encoded Signed Distance Field for Memory-Efficient and Accurate Collision Detection"
authors:
  - Harim Ji
  - Yongseok Lee
  - Dongjun Lee
year: 2026
venue: 검증 필요
doi:
url:
---

# TE-SDF: Tetra-Encoded Signed Distance Field for Memory-Efficient and Accurate Collision Detection

## TL;DR

TE-SDF는 SDF를 dense voxel grid나 neural network로 저장하지 않고, tetrahedral mesh의 각 tetrahedron에 가까운 후보 surface face 집합을 encoding해 query를 소수의 point-triangle distance 계산으로 바꾸는 표현이다. 논문은 이 표현을 GPU-accelerated collision detector로 구현하고, robot assembly, chain spool, gear transmission, pile of shafts 같은 contact-rich simulation에서 수 MB에서 수십 MB 수준의 메모리와 millisecond 수준의 collision detection time을 보고한다. Voxel-SDF 대비 tight tolerance assembly에서 메모리 효율과 accuracy를 동시에 얻는 것이 핵심 주장이다.

## Problem

Contact-rich robotics simulation에서는 복잡한 non-convex mesh 사이의 collision/contact를 빠르고 정확하게 계산해야 한다. Voxel-SDF는 query가 단순하고 빠르지만 grid resolution이 올라가면 memory footprint가 $O(n^3)$로 커지고, tight tolerance assembly에서는 discretization artifact가 문제가 된다.

Memory-efficient SDF 표현으로 octree, polynomial local function, neural SDF 등이 있지만, tree traversal이나 neural network inference가 필요해 Face-SDF처럼 per-face optimization을 반복하는 collision detection에서는 query overhead가 커질 수 있다.

## Core Idea

TE-SDF는 tetrahedral mesh의 adaptive spatial discretization과 exact point-triangle distance evaluation을 결합한다. 어떤 query point $x$가 tetrahedron $t$ 내부에 있다고 할 때, 전체 surface face $F$를 모두 보지 않고 $t$에 대해 미리 encoding된 후보 face 집합 $E_t$만 검사한다.

즉 $E_t$는 tetrahedron $t$ 내부의 어떤 점에서든 closest face가 될 수 있는 surface faces의 compact set이다. 그러면 SDF query는 다음처럼 local distance evaluation으로 줄어든다.

$$
d(x,F) = d(x,E_t)
$$

## Method

논문은 각 face $f$에 대해 gap function $g_f(x)=d(x,f)-d(x,F)$를 정의하고, tetrahedron 내부에 $g_f(x)=0$인 점이 있으면 $f$를 $E_t$에 포함한다. 모든 face를 brute force로 검사하지 않기 위해 Lipschitz pruning으로 candidate face set을 줄이고, 이후 GPU-accelerated brute force sampling으로 encoded face set을 만든다.

Runtime collision detection에서는 두 가지 방식을 구현한다.

- `Node-TES`: 한 mesh의 node를 다른 mesh의 TE-SDF에 query한다.
- `Face-TES`: face 단위 최적화 기반 contact feature를 만들며, warp-wise parallelism으로 encoded face fetch와 distance evaluation을 처리한다.

## Data / Embodiment

실험 asset은 M16 bolt, nut, hole, shaft, spoon, gripper 등을 포함한다. Simulation scenario는 Robo-assembly, Chained suspended aerial manipulator, Engine transmission, Bolt-nut, Peg-in-hole, Pile of shafts로 구성된다. Robo-assembly는 세 개의 peg-in-hole과 일곱 개의 bolt-nut assembly를 포함하는 장기 assembly task로 설명된다.

## Evaluation

평가는 세 축이다.

- TE-SDF encoding 결과: encoded face 수, memory, max error, exactness-band, 1% error-band.
- GPU-accelerated simulation: broad/middle/narrow phase time, memory, narrow-phase query 수.
- Voxel-SDF 비교: bolt-nut 및 peg-in-hole tight tolerance에서 success/failure와 memory footprint.

모든 실험은 Intel Core i9-13900K CPU와 NVIDIA RTX 5090 GPU PC에서 수행됐다고 보고한다.

## Results

- Table II 기준 Face-TES는 Robo-assembly 5.80 MB, Chained SAM 52.91 MB, Engine transmission 8.05 MB, Bolt-nut 3.69 MB, Peg-in-hole 2.59 MB, Pile of shafts 88.24 MB를 보고한다.
- 같은 Table II에서 narrow phase time은 Robo-assembly 0.10 ms, Chained SAM 0.49 ms, Engine transmission 0.08 ms, Bolt-nut 0.14 ms, Peg-in-hole 0.21 ms, Pile of shafts 0.05 ms로 보고된다.
- Table III에서 bolt-nut tight tolerance 비교 시 voxel-SDF 1024/1024는 약 1007.52 MB, TES는 약 3.69 MB로 보고된다.
- Peg-in-hole 비교에서도 voxel-SDF 1024/1024는 약 815.03 MB, TES는 약 2.59 MB로 보고된다.
- Appendix의 voxel-SDF 분석은 M16 bolt에서 1024 grid도 lower-bound Hausdorff distance 40 µm를 보이며, 25 µm tolerance setting을 넘는다고 설명한다.

## Limitations

- TE-SDF encoding은 tetrahedralization 품질, exterior tetrahedral region 설정, sampling density, truncation setting에 의존한다.
- Face-TES는 overlapping face-tetrahedron pair마다 contact feature를 만들 수 있어 contact constraint 수가 많아질 수 있다.
- 저자들은 second-order solver나 projected Gauss-Seidel 같은 sequential update method와 결합할 때 contact feature 과다 문제가 생길 수 있으며, contact clustering이 가능한 해결책이라고 제안한다.
- 논문은 soft-body simulation으로의 확장을 promising direction으로 제시하지만, 본문 실험의 중심은 rigid/contact-rich assembly scenario다.
- 검증 필요: PDF 안에서 peer-review 상태, arXiv ID, DOI는 확인하지 못했다.

## Connections

- [[Signed Distance Field Collision Detection]]: TE-SDF는 SDF collision detection의 memory-efficient representation이다.
- [[Tetra-Encoded Signed Distance Field]]: 논문이 제안한 핵심 representation.
- [[TE-SDF Collision Detection]]: GPU collision detector 구현 패턴.
- [[NeuralSDF Collision Detection]]: Neural SDF가 memory-efficient representation인 반면 TE-SDF는 tetrahedralized local exact-distance encoding으로 query overhead를 줄이는 대안이다.
- [[Differentiable Dynamics]]: 빠르고 안정적인 contact query는 differentiable 또는 GPU-accelerated simulator의 병목을 줄이는 substrate가 될 수 있다.

## Contradictions / Updates

기존 [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]]은 NeuralSDF query 병목을 amortized predictor로 줄이는 방향이고, 이 논문은 NeuralSDF 대신 tetrahedralized exact-distance encoding으로 같은 SDF collision bottleneck을 다룬다. 둘은 충돌이라기보다 SDF representation/query-cost trade-off의 서로 다른 해법으로 보는 것이 적절하다.

## Notes / Marginalia

PDF annotation marker 검색에서 `/Annots`는 확인됐지만 `/Highlight`, `/Ink`, `/QuadPoints`, `/InkList` 등 사용자 highlight/text/ink note는 확인하지 못했다.

## Open Questions

- TE-SDF encoding을 대규모 asset library에 적용할 때 preprocessing time, tetrahedralization failure, memory budget을 어떻게 관리해야 하는가?
- TE-SDF와 NeuralSDF/amortized contact predictor를 scene 안에서 hybrid하게 섞는 기준은 무엇인가?
- Contact feature clustering을 적용하면 Face-TES의 solver coupling 비용과 physical realism이 어떻게 trade-off되는가?
