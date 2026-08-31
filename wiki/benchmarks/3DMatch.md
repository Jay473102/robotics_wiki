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

# 3DMatch

## Snapshot

Kinect로 촬영한 실제 실내 RGB-D scan을 모은 registration benchmark (Zeng et al. 2017). 사무실, 호텔, 주방 등 여러 실내 장면의 복잡한 3D scan을 포함한다. 합성 데이터인 [[ModelNet40]]과 달리 **실제 센서 결함이 그대로 들어 있다.**

## Task Definition

실 장면 scan 쌍을 정렬한다. 원래는 local geometric descriptor 학습·평가용으로 만들어졌고, registration 연구에서는 실 데이터 평가 단계로 쓰인다.

## Data / Scale

- 여러 실내 데이터셋의 집합. RGB-D scan.
- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]의 설정: PointNetLK-Revisited를 따라 7-Scenes와 SUN3D에서 8개 scene category를 테스트로, 나머지를 학습으로 사용. 변환된 source를 target으로 삼고 회전 $[0, 60°]$, 병진 $[0, 1.0]$ 범위에서 무작위 sampling.

## Metrics

회전·병진 오차의 RMSE와 **median**. Median을 함께 보는 것이 중요하다. 실 데이터에서는 소수의 큰 실패가 RMSE를 지배하므로, 둘의 격차가 실패 tail의 크기를 보여준다.

## Known Results

[[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]] 기준:

| Method | R RMSE / Median [deg] | t RMSE / Median [m] |
|---|---|---|
| ICP | 24.772 / 4.501 | 1.064 / 0.149 |
| PointNetLK | 28.894 / 7.596 | 1.098 / 0.260 |
| DCP-V2 | 53.903 / 23.659 | 1.823 / 0.784 |
| DeepGMR | 32.729 / 16.548 | 2.112 / 0.764 |
| IFR | 23.814 / 4.191 | 1.057 / 0.161 |
| SDFReg | 15.623 / 3.1562 | 0.065 / 0.013 |

주목할 점: 모든 방법에서 RMSE와 median의 격차가 크다. SDFReg조차 median 3.16도 대 RMSE 15.6도로, 실 장면에는 여전히 큰 실패 사례가 남는다. **합성 데이터에서 좋은 방법이 실 데이터에서 그대로 좋지는 않다**는 것을 보여주는 사례다.

## Caveats

- 위 표는 논문 저자가 자체 실험 설정으로 재현한 결과다. 3DMatch 원 논문의 공식 리더보드 프로토콜과 다르며, 초기 pose 범위도 저자가 정했다. 따라서 다른 논문의 3DMatch 수치와 직접 비교하면 안 된다.
- 실내 정적 장면이다. 로봇 작업 공간의 동적 요소, 금속 반사, 근접 촬영 조건은 반영되지 않는다.
- 검증 필요: 위 수치는 SDFReg 논문 한 편에서만 확인했다. 각 baseline의 원 논문 보고값과 대조하지 않았다.

## Related Papers

- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]

## Related Concepts

- [[Point Cloud Registration]]

## Open Questions

- 실제 로봇 작업 셀(금속, 반사, 근접 거리)은 3DMatch보다 얼마나 더 어려운가? 대응하는 benchmark가 있는가?
- RMSE와 median의 격차를 줄이는 것, 즉 실패 tail을 없애는 것을 직접 목표로 삼은 registration 연구가 있는가?
