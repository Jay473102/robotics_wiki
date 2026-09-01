---
type: paper
status: active
created: 2026-09-01
updated: 2026-09-01
tags:
  - bin-picking
  - grasping
  - manipulation
  - industrial-automation
  - robot-learning
sources:
  - raw/papers/2608.28175v1.pdf
  - https://arxiv.org/abs/2608.28175
title: "Picking Bins Empty: A Hierarchical Hybrid Approach with Online Self-Learning of Grasp Points for Reliable Industrial Bin-Picking"
authors: Florian Töper, Samarth Kishor Yelvande, Jan Niklas Ewertz, Rudolph Triebel, Peter Ohlhausen
year: 2026
venue: arXiv preprint (2608.28175, v1 2026-08-28, cs.RO). IEEE copyright 문구가 있으나 venue 미표기
doi:
url: https://arxiv.org/abs/2608.28175
---

# Picking Bins Empty - Hierarchical Hybrid Industrial Bin-Picking

## TL;DR

산업용 bin picking에서 model-based 방식(CAD 기반 6D pose + 사전 정의 grasp)은 정밀하지만 deadlock으로 bin을 비우지 못하고, model-free 방식은 bin은 비우지만 grasp 성공률(GSR)이 낮다. 이 논문(Mercedes-Benz AG, Univ. Stuttgart, KIT, DLR, Fraunhofer IAO)은 둘을 **4층 계층 구조**로 결합한다: model-based backbone이 기본 동작하고, perception 실패 유형별로 Contact-GraspNet 기반 model-free fallback이 개입하며, Level II에서 발견한 grasp을 **gripper stroke 자동 라벨 + Wilson score interval 랭킹**으로 DB에 축적한다. 자동차 부품 3종 실기에서 bin clearance 50.9% → **100%** (30 bins 전부), manual init 시 GSR 83.6~91.9%를 달성했다.

## Problem

Model-based 파이프라인의 세 가지 perception 실패 지점이 bin 완전 배출을 막는다:

1. Object detection false negative → 미검출 부품이 bin에 남는다.
2. 부정확한 pose 추정 → grasp 오차로 전파된다.
3. **Deadlock**: 검출된 모든 부품의 사전 정의 grasp이 collision-free·reachable하지 않다. 실험에서 확인된 주 병목이며, 특히 bin 벽·모서리 부근에서 발생한다.

추가로 신규 부품마다 grasp point를 수동 정의·튜닝하는 commissioning 비용(실험 기준 부품당 30~45분 + 반복 조정)이 High-Mix Low-Volume 제조 적용을 막는다. 반대로 model-free(학습 기반) grasp 생성은 GSR이 낮고(GraspGen도 단순 tabletop 83.3%, CGN은 GraspClutter6D 학습 후 복잡 장면 67.9%), 결정성이 낮아 oriented placing과 얽힘 검출이 안 된다.

## Method

### 4층 계층 (Fig. 1)

| Level | 트리거 | 동작 |
|---|---|---|
| I | 정상 | 상용 backbone [30]: synthetic data + domain randomization으로 학습한 detector(oriented bbox) → depth 정합 6D pose(fitness score) → grasp DB collision check → 최상위 grasp 실행 |
| II | pose 고신뢰인데 collision-free 사전 grasp 없음 (deadlock) | CGN "exploration agent"가 새 grasp 후보 생성·채점·실행. pose를 알므로 성공한 grasp을 물체 좌표계로 DB에 추가 |
| III | 검출됐지만 pose 신뢰도 미달 | bbox로 point cloud를 잘라 model-free grasping |
| IV | 미검출 잔여 부품 | bin 내부 잔여 3D point에 model-free grasping (단일 품종 bulk 가정; 이물질 가능 시 생략) |

### Model-free fallback 상세

- CGN(GraspClutter6D 학습)에 target 2,048점 + 주변 context 20,000점 입력. 대칭 jaw라 각 grasp의 z축 180° 뒤집기 복제 추가.
- Level II에서는 CGN 점수를 기하 기준으로 rerank: $S_{total} = \alpha S_{CGN} + \beta S_{AP} + \gamma S_{COG}$, 경험적으로 $\alpha{=}0.2, \beta{=}0.6, \gamma{=}0.2$. $S_{AP}$는 friction cone(soft pad라 $\mu{=}0.9$) 기준 antipodal 정도, $S_{COG}$는 무게중심 offset.

### Online self-learning (Wilson score 랭킹)

- 전동 gripper의 폐합 후 stroke(폭)를 읽어 성공/실패를 자동 라벨링. grasp point별 $(n, k)$ 갱신.
- Wilson score interval($z{=}1.96$, 95%)의 **상한 $p_o$로 랭킹** — "optimism in the face of uncertainty". 미시도 grasp과 무결점 grasp이 $p_o{=}1$로 동률이 되면 tiebreaker $t = k{+}2$(사전 정의) / $k$(발견)로 검증 횟수 많은 쪽을 greedy 선택.
- UCB·Thompson sampling을 **의도적으로 배제**: 모든 옵션의 강제 탐색이 단기 GSR을 깎기 때문. 무결점 grasp 우선, 없을 때만 미시도 후보 탐색.
- $p_o < 75\%$ (초기 2연속 실패 상당)이면 해당 grasp 실행 차단 + 유사 grasp 학습 차단. 유사도 $\psi = \sqrt{\|t_\Delta\|^2 + (\lambda\theta)^2}$, $\lambda{=}0.01$ m/rad, 문턱 4mm (≈ 병진 4mm 또는 회전 23°).

## Data / Embodiment

