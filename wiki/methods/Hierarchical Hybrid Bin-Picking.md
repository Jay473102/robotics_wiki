---
type: method
status: active
created: 2026-09-01
updated: 2026-09-01
tags:
  - method
  - bin-picking
  - grasping
  - industrial-automation
  - robot-learning
sources:
  - raw/papers/2608.28175v1.pdf
---

# Hierarchical Hybrid Bin-Picking

## TL;DR

Model-based bin picking 파이프라인을 backbone으로 두고, perception 실패 유형별로 model-free grasp 생성이 개입하는 4층 fallback 구조 + 운영 중 grasp DB를 자동 확장·랭킹하는 online self-learning 절차. 목표는 수동 개입 없는 100% bin clearance와 높은 grasp 성공률의 양립. 출처: [[2026 - Picking Bins Empty Hierarchical Hybrid Bin-Picking]].

## Problem Setting

단일 품종 부품이 무작위로 쌓인 산업용 bin에서, 사전 정의 grasp이 모두 막히는 deadlock, 저신뢰 pose, 미검출 부품이라는 세 실패 지점 때문에 bin이 완전히 비워지지 않는다. 신규 부품마다 grasp 수동 정의·튜닝 비용도 크다.

## Procedure

**계층 실행** (실패 지점의 역순으로 배치):

1. **Level I (model-based)**: detector(oriented bbox + confidence) → 6D pose(depth 정합, fitness score) → grasp DB에서 collision-free·reachable 후보 필터 → 랭킹 최상위 grasp 실행.
2. **Level II (deadlock 해소 + 탐색)**: pose는 고신뢰인데 사전 grasp이 전부 막히면, model-free 생성기(Contact-GraspNet)로 대상 물체 표면(pose 투영 1mm 이내 점들)에서 후보 생성 → $S_{total} = 0.2\,S_{CGN} + 0.6\,S_{AP} + 0.2\,S_{COG}$로 rerank → 실행. pose를 알므로 grasp을 물체 좌표계로 변환해 DB에 추가.
3. **Level III**: pose 신뢰도 미달 시 detection bbox로 자른 point cloud에서 model-free grasping.
4. **Level IV**: 미검출 잔여 점군에 model-free grasping (단일 품종 가정 하에서만).

**Self-learning 루프** (Level I·II grasp마다):

1. 전동 gripper 폐합 후 stroke를 읽어 성공/실패 자동 라벨 → 해당 grasp의 $(n, k)$ 갱신.
2. Wilson score interval($z{=}1.96$) 상한 $p_o$로 전체 DB 랭킹. $p_o$ 동률이면 $t = k{+}2$(사전 정의) / $k$(발견)로 tiebreak. 같은 grasp이 여러 부품에 유효하면 pose fitness가 높은 부품에 실행.
3. $p_o < 75\%$이면 그 grasp 실행 차단 + 유사 grasp($\psi = \sqrt{\|t_\Delta\|^2 + (0.01\,\theta)^2} < 4$mm) 신규 학습 차단.

## Assumptions / Requirements

- 부품 CAD와 6D pose estimator (상용 시스템 수준의 detection·pose 신뢰도가 전제 — 실험에서 이 부분은 이미 강건했다).
- grasp 성공을 자동 판정할 수 있는 gripper 피드백 (여기서는 전동 parallel gripper의 stroke).
- Level IV는 bin에 대상 부품만 있다는 가정.
- 얽힘 복수 파지는 검출하지 못한다 — 얽히기 쉬운 부품에는 [[Tangled-Prone Bin Picking]]류 분리 전략이 별도로 필요하다.

## Inputs / Outputs

- 입력: RGB-D 관측, 부품 CAD, (선택) 수동 초기 grasp DB.
- 출력: 실행 grasp + 성공 통계가 붙은 grasp DB (운영하며 자가 확장).

## Design Rationale

- **UCB·Thompson 대신 Wilson $p_o$ greedy**: 표준 bandit은 모든 옵션의 탐색을 강제해 단기 GSR을 깎는다. 이 절차는 무결점 grasp을 우선하고 deadlock일 때만 새 후보를 탐색한다 (탐색이 "필요에 의해" 트리거되는 구조).
- **DB 확장 억제**: 성공 grasp이 쌓이면 Level II 진입 빈도 자체가 줄어 DB가 과성장하지 않는다 (실험에서 부품당 +10~22개).

## Evidence

- Tier A: 자동차 부품 3종 × 30 bins에서 bin clearance 100%, manual init GSR 83.6~91.9%, 탐색 페널티 ≤2.6%p. 상세 수치는 paper 페이지.

## Related Concepts

- [[Model-Based and Model-Free Grasping]] — 이 방법이 해소하는 이분법.
- [[Generative Grasp Synthesis]] — Level II-IV의 생성기가 이 축의 모델(CGN). 추론: CGN 자리는 교체 가능한 모듈이라 [[GraspMF Few-Step Grasp Generation]] 같은 few-step 모델로 대체 가능하나, 이 시스템의 병목은 latency가 아니라 GSR·grasp depth다.
- [[Object Singulation]] — 인접: deadlock은 얽힘이 아니라 접근 불가에서 온다. 두 실패 축은 서로 다른 대응을 요구한다.

## Open Questions

- 열린 질문: rerank 가중치·차단 문턱의 부품 의존성. 자동 튜닝 없이 HMLV로 확장 가능한가?
- 열린 질문: grasp depth를 예측하는 생성기(또는 CGN fine-tuning)로 Level II-IV GSR을 얼마나 끌어올릴 수 있는가 (저자 future work).
