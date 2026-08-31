---
type: benchmark
status: draft
created: 2026-09-01
updated: 2026-09-01
tags:
  - benchmark
  - grasping
  - manipulation
sources:
  - raw/papers/2608.26076v1.pdf
  - https://arxiv.org/abs/2011.09584
---

# ACRONYM

## Snapshot

시뮬레이션 기반 대규모 grasp 데이터셋 (Eppner, Mousavian, Fox — NVIDIA, ICRA 2021). 물체 mesh에 parallel-jaw grasp pose와 물리 시뮬레이션으로 판정한 성공 라벨을 부여한다. $SE(3)$ grasp 분포 학습 연구의 표준 학습·평가 데이터로 쓰인다.

## Task Definition

물체 형상(mesh 또는 그로부터 샘플링한 point cloud)이 주어졌을 때 안정적인 6-DoF parallel-jaw grasp pose를 생성·예측한다.

## Data / Scale

- 전체 규모: 검증 필요 — 위키는 아직 원 논문 미확보. GraspMF가 사용한 부분집합은 10개 카테고리(Book, Bottle, Bowl, Cap, CellPhone, Cup, Hammer, Mug, Scissors, Shampoo) 416개 인스턴스, 유효 grasp ~780K (Tier A: GraspMF 본문).
- OOD 평가용으로 별도 카테고리(Car, Donut, Laptop, Pencil, RubiksCube, Spoon)를 떼어 쓰는 관행이 있다.

## Metrics

ACRONYM 자체는 데이터셋이고, 평가는 통상 다음을 결합한다 (SE3Dif 이후 관행):

- **성공률(SR)**: 생성 grasp을 Isaac Gym에서 open→approach→close→lift + shake 프로토콜로 실행해 판정.
- **EMD**: 생성 grasp 집합과 ground-truth 집합 사이 pose 거리($SO(3)$ geodesic + 가중 Euclidean)의 Earth Mover's Distance — 분포 커버리지 proxy.

## Known Results

[[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]]의 프로토콜(위 부분집합) 기준: GraspMF T=5가 ID SR 87.40% / OOD 71.73%로 SE3Dif, EquiGraspFlow, BRIDGER, VSIGD를 상회. 자세한 표는 paper 페이지 참조.

## Caveats

- 시뮬레이션 판정 grasp이므로 sim-to-real 격차가 내재한다. 실기 검증은 별도로 필요하다.
- 논문마다 사용하는 카테고리 부분집합·분할이 달라 수치의 논문 간 직접 비교는 주의해야 한다.
- EMD는 reference grasp set의 구성(예: 가시 표면 제한)에 민감하다 — GraspMF 부분 관측 실험에서 확인된 metric 한계.

## Related Papers

- [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]] — evaluated-on.

## Open Questions

- 원 논문(arXiv:2011.09584)의 전체 규모·생성 절차를 ingest해서 이 페이지를 채울 것.
