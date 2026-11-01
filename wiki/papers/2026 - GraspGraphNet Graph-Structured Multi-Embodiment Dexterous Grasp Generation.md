---
type: paper
status: active
created: 2026-11-02
updated: 2026-11-02
tags:
  - paper
  - grasping
  - flow-matching
  - generative-models
  - cross-embodiment
  - manipulation
sources:
  - raw/papers/2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation.pdf
  - https://arxiv.org/abs/2607.11031v1
title: "GraspGraphNet: Graph-Structured Multi-Embodiment Dexterous Grasp Generation"
authors:
  - Yeonseo Lee
  - Taeyeop Lee
  - Hyosup Shin
  - Guebin Hwang
  - Sungho Jo
year: 2026
venue: arXiv preprint (2607.11031v1, 2026-07-13)
doi:
url: https://arxiv.org/abs/2607.11031v1
---

# GraspGraphNet: Graph-Structured Multi-Embodiment Dexterous Grasp Generation

## TL;DR

GraspGraphNet은 손의 URDF 기구학 그래프와 물체 점군을 조건으로, **palm pose와 손별 관절 상태를 직접 생성**하는 conditional flow matching 모델이다. 기본 Euler 3 step에서 Barrett·Allegro·Shadow의 시뮬레이션 평균 성공률 **83.48%**, grasp당 계산 시간 **40ms**를 보고한다. 손가락 제거 변형의 zero-shot 결과는 **72.70%**이며, 실물 Leap Hand의 **91%는 fine-tuning 후 결과**다. 모든 수치는 논문 본문(Tier A)의 저자 보고값이며 독립 재현하지 않았다.

## Problem

손마다 손가락 수, link 형상, 관절 연결과 구동 차원 $J$가 다르다. Contact map이나 robot–object interaction 같은 중간 표현을 먼저 예측하면 여러 손에 공유하기 쉽지만, 이를 실행 가능한 손 pose·관절 명령으로 바꾸는 최적화·IK·retargeting이 추가로 필요할 수 있다. 이 논문은 손의 구조를 보존하면서 native grasp state를 생성하는 방법을 제안한다 (pp.1–2).

## Core Idea

URDF의 physical link를 노드, joint를 parent-to-child edge로 표현하여 손마다 다른 그래프 크기와 관절 수를 수용한다. 생성 중 손 상태가 바뀔 때마다 FK로 link pose를 계산하고, 가까운 물체 표면과의 **world edges를 다시 구성**한다. 이렇게 갱신한 상호작용 특징으로 조건부 속도장을 예측한다 (pp.3–4).

## Method

- **상태:** $x=[t_{\mathrm{palm}},R_{\mathrm{palm}}^{6D},q_{\mathrm{norm}}]\in\mathbb{R}^{9+J}$. 손 사이에서 일관된 canonical palm frame을 사용하고 관절은 URDF limit으로 정규화한다 (p.3).
- **물체:** 위치·법선·곡률을 포함하는 점군 1,024개에서 256/64/32개 계층을 구성한다. 64-point 특징은 fine interaction, 32-point 특징은 coarse context에 사용한다 (p.3).
- **손:** link당 mesh point 64개를 shared PointNet으로 인코딩한다. 현재 FK position·6D orientation, tree depth, fingertip 표시, 관절 상태를 합쳐 3-layer kinematic MPNN에 넣는다 (pp.4–5).
- **융합:** coarse object cross-attention과 fine object world-edge MPNN을 결합한다. 각 link에 가까운 물체 점 $k=8$개를 연결하며, world-edge message passing은 2 layer다 (pp.4–5).
- **학습:** open-hand 초기 상태 $x_0$와 정답 grasp $x_1$ 사이의 선형 경로 $x_t=(1-t)x_0+tx_1$에서 목표 속도 $v^*=x_1-x_0$를 회귀한다. Palm·joint MSE를 더하며 $\lambda_q=1$이다. 학습 초기 접근 방향은 정답 방향 중심 30° cone에서, 추론 시에는 구면 전체에서 샘플링한다 (pp.4–5).
- **추론:** $x^{(k+1)}=x^{(k)}+\frac{1}{K}v_\theta(x^{(k)},k/K)$, 기본 $K=3$. 최종 canonical palm orientation을 robot-native frame으로 바꾸고 고정 palm-to-wrist offset 및 관절 역정규화를 적용한다 (p.5).
- **구현:** 약 1.58M parameters, hidden dim 128, AdamW 초기 학습률 $3\times10^{-4}$, cosine decay, 200 epochs, NVIDIA RTX 4090 한 장 (p.5).

