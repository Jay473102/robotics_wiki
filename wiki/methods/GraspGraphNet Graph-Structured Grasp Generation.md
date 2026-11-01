---
type: method
status: active
created: 2026-11-02
updated: 2026-11-02
tags:
  - method
  - grasping
  - manipulation
  - cross-embodiment
  - flow-matching
  - generative-models
sources:
  - raw/papers/2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation.pdf
---

# GraspGraphNet Graph-Structured Grasp Generation

## TL;DR

URDF로 만든 손의 link-joint graph와 물체 point cloud를 조건으로, palm pose와 관절값을 함께 생성하는 방법이다. 매 flow step에서 differentiable forward kinematics(FK)와 동적 robot-object 연결을 다시 계산하고, conditional flow matching(CFM)의 velocity를 기본 3회 Euler 적분한다. 별도의 grasp 복원용 최적화·hand IK·retargeting 없이 손에 맞는 wrist pose와 관절 명령을 출력한다. 근거: [[2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]], pp. 3–5, Sec. III (Tier A).

## Problem Setting

서로 다른 손은 손가락 수, link 구조, 관절 수 $J$, joint limit가 다르다. 고정 길이 출력 대신 가변 크기 kinematic graph와 공유 per-joint head를 사용해 하나의 모델이 여러 손의 grasp를 생성하도록 한다. 상태는 다음 연속 표현이다.

$$
x=[t_{\mathrm{palm}},R_{\mathrm{palm}}^{6D},q_{\mathrm{norm}}]\in\mathbb R^{9+J}.
$$

병진은 object-centered frame, 회전은 손 사이에서 의미를 맞춘 canonical palm frame의 6D 표현, 관절은 URDF limit로 정규화한 값이다. 물리적 palm pose와 관절 구성이 대상이며, 학습 경로는 이 연속 벡터에서 정의한다. 근거: p. 3, Sec. III-A.

## Procedure

1. **물체 인코딩:** 표면점 1,024개에서 위치·normal·local curvature를 사용한다. 1,024→256→64→32점 계층과 각 계층의 kNN graph를 구성한다. 64점 feature는 국소 상호작용, 32점 feature는 전체 형상 context에 사용한다. 근거: p. 3, Sec. III-B.1.
2. **손 graph 구성:** URDF의 물리 link를 node, parent-child joint를 directed edge로 둔다. Edge에는 joint type·axis·limit·고정 변환을 담고, link visual mesh에서 샘플링한 점을 공유 PointNet으로 인코딩한다. Virtual/사용하지 않는 link는 제외한다. 근거: pp. 3–4, Sec. III-B.2.
3. **학습 초기 상태와 목표를 짝짓기:** 관절은 open-hand 상태로 시작한다. 학습 시 target 방향을 중심으로 한 cone에서 palm 접근 방향을 샘플링하고 in-plane 회전도 샘플링한다. 후보 ground-truth grasp 중 초기 palm과 병진·회전 비용이 가까운 것을 목표로 선택한다. 추론 시에는 target 없이 구면에서 접근 방향을 샘플링한다. 근거: p. 4, Sec. III-E.2; cone angle 30°는 p. 5, Sec. IV-A.
4. **현재 손 상태 인코딩:** 정규화 관절을 복원하고 differentiable FK로 각 link의 world pose를 계산한다. Link geometry, 현재 위치·6D 회전, tree depth, fingertip 여부, 연관 joint state를 결합한 뒤 kinematic-tree MPNN으로 전달한다. 근거: p. 4, Sec. III-C.
5. **물체와 결합:** 손 node를 query로 하는 cross-attention이 coarse object context를 가져온다. 각 link 위치에서 가까운 fine object points로 world edges를 만들고, relative displacement·distance를 포함한 message를 집계한다. 이 연결은 매 flow step에서 새로 계산한다. 기본 설정은 link당 이웃 8개다. 근거: p. 4, Sec. III-D; p. 5, Sec. IV-A.
6. **Velocity 학습:** palm-hub node의 head와 관절별 공유 head가 $v_\theta(x_t,t)=[v_{\mathrm{palm}};v_q]$를 예측한다. 선형 CFM 경로와 target은 아래와 같고, palm/joint MSE를 합쳐 학습한다. 근거: pp. 4–5, Sec. III-E, Eqs. (3)–(5).

$$
x_t=(1-t)x_0+tx_1,\qquad v^*=x_1-x_0,
$$

$$
\mathcal L=\operatorname{MSE}(v_{\mathrm{palm}},v^*_{\mathrm{palm}})
+\lambda_q\operatorname{MSE}(v_q,v_q^*),\qquad\lambda_q=1.
$$

7. **추론 적분:** open-hand $x^{(0)}$에서 시작해 $t_k=k/K$, $\Delta t=1/K$로 갱신한다. 기본 $K=3$이며, 각 갱신에서 FK·상태 feature·world edges가 함께 변한다. 근거: p. 5, Sec. III-F.

$$
x^{(k+1)}=x^{(k)}+\Delta t\,v_\theta(x^{(k)},t_k).
$$

8. **실행 표현으로 변환:** canonical palm orientation을 robot-native frame으로 변환하고, 모델에 정의된 palm-to-wrist offset을 적용하며, joint limit로 관절값을 역정규화한다. 근거: p. 5, Sec. III-F.