Fanuc CRX-25iA cobot + Zivid 2+ LR110 RGB-D + Schunk EGK-40 parallel gripper(soft finger pad), TCP는 gripper 끝에서 5mm 안쪽 고정. 자동차 부품 3종(A/B/C), VDA-R-KLT 4315 용기에 부품 50개씩. baseline은 부품당 3 bins, hybrid는 부품당 5 bins × (Empty Init / Manual Init) 두 전략.

## Results

### Baseline의 trade-off가 실험으로 정량화됨 (Table I, II)

| | Bin clearance | GSR |
|---|---|---|
| Model-based | 평균 **50.9%** (A 33.3 / B 34.7 / C 84.7) | **99.1%** |
| Model-free (CGN) | **100%** | **45.6%** (A 71.4 / B 29.8 / C 55.0) |

- Deadlock의 주 원인은 detection·pose가 아니라 **collision-free 사전 grasp의 부재**였다 (bin 벽 부근 A·C, 복잡 기하 B는 중앙에서도).
- CGN의 GSR 붕괴 원인 중 하나: 곡률이 큰 부위마다 필요한 grasp depth가 다른데 CGN 구조는 depth를 예측하지 않는다 (TCP 5mm 고정).

### Hybrid (Table 없음, Fig. 6-7 + 본문)

- **30 bins 전부 100% bin clearance** 유지. Manual init 15 bins에서 deadlock 해소 22회: Level II 18회, III 1회, IV 3회. 실패한 grasp조차 부품 재배치로 deadlock을 푼 사례 존재.
- Manual init GSR 평균: A 91.9% / B 83.6% / C 89.3%. 학습 grasp 탐색으로 인한 GSR 페널티 $\Delta GSR$은 2.6 / 1.2 / 0.0%p에 불과.
- Empty init: model-free baseline 대비 유의한 개선(예: A 63.3→83.3%, C 58.8→89.3% 추세)이나 부품 B는 CGN depth 문제가 그대로 남음.
- 오버헤드: Level II-IV 진입 시 grasp 생성 1.01s + 4,096 후보 collision check 1.36s. DB는 실험 전체에서 부품당 22/10/12개만 증가 → Level I cycle time 영향 무시 가능 (check당 ~0.3ms).

## Limitations

- 얽힌 부품 복수 파지를 자동 검출하지 못한다 (부품 A에서 드물게 발생, 수동 복구). [[Tangled-Prone Bin Picking]]이 다루는 축이 이 시스템에는 없다.
- 부품 3종, 단일 gripper, 단기 실험. 저자 스스로 장기 거동·파라미터 ablation을 future work로 명시.
- 랭킹·차단 문턱($p_o$ 75%, $\psi$ 4mm, rerank 가중치)이 모두 heuristic.
- 상용 backbone 의존으로 Level I 재현이 제한적. 코드 공개 언급 없음.
- GSR 비교의 공정성 주의: model-based baseline은 가장 어려운 잔여 배치에서 (grasp 시도 없이) 정지하므로 GSR이 유리하게 측정된다 — 본문이 직접 인정.

## Connections

- [[Hierarchical Hybrid Bin-Picking]] — implemented-by: 방법 절차 페이지.
- [[Model-Based and Model-Free Grasping]] — 이 논문이 정면으로 다루는 이분법과 hybrid 해소.
- [[Generative Grasp Synthesis]] — uses: CGN(contact-point 생성 모델)을 fallback으로 사용. GraspGen(diffusion)을 "우수하나 계산 비용이 크고 표면 비접촉 grasp을 낼 수 있다"고 평가 — 생성 grasp 축의 산업 배치 관점 근거.
- [[2026-09-01 - Grasp Generation and Object Singulation]] — answers(부분): 생성형 grasp 모델이 산업 bin picking 파이프라인 안에서 어디에 놓이는가에 대한 첫 Tier A 실증 — "주 경로가 아니라 deadlock 해소용 탐색 에이전트".
- [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]] — 상보적: 그쪽은 얽힘(부품 간 결합)이 병목, 이쪽은 deadlock(사전 grasp 부재)이 병목. 이 논문은 얽힘 검출을 명시적 한계로 남긴다.
- [[Action Affordance Learning]] — 대비: pixel affordance 대신 pose 조건부 grasp DB + 후보 채점으로 action을 고른다.
- 추론: Wilson score 랭킹은 Dex-Net 1.0의 multi-armed bandit(correlated rewards)과 같은 계열이나, 탐색을 강제하지 않는 보수적 변형이다.

## Contradictions / Updates

- 위키 기존 서술과 충돌 없음. [[Generative Grasp Synthesis]]의 "생성 모델 품질·속도 경쟁" 프레임에 "산업 현장에서는 GSR 신뢰성과 상용 시스템 통합이 우선"이라는 보완 관점을 추가한다 (해당 페이지에 기록).

## Notes / Marginalia

PDF에 사용자 annotation 없음 (하이퍼링크만 존재).

## Open Questions

- 열린 질문: few-step 생성 모델([[GraspMF Few-Step Grasp Generation]])을 CGN 자리에 넣으면 무엇이 달라지는가? 이 시스템의 병목은 latency(1.01s 생성은 이미 허용됨)가 아니라 GSR과 grasp depth 예측이다 — GraspMF의 속도 우위가 여기서는 가치가 낮고, 분포 커버리지·depth 처리가 관건이라는 추론.
- 열린 질문: Wilson score 랭킹의 "탐색 강제 배제"는 부품 교체 주기가 짧은 HMLV에서 local optimum에 갇히지 않는가?
- 열린 질문: Level IV의 단일 품종 가정이 깨지는 혼합 bin에서 계층 구조는 어떻게 확장되는가?