## Data / Embodiment

- 학습: filtered CMapDataset의 Barrett Hand, Allegro Hand, Shadow Hand 데이터를 공동 사용한다. 비교 방법도 같은 세 손의 training split을 사용했다고 명시한다 (p.5).
- 시뮬레이션: CMapDataset held-out 물체 10개 + Google Scanned Objects 30개, 총 미관측 물체 40개 (pp.5–6).
- Topology 변형: Allegro 3종, Shadow 4종의 **손가락 하나 제거** 모델. 기본 평가와 같은 학습 모델을 재학습·adaptation 없이 사용한다 (p.6).
- 실물: xArm6 + Leap Hand + Azure Kinect의 partial point cloud 입력. TRO-Grasp이 제공한 Leap Hand 학습 데이터로 **fine-tuning**한다 (p.7).

## Evaluation

- 시뮬레이션은 Isaac Gym에서 물체당 100회, **손당 4,000회** 생성한다. 6방향 perturbation하에서 물체 변위가 2cm 미만이면 성공이다 (p.5).
- 추론 시간은 같은 하드웨어에서 **실행 가능한 grasp command 하나를 생성하는 계산 시간**이다. Physics simulation을 제외하므로 perception–planning–execution 전체 latency가 아니다 (p.5).
- 실물은 10개 물체 × 10회 = 100회. 물체를 잡고 테이블에서 들어 올린 뒤 떨어뜨리지 않고 유지하면 성공이다 (p.7).

## Results

### 기본 세 손 비교 (Table I, p.6)

| 방법 | Barrett SR | Allegro SR | Shadow SR | 평균 SR | 평균 추론 시간 |
|---|---:|---:|---:|---:|---:|
| GenDexGrasp | 38.57% | 19.72% | 28.87% | 29.05% | 15,550ms |
| DRO-Grasp | 85.65% | 81.07% | 66.07% | 77.60% | 569ms |
| TRO-Grasp | 82.12% | 86.57% | 74.30% | 81.00% | 265ms |
| GraspGraphNet | **86.05%** | **87.75%** | **76.65%** | **83.48%** | **40ms** |

GraspGraphNet의 손별 성공 횟수는 3,442/4,000, 3,510/4,000, 3,066/4,000이며 추론 시간은 각각 24/33/63ms다. 평균 성공률 차이는 DRO 대비 **+5.88pp**, TRO 대비 **+2.48pp**. 표의 소수 자릿수는 원문 보고값을 유지했다.

### 손가락 제거 변형 (Table II, p.7)

| 방법 | 7개 변형 전체 평균 SR |
|---|---:|
| GenDexGrasp | 12.99% |
| DRO-Grasp | 56.78% |
| TRO-Grasp | 15.29% |
| GraspGraphNet | **72.70%** |

GraspGraphNet은 Allegro w/o F1/F2/F3에서 **87.40/84.07/57.45%**, Shadow w/o F1/F2/F3/F4에서 **73.72/75.12/75.80/55.35%**다. 7종 중 5종에서 최고이며, Allegro w/o F3와 Shadow w/o F4에서는 DRO가 높다. 이 실험은 학습한 손의 제한된 구조 변형에 대한 일반화를 평가한다 (p.6).

### 실물과 구성 요소 검증 (p.7, Tables III–V)

- 실물 Leap Hand: **91/100회 성공(91%)**, Leap 데이터 fine-tuning 후 결과.
- Table III: direct regression **61.98%**, flow matching K=1 **78.94%**, K=3 **83.48%**.
- Table IV: cross-attention 제거 **54.80%**, world-edge MPNN 제거 **51.27%**, 전체 모델 **83.48%**.
- Table V: 초기 open-hand 상태에서 한 번만 구성한 static world edges **50.23%**, 매 step 갱신하는 dynamic world edges **83.48%**.