## Assumptions / Requirements

- 손 URDF, link visual geometry, 관절 한계 및 frame 변환이 필요하다. 학습에는 object point cloud와 ground-truth grasp annotation을 사용한다. 근거: Sec. III-A–B, III-E.
- 본 논문은 filtered CMapDataset의 Barrett·Allegro·Shadow 데이터를 함께 학습한다. 완전히 다른 손에도 재학습 없이 성공한다는 보장은 아니다. 근거: p. 5, Sec. IV-A; p. 8, Sec. V.
- 정규화에 joint limit를 사용한다는 설명과 collision-free·joint-limit 준수의 형식적 보장은 구분해야 한다. 검증 필요: 추론 중 limit 처리와 6D 회전 decoding의 구현 세부는 코드 확인이 필요하다.

## Inputs / Outputs

- **입력:** 물체 mesh/point cloud, 손 URDF 및 link mesh, 초기 open-hand 상태, flow time. 실기 실험에서는 RGB-D partial point cloud를 사용한다. 근거: Sec. III, p. 7, Sec. IV-D.
- **출력:** 해당 손의 executable wrist pose와 실제 단위 관절 명령. 이는 grasp configuration 생성이며, 본문은 팔의 전체 접근 경로를 생성하는 방법으로 정의하지 않는다. 근거: p. 5, Sec. III-F.
- **계산량 보고:** RTX4090에서 grasp 1개 생성에 평균 40 ms, 기본 $K=3$. Physics simulation 시간은 제외한다. 근거: p. 5, Sec. IV-A; p. 6, Table I.

## Failure Modes

- World-edge 연결을 초기 상태에 고정하면 평균 시뮬레이션 성공률이 83.48%에서 50.23%로 낮아진다. 국소 근접 관계 갱신이 중요한 ablation 결과다. 근거: pp. 7–8, Table V, Sec. IV-E.3.
- Cross-attention 제거 시 54.80%, world-edge MPNN 제거 시 51.27%다. 두 경로를 제거한 결과를 동적 연결만 고정한 결과와 혼동하지 않는다. 근거: p. 7, Table IV.
- 손가락 제거 변형에서도 실패가 남으며 평균 성공률은 72.70%다. 임의의 미지 morphology에 대한 일반화는 검증되지 않았다. 근거: pp. 6–7, Sec. IV-C, Table II; p. 8, Sec. V.
- 추론: 손 grasp 복원에 IK가 필요 없다는 주장만으로 팔 접근 시의 장애물 회피·도달 가능성·실제 접촉 안정성이 보장되지는 않는다. 실험 성공률과 별도의 실행 검증이 필요하다.

## Evidence

- **Tier A, 저자 보고:** 40개 unseen objects(CMapDataset held-out 10 + Google Scanned Objects 30), 손당 4,000회 시뮬레이션에서 평균 83.48%. 성공은 6방향 perturbation에 물체 변위가 2 cm 미만인 경우다. 근거: p. 5, Sec. IV-A; p. 6, Table I.
- **적분 budget:** $K=1$은 78.94%/9 ms, $K=3$은 83.48%/40 ms, $K=20$은 83.87%/189 ms다. 이 논문 설정에서 3 step 이후의 이득이 작다. 근거: p. 8, Table VI.
- **실기:** Leap Hand 데이터로 fine-tune한 모델을 xArm6·Azure Kinect와 사용해 10개 물체에서 100회 중 91회 성공했다. 성공은 들어 올린 뒤 떨어뜨리지 않고 유지하는 것으로, 미지 손 zero-shot 실험이 아니다. 근거: p. 7, Sec. IV-D.
- 원자료와 필기 확인 기록: [[2026-07-13 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]]. 위 수치는 저자 보고이며 이 위키에서 독립 재현하지 않았다.

## Related Concepts

- [[Cross-Embodiment Dexterous Grasping]] — implemented-by: 손마다 다른 graph와 관절 차원을 공유 모델로 처리하는 구현 사례.
- [[Generative Grasp Synthesis]] — 이 방법은 palm pose뿐 아니라 다관절 손의 구성까지 생성하는 문제에 해당한다.
- [[Flow Matching]] — uses: 연속 6D 회전·관절 표현에 선형 CFM 경로와 Euler 적분을 적용한다.
- [[GraspMF Few-Step Grasp Generation]] — 비교할 설계 축: GraspMF는 $SO(3)\times\mathbb R^3$에서 MeanFlow를 사용하며, GraspGraphNet은 그 파생 방법이 아니다. 기존 위키의 GraspMF 15.5 ms는 RTX5080의 100-grasp batch, 본 방법의 40 ms는 RTX4090의 1-grasp 비용이므로 직접 속도비·성공률 우열로 비교하지 않는다.

## Open Questions

- Finger removal을 넘어 link 길이·관절 coupling·구동 방식이 달라진 손에서 재학습 없는 일반화는 어느 범위까지 가능한가?
- 실기 partial point cloud의 occlusion·normal/curvature 오차에 얼마나 민감한가?
- 실제 구현에서 joint limit, mimic/coupled joint, 6D orientation decoding은 어떻게 처리하는가?
- 추론: arm motion planning과 collision 검증을 더한 전체 시스템에서도 생성 지연 감소가 실행 성공률·처리량 개선으로 이어지는가?
