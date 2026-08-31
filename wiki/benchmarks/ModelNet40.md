---
type: benchmark
status: draft
created: 2026-08-01
updated: 2026-08-01
tags:
  - point-cloud-registration
  - benchmark
sources:
  - raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf
---

# ModelNet40

## Snapshot

40개 물체 class에 걸친 12,311개 CAD model로 이루어진 합성 3D shape 데이터셋. 원래는 3D shape classification용(Wu et al. 2015, 3D ShapeNets)이지만, point cloud registration 연구에서 표준 합성 benchmark로 널리 쓰인다.

## Task Definition

Registration 용도로 쓸 때는 CAD model에서 point를 sampling해 source로 삼고, 알려진 rigid transformation을 가해 target을 만든 뒤 그 변환을 복원하도록 한다. 정답 변환이 알려져 있으므로 오차를 정확히 측정할 수 있다.

## Data / Scale

- 12,311 CAD model, 40 class.
- Registration 실험의 관례적 분할(PointNetLK 설정): 20 class 학습, 나머지 20 class 테스트. 학습에서 보지 못한 category로 평가하므로 **cross-category 일반화**를 측정한다.
- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]의 설정: 1024점 균일 sampling, 원점 기준 $[0,1]^3$ 정규화, 축별 회전 $[0, 45°]$, 병진 $[-0.5, 0.5]$.

## Metrics

회전·병진 오차의 MAE와 RMSE. 정의는 [[Point Cloud Registration]] 참조.

## Known Results

[[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]] 기준 (unseen categories, 회전 RMSE [deg] / 병진 RMSE [m]):

| Method | Clean | Noise | Partial (70%) | Density (20x) |
|---|---|---|---|---|
| ICP | 23.751 / 0.5951 | 23.459 / 0.0585 | 31.645 / 0.1279 | 23.976 / 0.0612 |
| DCP-V2 | 3.5501 / 0.0050 | 12.850 / 0.0381 | 43.275 / 0.1168 | 59.627 / 0.0318 |
| IFR | 5.0707 / 0.0554 | 11.335 / 0.1271 | 11.728 / 0.0233 | 9.3591 / 0.1122 |
| SDFReg | 3.1540 / 0.0048 | 9.1780 / 0.0089 | 11.596 / 0.0103 | 8.839 / 0.0098 |

DeepGMR은 density 20배 조건에서 실행되지 않는다.

## Caveats

- **합성 데이터다.** CAD model에서 균일 sampling한 point cloud는 실제 depth sensor 출력과 noise 구조가 다르다. 실 센서 특유의 결측, 반사, 시점 의존 결함이 없다.
- 열화 조건(noise, partial, density)이 인위적으로 주입된다. 논문마다 주입 방식이 달라 서로 다른 논문의 수치를 직접 비교하기 어렵다.
- 20/20 class 분할은 관례일 뿐 표준 규격이 아니다. 어떤 class를 어느 쪽에 넣었는지에 따라 결과가 달라질 수 있다.
- 물체 단위 shape이므로 장면 수준 registration의 난이도를 반영하지 않는다. 실 장면 평가는 [[3DMatch]]로 보완한다.

## Related Papers

- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]

## Open Questions

- ModelNet40에서의 강건성 순위가 실제 로봇 센서 데이터에서도 유지되는가?
- 합성 noise 주입과 실제 depth sensor noise의 차이가 방법 순위를 바꾸는가?
