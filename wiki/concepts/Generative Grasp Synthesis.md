---
type: concept
status: draft
created: 2026-09-01
updated: 2026-11-02
tags:
  - grasping
  - manipulation
  - generative-models
sources:
  - raw/papers/2608.26076v1.pdf
  - raw/papers/2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation.pdf
---

# Generative Grasp Synthesis

## Definition

물체 관측(주로 point cloud)을 조건으로 안정 grasp pose의 **분포**를 생성 모델로 학습하고 샘플링하는 접근. 한 물체의 유효 grasp 집합은 $SE(3)$ 위의 multimodal 분포이므로, point estimate 회귀나 후보 채점(discriminative) 대신 분포 자체를 학습하면 여러 mode를 커버하고 collision avoidance·reachability 같은 downstream 목적과 합성할 수 있다.

## Why It Matters

범위 보강 (2026-11-02): 위의 $SE(3)$ 설명은 주로 parallel-jaw gripper의 pose 생성에 해당한다. [[Cross-Embodiment Dexterous Grasping]]에서는 palm pose와 손별 관절 구성까지 생성해야 한다. GraspGraphNet은 이를 연속 6D 회전 표현을 포함한 $9+J$차원 상태로 표현한다 (논문 §III-A, p.3).

Grasp은 조작의 진입점이고, 분포 커버리지는 cluttered·제약 환경에서 실행 가능한 grasp을 찾을 확률을 결정한다. 생성 모델의 품질(성공률·커버리지)과 샘플링 속도(closed-loop 가능 여부)가 이 축의 두 경쟁 지표다.

## Key Ideas

계보 (모두 Tier A, GraspMF related work 기준):

- **CVAE**: 6-DOF GraspNet (Mousavian et al. 2019) — 생성 접근의 시초.
- **Diffusion / score 기반**: SE(3)-DiffusionFields (Urain et al. 2023, grasp energy field + Langevin), GraspLDM (latent diffusion), Carvalho et al. ($SO(3) \times \mathbb{R}^3$ DDPM), VSIGD (shape inference 결합, 부분 관측 강건성).
- **Flow 기반**: EquiGraspFlow ($SE(3)$-equivariant flow matching), BRIDGER (informative prior로 스텝 절감).
- **Few-step**: [[GraspMF Few-Step Grasp Generation]] — MeanFlow로 ≤5 NFE에서 diffusion/flow 품질 유지. 기존 방법은 low budget에서 SR이 붕괴한다 (SE3Dif T=1에서 6.65%).
- **기하 결합**: 암묵적 표현의 기하 특징으로 grasp 생성을 grounding하는 흐름 (VSIGD, Implicit Grasp Diffusion, GraspMF의 보조 SDF regression) — [[Neural Implicit Surface Representation]]과 교차.

[[ACRONYM]] + Isaac Gym 실행 성공률 + EMD 커버리지는 위 GraspMF 및 관련 parallel-jaw 생성 연구의 평가 맥락이다. 다관절 손 전체에 공통인 프로토콜로 일반화하지 않는다. GraspGraphNet은 filtered CMapDataset의 3종 손으로 학습하고, CMapDataset held-out 10개와 Google Scanned Objects 30개에 대한 perturbation 기반 안정성을 평가한다 (논문 §IV-A, p.5).

- **다관절·여러 손**: [[GraspGraphNet Graph-Structured Grasp Generation]] — URDF 그래프, differentiable FK, 매 스텝 갱신하는 손-물체 edge와 conditional flow matching으로 palm pose 및 관절값을 함께 생성한다.

## Related Papers

- [[2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]] — 가변 손 구조와 관절 차원을 다루는 직접 grasp-state 생성. GraspMF와 로봇·데이터·성공 기준이 달라 수치 우열을 직접 비교하지 않는다.
- [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]] — 속도 축의 현 SOTA 주장. 계보 정리의 출처.

## Related Concepts

- [[Flow Matching]], [[MeanFlow]] — 생성 백본.
- [[Vision-Language-Action Models]] — 추론: VLA는 grasp을 명시적 pose 분포가 아니라 policy 안에 암묵적으로 학습한다. 명시적 grasp 생성은 계획 기반 파이프라인(segmentation → grasp 샘플링 → motion planning)에서 여전히 유효하다.
- [[Tangled-Prone Bin Picking]] — grasp 선택이 성패를 가르는 인접 태스크 축.

## Contradictions / Updates

- 2026-11-02: GraspGraphNet (§III-A, §IV-A)을 반영해 기존 $SE(3)$ 및 ACRONYM 평가 설명의 적용 범위를 parallel-jaw 맥락으로 한정하고, 다관절 손의 palm+joint 생성 축을 추가했다. 기존 GraspMF 결과 자체를 반박하는 것은 아니다.

## Open Questions

- 명시적 grasp 생성 + motion planning 파이프라인과 end-to-end VLA 중 어느 쪽이 산업 배치에서 우세해질 것인가? 위키에 아직 정면 비교 자료 없음.
- Cluttered scene에서의 조건부 분포 학습 (물체 단위 segmentation 의존성 제거)은 어디까지 왔는가?
