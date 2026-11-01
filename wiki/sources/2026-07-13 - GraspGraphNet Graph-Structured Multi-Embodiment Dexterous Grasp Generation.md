---
type: source
status: ingested
created: 2026-11-02
updated: 2026-11-02
tags:
  - source
  - grasping
  - flow-matching
  - cross-embodiment
  - manipulation
sources:
  - raw/papers/2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation.pdf
  - https://arxiv.org/abs/2607.11031v1
---

# GraspGraphNet: Graph-Structured Multi-Embodiment Dexterous Grasp Generation

## TL;DR

서로 다른 다지 손을 URDF 기구학 그래프로 표현하고, 동적으로 갱신하는 손–물체 연결과 conditional flow matching으로 palm pose와 관절 상태를 직접 생성한다. 저자는 세 손의 시뮬레이션 평균 성공률 **83.48% / grasp당 40ms**, 손가락 제거 변형에서 재학습 없이 **72.70%**, Leap Hand 데이터로 fine-tuning한 실물 실험에서 **91%**를 보고한다. 세 결과는 평가 조건이 서로 다르다.

## Source

- Raw file: `raw/papers/2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation.pdf`
- Type: 사용자 제공 논문 PDF, arXiv preprint 9쪽.
- Date: 2026-07-13, arXiv:2607.11031v1 [cs.RO] (PDF p.1).
- Authors: Yeonseo Lee, Taeyeop Lee, Hyosup Shin, Guebin Hwang, Sungho Jo (KAIST).
- Evidence tier: **A — 논문 본문**. 아래 수치는 저자 보고 결과이며 독립 재현하지 않았다.
- 논문 식별 URL: https://arxiv.org/abs/2607.11031v1
- PDF p.1에 제시된 프로젝트 URL: https://lysees.github.io/graspgraphnet-page (이 ingest에서 사이트·코드·모델 공개 상태를 별도 확인하지 않음).

## Key Content

- **문제:** 손마다 손가락 수, 기구학 구조, actuated-joint 수가 달라 고정 길이 출력이나 hand-agnostic contact 표현만으로 실행 상태를 생성하기 어렵다 (pp.1–2).
- **표현:** 물체 점군과 URDF의 link–joint 그래프를 사용한다. 상태는 병진 3차원, 회전 6D 표현, 손별 정규화 관절 상태를 합친 $\mathbb{R}^{9+J}$다 (p.3).
- **방법:** differentiable FK → 기구학 MPNN → coarse object cross-attention + fine object dynamic world-edge MPNN → palm·joint velocity 예측을 반복한다. 기본 추론은 Euler 3 step이다 (pp.3–5).
- **시뮬레이션:** CMapDataset의 Barrett·Allegro·Shadow 데이터로 공동 학습. 미관측 물체 40개(CMapDataset 10개 + Google Scanned Objects 30개), 손마다 4,000회 평가. Isaac Gym에서 6방향 perturbation 후 물체 변위 2cm 미만을 성공으로 정의한다 (p.5).
- **Table I, p.6:** 평균 성공률/추론 시간은 GraspGraphNet 83.48%/40ms, TRO-Grasp 81.00%/265ms, DRO-Grasp 77.60%/569ms, GenDexGrasp 29.05%/15,550ms. RTX 4090에서 executable grasp command를 생성하는 시간이며 physics simulation은 제외한다.
- **Table II, pp.6–7:** Allegro 3종·Shadow 4종의 손가락 하나 제거 변형에 재학습 없이 적용하여 평균 72.70%. 임의의 새로운 손 형태에 대한 일반화 실험은 아니다.
- **실물, p.7:** xArm6 + Leap Hand + Azure Kinect. TRO-Grasp의 Leap Hand 학습 데이터로 fine-tuning 후 10개 물체 × 10회, grasp–lift–hold 성공률 91%. Leap Hand zero-shot 결과가 아니다.
- **Ablation, pp.7–8:** direct regression 61.98%, flow matching K=1 78.94%, K=3 83.48%. Cross-attention 제거 54.80%, world-edge MPNN 제거 51.27%, static world edges 50.23%로 낮아진다. K=20은 83.87%/189ms로 K=3보다 0.39pp 높다.

## Notes / Marginalia Check

- PDF annotation 계층 검사: 9쪽에 Link annotation 75개, 비-Link annotation 0개. annotation 형태의 사용자 필기·하이라이트·메모는 없다.
- pp.6–8의 렌더링을 확인하여 주요 결과 표를 텍스트 추출 결과와 대조했다.

## Claims To Verify

- 검증 필요: 공개 코드·checkpoint와 실제 재현 결과. PDF에 있는 프로젝트 URL만으로 공개 상태를 확정하지 않는다.
- 검증 필요: 손가락 제거보다 큰 형태 차이를 가진 새로운 손에 대한 zero-shot 성능. 논문도 이를 향후 연구로 남긴다 (p.8).
- 검증 필요: 센서 처리·로봇 접근·실행까지 포함하는 전체 latency. 보고된 40ms를 물체를 집는 전체 시간으로 해석하지 않는다.
- 손 상태를 직접 출력한다는 설명을 충돌 없는 접근 경로나 모든 관절 명령의 물리적 유효성 보장으로 확장하지 않는다.
- 원문의 성공률 차이 표기인 5.88%, 2.48%, 15.92%는 각각 DRO/TRO 대비 기본 성능 및 DRO 대비 손가락 제거 성능의 **퍼센트포인트(pp)** 차이로 읽는다.

## Promoted To Wiki Pages

- [[2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]] — 논문별 방법·평가·한계 정리.
- [[GraspGraphNet Graph-Structured Grasp Generation]] — 입력부터 실행 가능한 손 상태 생성까지의 절차.
- [[Cross-Embodiment Dexterous Grasping]] — 여러 손의 구조·출력 공간을 다루는 문제 영역.
- [[Flow Matching]] — 조건부 속도장 학습의 구체적인 grasp 적용 사례.
- [[Generative Grasp Synthesis]] — 기존 grasp 생성 지식과 다지 손 생성의 연결.
- [[GraspMF Few-Step Grasp Generation]] — few-step 생성이라는 공통점과 표현·평가 조건의 차이를 비교할 관련 방법.

## Open Questions

- 열린 질문: 학습한 손의 finger-removal을 넘어, 관절 배치·손바닥·link 형상이 크게 다른 손에서도 zero-shot 생성이 가능한가?
- 열린 질문: 생성된 최종 grasp와 충돌 없는 접근 궤적을 결합하면 전체 시스템 성공률과 latency는 어떻게 달라지는가?
- 열린 질문: 같은 데이터·하드웨어·grasp 수로 비교할 때, 그래프 기반 conditional flow matching과 다른 few-step 생성 방법의 품질·속도 차이는 무엇인가?
