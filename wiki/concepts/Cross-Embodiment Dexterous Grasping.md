---
type: concept
status: draft
created: 2026-11-02
updated: 2026-11-02
tags:
  - grasping
  - manipulation
  - cross-embodiment
  - generative-models
sources:
  - raw/papers/2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation.pdf
---

# Cross-Embodiment Dexterous Grasping

## Definition

손가락 수, link-joint topology, 관절 차원, 구동 범위가 다른 다관절 로봇 손들에서 grasp 지식을 공유하거나 전이하는 문제다. 물체를 잡는 palm pose에 더해 각 손의 관절 구성을 다뤄야 하므로, 고정된 $SE(3)$ pose 생성만으로 전체 문제를 나타낼 수 없다. 근거: [[2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]], pp. 1–3, Sec. I–III-A (Tier A).

## Why It Matters

물체 위의 유용한 접촉 위치를 공유하더라도 각 손의 구조에 따라 해당 접촉을 실현할 수 있는 자세는 다르다. 전이 가능한 표현을 학습하는 것과 실제 손에 실행 가능한 명령을 얻는 것은 함께 평가해야 할 두 요구다. GraspGraphNet은 이를 hand-agnostic 중간 표현의 복원 비용과 graph-conditioned 직접 출력의 대비로 설명한다. 근거: pp. 1–2, Sec. I–II.

## Key Ideas

### 표현의 전이성과 실행 명령

GraspGraphNet의 related work가 구분하는 접근은 다음과 같다. 개별 선행 방법의 설명은 해당 논문의 문헌 정리에 근거하며, 이 페이지에서 선행 원문까지 독립 확인한 것은 아니다.

| 표현 | 전이 아이디어 | 실행 시 확인할 부분 |
|---|---|---|
| Contact points/maps·표면 correspondence | 물체와 손 사이의 접촉 단서를 공유한다 | 실제 palm pose·관절값을 얻는 IK, fitting, optimization 또는 hand-specific 단계 |
| Robot-object 거리·상대 변환 | 손과 물체의 관계를 중간 표현으로 예측한다 | 관계 표현을 executable hand state로 복원하는 과정 |
| Graph-conditioned palm pose + joint state | 손의 topology와 가변 관절 차원을 입력·출력에 직접 반영한다 | 공유 모델이 새로운 구조에서도 유효한 grasp를 생성하는지 검증 |

근거: pp. 1–2, Sec. I–II. GraspGraphNet은 세 번째 접근으로 URDF graph, shared per-joint head, 현재 FK 상태에 따라 바뀌는 robot-object world edges를 결합한다. 근거: pp. 3–5, Sec. III.

### 일반화 평가를 구분하는 세 단계

아래 구분은 논문의 서로 다른 실험과 미검증 범위를 정리한 것이다. “여러 손을 지원한다”는 표현만으로 세 단계가 모두 달성됐다고 보지 않는다.

| 평가 범위 | GraspGraphNet에서 확인한 설정 | 해석의 한계 |
|---|---|---|
| **학습된 여러 손 + 새로운 물체** | Barrett·Allegro·Shadow 공동 학습, 40개 unseen objects에서 평균 83.48% | 미지 물체 성능이며 미지 손 성능은 아님 |
| **학습된 손의 topology 변형** | Allegro 3종·Shadow 4종 손가락 제거 변형, 재학습 없이 평균 72.70% | 통제된 구조 변경에 대한 결과이며 임의의 새 손을 대표하지 않음 |
| **다른 morphology의 손으로 전이** | Leap Hand는 해당 손 데이터로 fine-tune한 뒤 실기 91/100 성공 | Leap 결과는 zero-shot이 아님. 크게 다른 morphology의 zero-shot은 향후 과제 |

근거: pp. 5–7, Sec. IV-A–D, Tables I–II; p. 8, Sec. V. 특히 손가락 제거 결과와 Leap fine-tuning 결과를 합쳐 “아무 손에나 재학습 없이 적용”한다고 서술하면 안 된다.