### 적분 step 수 (Table VI, p.8)

| K | 평균 SR | 추론 시간 |
|---:|---:|---:|
| 1 | 78.94% | 9ms |
| 2 | 82.40% | 19ms |
| 3 | 83.48% | 40ms |
| 5 | 83.36% | 47ms |
| 10 | 83.67% | 95ms |
| 20 | 83.87% | 189ms |

K=3에서 K=20으로 늘리면 +0.39pp에 그치지만 시간은 40→189ms다. 저자는 품질과 시간의 절충으로 K=3을 선택했다.

## Limitations

- 논문은 finger-removal을 넘어 **형태가 크게 다른 손의 zero-shot 일반화**를 향후 연구로 남긴다 (p.8). 실물 Leap 결과도 fine-tuning을 포함한다.
- 40ms는 시뮬레이터 시간을 제외한 grasp command 생성 값이다. 실제 로봇이 물체를 들어 올리는 시간이나 closed-loop 제어 성능은 이 수치로 입증되지 않는다.
- 논문 본문 확인 범위에서 실물 비교 baseline, 반복 학습의 분산·신뢰구간, 물체별 실물 성공률은 제시되지 않는다. 100회 결과를 임의의 물체·환경에 대한 성공률로 확대하지 않는다.
- 추론: 직접 출력한 grasp state만으로 충돌 없는 접근 궤적, robot-arm reachability, 모든 출력의 물리적 유효성이 보장되지는 않는다. 논문의 성공률은 이러한 보장을 대신하는 수학적 증명이 아니다.
- 검증 필요: 코드·checkpoint 공개 상태와 독립 재현. PDF p.1의 프로젝트 URL은 이 ingest에서 별도 검증하지 않았다.

## Connections

- [[2026-07-13 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]] — 원자료·annotation 확인·검증 항목을 기록한 source note.
- [[GraspGraphNet Graph-Structured Grasp Generation]] — 이 논문의 생성 절차를 재사용 가능한 방법으로 정리.
- [[Cross-Embodiment Dexterous Grasping]] — 손의 기구학·출력 차이를 공유 모델로 다루는 문제 영역.
- [[Flow Matching]] — instantaneous velocity를 학습하는 conditional flow matching의 응용.
- [[Generative Grasp Synthesis]] — 물체 조건부 grasp 분포 생성에 다지 손의 관절 상태를 포함하는 사례.
- [[GraspMF Few-Step Grasp Generation]] — few-step grasp 생성이라는 비교 축. 추론: GraspMF의 Lie-group MeanFlow·parallel-jaw 설정과 본 논문의 6D 회전 표현·가변 관절 상태는 구분해야 한다. 데이터·성공 기준·하드웨어·grasp batch가 달라 latency나 성공률을 직접 순위화하지 않는다.

## Contradictions / Updates

- 2026-11-02: 제공된 v1 PDF를 바탕으로 처음 정리했다. 기존 grasp 페이지를 대체하지 않고 cross-embodiment dexterous grasp 생성 사례로 연결한다.
- 논문 본문의 성공률 개선 표기는 상대 증가율이 아니라 퍼센트포인트 차이로 명확히 적었다.

## Notes / Marginalia

9쪽의 PDF annotation 계층에서 Link 75개, 비-Link 0개를 확인했다. Annotation 형태의 사용자 필기·하이라이트·메모는 없다. 주요 결과 표가 있는 pp.6–8은 렌더링으로도 확인했다.

## Open Questions

- 열린 질문: 손가락 수뿐 아니라 link 길이·관절축·손바닥 구조가 다른 미학습 손에서도 성능을 유지하는가?
- 열린 질문: real-world partial observation과 occlusion 변화에 대한 성능을 손별 fine-tuning 없이 유지할 수 있는가?
- 열린 질문: grasp 생성과 arm 접근 궤적의 실행 가능성을 함께 고려할 때 최종 성공률·처리 시간은 어떻게 달라지는가?
- 열린 질문: 동일한 benchmark와 계산 조건에서 다른 few-step 모델과 비교하면 구조 표현과 생성 objective의 기여를 각각 분리할 수 있는가?
