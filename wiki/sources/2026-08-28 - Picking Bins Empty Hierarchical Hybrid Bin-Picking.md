---
type: source
status: ingested
created: 2026-09-01
updated: 2026-09-01
tags:
  - source
  - bin-picking
  - grasping
  - industrial-automation
sources:
  - raw/papers/2608.28175v1.pdf
---

# Picking Bins Empty - Hierarchical Hybrid Bin-Picking (arXiv 2608.28175)

## Source

- Raw file: `raw/papers/2608.28175v1.pdf` (사용자가 직접 업로드, 환경 네트워크 정책이 arxiv.org를 차단해 직접 다운로드 불가)
- Type: 논문 (arXiv preprint 2608.28175v1, 2026-08-28, cs.RO)
- Date: 2026-08-28 (v1)
- Evidence tier: A

## TL;DR

Mercedes-Benz·KIT·DLR·Fraunhofer IAO 공동의 산업용 bin picking 논문. model-based 파이프라인(CAD 기반 6D pose + 수동 grasp DB)을 backbone으로 두고, deadlock·저신뢰 pose·미검출이라는 세 가지 perception 실패 지점을 Contact-GraspNet 기반 model-free fallback 3개 층으로 막는 4층 계층 구조를 제안한다. gripper stroke를 자동 라벨로 쓰는 Wilson score 기반 online self-learning으로 grasp DB를 운영 중에 확장·랭킹한다. 자동차 부품 3종 실기에서 bin clearance를 50.9% → 100%로 올렸다.

## Key Content

- 4층 계층: Level I model-based(상용 Roboception CADMatch 계열 backbone), II deadlock 해소 + grasp 탐색, III 저신뢰 pose에서 model-free, IV 미검출 잔여 물체 grasping.
- CGN(GraspClutter6D 학습)을 fallback 생성기로 사용, antipodal·무게중심 점수로 rerank.
- Wilson score 상한 $p_o$ 랭킹, $p_o < 75\%$ 차단, pose 유사도 기반 유사 grasp 학습 차단.
- 실험: Fanuc CRX-25iA + Zivid 2+ + Schunk EGK-40, 부품 3종 × bin당 50개.

자세한 내용은 [[2026 - Picking Bins Empty Hierarchical Hybrid Bin-Picking]]과 [[Hierarchical Hybrid Bin-Picking]] 참조.

## Notes / Marginalia Check

pypdf로 annotation을 확인했다. 하이퍼링크 외 사용자 필기·하이라이트 없음.

## Claims To Verify

- 게재 venue 미표기 (IEEE copyright 문구와 IEEE 학회 양식만 존재, ICRA/IROS/CASE류 투고 추정 — 추론).
- Level I backbone이 Roboception CADMatch 상용 시스템인지: 인용 [30]이 해당 제품 페이지이나 본문은 "commercial bin-picking system [30]"으로만 언급.
- 코드·데이터 공개 여부 본문 미언급.
