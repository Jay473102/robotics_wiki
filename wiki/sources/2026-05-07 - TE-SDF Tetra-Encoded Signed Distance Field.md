---
type: source
status: ingested
created: 2026-06-16
updated: 2026-06-16
tags:
  - source
  - paper
  - collision-detection
  - signed-distance-field
  - contact-simulation
sources:
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
---

# TE-SDF Tetra-Encoded Signed Distance Field Source

## Source

- Raw file: `raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf`
- Title: "TE-SDF: Tetra-Encoded Signed Distance Field for Memory-Efficient and Accurate Collision Detection"
- Authors: Harim Ji, Yongseok Lee, Dongjun Lee
- Affiliation: Seoul National University; DGIST
- Date in PDF metadata: 2026-05-07
- Public resources in PDF: `https://github.com/HarimJi/TES-sdk`, `https://github.com/HarimJi/TES-Encoder`
- Venue / identifier: 검증 필요. PDF 안에서 arXiv ID, DOI, 학회명은 확인하지 못했다.

## Extraction Summary

이 논문은 복잡한 형상 사이의 contact-rich collision detection을 위해 Tetra-Encoded SDF, 줄여서 TES 또는 TE-SDF를 제안한다. 핵심은 tetrahedral mesh의 adaptive spatial discretization을 사용하고, 각 tetrahedron마다 그 내부 query point에서 closest surface가 될 수 있는 후보 surface face 집합을 compact하게 저장하는 것이다.

Voxel-SDF는 query가 빠르지만 tight tolerance geometry에서 메모리가 급격히 증가한다. Neural SDF 계열은 메모리 효율적일 수 있지만 query마다 neural network inference나 tree traversal이 필요해 Face-SDF 같은 반복 최적화 기반 collision detection에 부담이 된다. TE-SDF는 각 tetrahedron 내부의 SDF query를 소수의 point-triangle distance 계산으로 국소화해 GPU-friendly한 collision detector를 만든다.

## Evidence Notes

- PDF abstract는 TE-SDF가 tetrahedral mesh의 adaptive discretization과 tetrahedron별 candidate surface face encoding을 결합한다고 설명한다.
- Table I은 M16 bolt, nut, hole, shaft, spoon, gripper 등에 대해 encoded face 수, memory, max error, exactness-band를 보고한다.
- Table II는 Robo-assembly, Chained SAM, Engine transmission, Bolt-nut, Peg-in-hole, Pile of shafts에서 Face-TES collision detection의 broad/middle/narrow phase time과 memory를 보고한다.
- Table III은 bolt-nut 및 peg-in-hole tight tolerance 실험에서 TE-SDF가 voxel-SDF보다 훨씬 적은 메모리로 성공했다고 보고한다. 예: bolt-nut 비교에서 voxel-SDF 1024/1024는 약 1007.52 MB, TES는 약 3.69 MB로 보고된다.
- Discussion은 Face-TES가 overlapping face-tetrahedron pair마다 contact feature를 만들기 때문에 second-order solver나 sequential update solver에서는 contact constraint가 과도해질 수 있다고 지적한다.

## Notes / Marginalia

PDF annotation marker 검색에서 `/Annots`는 확인됐지만 `/Highlight`, `/Ink`, `/QuadPoints`, `/InkList` 등 사용자 highlight/text/ink note로 볼 만한 marker는 확인하지 못했다. 논문 내 GitHub/참고문헌 링크로 인한 annotation일 가능성이 높다.

## Created / Updated

- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]
- [[Signed Distance Field Collision Detection]]
- [[Tetra-Encoded Signed Distance Field]]
- [[TE-SDF Collision Detection]]

## Open Questions

- TE-SDF의 encoding 비용은 asset pipeline에서 어느 정도까지 amortize될 수 있는가?
- Tetrahedralization 품질과 exterior tetrahedral region 설계가 contact stability에 미치는 영향은 어떻게 진단할 수 있는가?
- Face-TES의 contact feature 수 증가를 contact clustering이나 solver-level pruning으로 줄일 때 안정성과 속도의 Pareto frontier는 어떻게 변하는가?
