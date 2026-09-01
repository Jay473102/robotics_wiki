---
type: concept
status: draft
created: 2026-09-01
updated: 2026-09-01
tags:
  - grasping
  - bin-picking
  - manipulation
  - industrial-automation
sources:
  - raw/papers/2608.28175v1.pdf
---

# Model-Based and Model-Free Grasping

## Definition

로봇 grasping 접근의 기본 이분법. **Model-based(분석적)**: 알려진 CAD 기하로 물체를 6D pose 추정하고 물체 좌표계에 사전 정의된 grasp을 collision·kinematics 검사 후 실행한다. **Model-free(학습 기반)**: pose 추정 없이 센서 데이터에서 직접 grasp을 예측한다 — 후보를 채점하는 discriminative(Dex-Net 계열)와 grasp pose를 직접 합성하는 generative(Contact-GraspNet, GraspGen, [[Generative Grasp Synthesis]] 축)로 나뉜다.

## Why It Matters

산업 현장은 이 이분법의 trade-off 위에 서 있다. Model-based는 반복 정밀도·oriented placing·높은 GSR을 주지만 부품별 수동 commissioning과 perception 실패 시 deadlock이 약점이고, model-free는 "out-of-the-box" 범용성과 bin 완전 배출을 주지만 GSR·결정성·의미 이해(얽힘 검출, oriented placing)가 약하다. [[2026 - Picking Bins Empty Hierarchical Hybrid Bin-Picking]]이 같은 setup에서 이를 정량화했다: model-based는 clearance 50.9% / GSR 99.1%, model-free(CGN)는 clearance 100% / GSR 45.6%.

## Key Ideas

- 산업 표준은 여전히 model-based다 (Tier A: 위 논문 related work). 학습 기반 방법은 embodiment·gripper 다양성에 걸친 강건한 실배치에 아직 도달하지 못했다.
- 절충 계열: 오프라인 grasp 자동 합성(Kleeberger et al. — 기하 특징 + 시뮬레이션), 실기 self-supervision(Pinto & Gupta 50K, Levine et al. 800K), rule-based 출력으로 DL을 학습시키는 hybrid(Komoda et al. — 단 성능이 rule 품질에 캡핑).
- 두 방식을 택일이 아니라 **계층적 상보 관계**로 결합하는 것이 [[Hierarchical Hybrid Bin-Picking]]의 핵심: model-based가 주 경로, model-free가 실패 지점의 fallback + 탐색 에이전트.
- 추론: [[Vision-Language-Action Models]]는 이 이분법 바깥의 세 번째 축(암묵적 grasp)이며, 산업 bin picking에서의 정면 비교 자료는 위키에 아직 없다.

## Related Papers

- [[2026 - Picking Bins Empty Hierarchical Hybrid Bin-Picking]] — 이분법의 정량화와 hybrid 해소.
- [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]] — model-free affordance 계열의 산업 응용.

## Related Concepts

- [[Generative Grasp Synthesis]] — model-free generative 갈래의 연구 축.
- [[Action Affordance Learning]] — model-free의 또 다른 표현 형태 (pixel-wise).
- [[2026-09-01 - Grasp Generation and Object Singulation]] — 이 이분법이 두 grasp 축 종합의 배경 구도.

## Open Questions

- 열린 질문: zero-shot pose 추정(BOP 계열 진전)이 model-based의 commissioning 비용을 없애면 이분법은 어디로 수렴하는가?
