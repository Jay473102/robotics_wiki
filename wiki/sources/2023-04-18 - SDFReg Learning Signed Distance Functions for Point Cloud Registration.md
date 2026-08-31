---
type: source
status: ingested
created: 2026-08-01
updated: 2026-08-01
tags:
  - source
  - point-cloud-registration
  - signed-distance-field
  - neural-implicit-representation
sources:
  - raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf
  - https://arxiv.org/abs/2304.08929
---

# SDFReg - Learning Signed Distance Functions for Point Cloud Registration

## Source

- Raw file: `raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf`
- Type: 논문 (arXiv preprint)
- arXiv: 2304.08929, v1 2023-04-18, v2 2024-01-10 (수집한 파일은 v2)
- Authors: Leida Zhang, Zhengda Lu, Kai Liu, Yiqun Wang
- Category: cs.CV
- Venue: 명시되지 않음. Index Terms와 4쪽 본문 + supplementary 구성은 conference 투고 형식이지만 논문 안에 venue 표기가 없다.
- Evidence tier: A (논문 본문 및 supplementary 직접 확인)
- 수집 경위: 사용자가 arXiv HTML 링크를 지정해 PDF를 내려받아 추가. 본문과 표는 PDF에서 직접 추출해 확인했다.

## TL;DR

Point cloud registration에서 target point cloud를 neural SDF로 표현하고, source point를 그 implicit surface에 정렬하는 correspondence-free 방식을 제안한다. SDF 학습과 registration을 번갈아 최적화하는 coarse-to-fine 전략이 핵심 기여이며, noise/partial/density 변화가 있는 imperfect point cloud에서 강건성이 좋다.

자세한 정리는 [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]에 있다.

## Key Content

- Registration 문제를 point-to-point 정렬에서 point-to-implicit-surface 정렬로 치환한다. 대응점 탐색이 사라진다.
- Distance metric이 SDF 값 그 자체이므로, network backpropagation으로 얻은 $\nabla \mathrm{SDF}$와 chain rule로 Jacobian을 만들고 Levenberg-Marquardt로 푼다.
- Coarse-to-fine: 고정된 query point 대신 source point cloud를 query point로 쓰고, registration 1 iteration마다 갱신된 point cloud를 query set에 누적한다.
- Eikonal 항으로 SDF gradient norm을 1로 정규화한다.
- Backbone은 GenSDF (Chou et al. 2022)이며, 미지 category에 대해 SDF를 처음부터 재학습할 필요가 없다는 점을 채택 이유로 든다.
- ModelNet40, 3DMatch, Stanford 3D Scan에서 평가하고 ICP, PointNetLK, DCP-V2, FMR, DeepGMR, IFR과 비교한다.

## Notes / Marginalia Check

없음. PDF annotation을 확인한 결과 highlight, text note, ink annotation이 전혀 없다. 사용자가 방금 내려받은 원본 그대로다.

## Claims To Verify

- Venue와 게재 여부: arXiv에 journal reference가 없다. 이후 어떤 학회/저널에 실렸는지 확인 필요.
- Table 3 (robustness)의 baseline 인용 번호가 어긋나 있다. 본문 표에서 `FMR [12]`, `DeepGMR [11]`로 표기되어 있는데 참고문헌 목록상 [11]은 IFR, [12]는 DeepGMR이다. 표의 행 이름과 인용 번호 중 무엇이 맞는지 원저자 확인 없이는 단정할 수 없다. 수치 자체는 행 이름 기준으로 읽었다.
- 본문 2.3절은 SDF 학습을 self-supervised로, supplementary 1.1절은 semi-supervised로 서술한다. 같은 GenSDF 기반 절차를 다르게 부른 것으로 보이나 논문 안에서 용어가 통일되어 있지 않다.
- 학습 시간, inference 시간, iteration당 비용이 전혀 보고되지 않았다. Registration마다 SDF 최적화를 도는 구조라 실시간 로봇 적용 가능성은 이 논문만으로 판단 불가.

## Promoted To Wiki Pages

- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]
- [[SDFReg Point Cloud Registration]]
- [[Point Cloud Registration]]
- [[Neural Implicit Surface Representation]]
- [[ModelNet40]]
- [[3DMatch]]
- [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]

## Open Questions

- 이 방식은 target 하나마다 SDF를 최적화한다. 로봇의 온라인 perception loop에 넣을 만한 비용인가?
- SDF를 perception(registration)과 contact(collision detection) 양쪽에서 공유할 수 있는가? → [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]로 승격.
- Partial overlap 70% 실험 외에 더 낮은 overlap에서도 성립하는가?