### 생성 모델과 기하 표현은 별개의 설계 축

- GraspGraphNet은 canonical palm 회전의 6D 표현과 정규화 관절값을 포함한 $\mathbb R^{9+J}$ 상태에서 선형 conditional flow matching을 학습한다. Graph 구조는 손과 물체 조건을 전달하는 역할이다. 근거: pp. 3–5, Sec. III-A, III-E.
- [[GraspMF Few-Step Grasp Generation]]은 기존 위키에서 $SO(3)\times\mathbb R^3$의 parallel-jaw grasp pose에 MeanFlow를 적용한 방법으로 정리되어 있다. GraspGraphNet을 MeanFlow의 후속·파생 구현으로 분류할 근거는 없다.
- 추론: few-step이라는 공통점만으로 생성 목적 함수, 출력 차원, 데이터셋 또는 일반화 능력이 같다고 볼 수 없다. GraspGraphNet의 40 ms/1 grasp/RTX4090과 GraspMF의 15.5 ms/100-grasp batch/RTX5080은 직접 속도 비교에 사용할 수 없다.

### 실행 가능 출력과 성공 판정

GraspGraphNet의 “direct executable”은 별도 grasp 복원용 optimization·hand IK·retargeting 없이 palm/joint 출력을 robot-native frame과 명령 단위로 변환한다는 뜻이다. 시뮬레이션의 6방향 perturbation 평가, 실기의 lift-and-hold 성공, 팔의 접근 경로 안전성은 구분해야 한다. 근거: p. 5, Sec. III-F, IV-A; p. 7, Sec. IV-D. 추론: 명령 형식을 직접 출력하는 것만으로 모든 물리·운동학 제약이 보장되는 것은 아니다.

## Related Papers

- [[2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]] — graph-conditioned 직접 palm/joint 생성, 다중 손·손가락 제거·fine-tuned 실기 평가의 근거.
- [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]] — parallel-jaw grasp pose 생성이라는 인접 문제. 동일 benchmark나 embodiment의 정면 비교 자료는 아니다.
- [[2026-07-13 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]] — 원자료 metadata와 필기 확인 기록.

## Related Concepts

- [[Generative Grasp Synthesis]] — 상위 문제 영역. 본 개념에서는 손의 관절 구성과 embodiment 전이를 추가로 다룬다.
- [[Flow Matching]] — uses: GraspGraphNet의 생성 목적 함수. Cross-embodiment grasping 자체가 flow matching에 한정되는 것은 아니다.
- [[GraspGraphNet Graph-Structured Grasp Generation]] — implemented-by: URDF/FK와 동적 robot-object message passing을 이용하는 구체적 방법.
- [[GraspMF Few-Step Grasp Generation]] — 표현 공간·생성 목적·평가 범위를 구분할 비교 사례.

## Contradictions / Updates

- 2026-11-02: GraspGraphNet v1을 바탕으로 생성. 기존 위키의 parallel-jaw 중심 grasp 설명에 다관절 손과 topology 전이 관점을 추가한다. 서로 다른 실험의 성공률·지연을 같은 척도의 순위로 해석하지 않는다.

## Open Questions

- 손가락 삭제를 넘어 link 길이·joint axis·actuation coupling까지 달라졌을 때 어떤 표현이 전이를 유지하는가?
- 신규 손에 대한 zero-shot, 소량 fine-tuning, 손별 재학습을 같은 데이터·물체·실행 조건에서 어떻게 비교할 것인가?
- Contact 기반 중간 표현과 직접 joint-state 생성 중 어떤 접근이 데이터 부족·접촉 제약 변화에 더 강한가? 위키에 아직 통제된 정면 비교 자료가 충분하지 않다.
- 생성 grasp의 수치상 타당성과 실기 실행 성공을 함께 검증하는 표준 평가를 어떻게 구성할 것인가?
