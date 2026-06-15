---
type: question
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - question
  - vla
  - robot-foundation-models
  - world-modeling
sources:
  - raw/papers/2026 - DIAL Decoupling Intent and Action via Latent World Modeling.pdf
---

# How Should VLA Models Bridge Intent and Action?

## Short Answer

DIAL의 답은 high-level intent와 low-level action 사이를 text plan도 raw action token도 아닌 latent visual foresight로 연결하자는 것이다. VLM은 미래 subgoal의 latent representation을 예측하고, policy는 현재 관측과 그 latent intent의 차이를 action chunk로 풀어낸다.

## Source Research Questions

DIAL 본문은 평가 질문을 Q1-Q5로 명시한다.

- Performance: DIAL이 public humanoid simulation benchmark에서 success rate와 sample efficiency를 개선하는가?
- Architecture: VLM의 high-level intent를 low-level control에 grounding하는 데 어떤 구조가 필수인가?
- Scalability: heterogeneous human demonstrations가 in-distribution과 OOD 성능을 모두 개선하는가?
- Robustness: real-world generalization이 가능한가, decoupled warmup은 어떤 역할을 하는가?
- Interpretability: predicted latent foresight가 VLM-native feature space에서 의미 있는 task dynamics를 담는가?

## Current Answer

DIAL의 ablation 기준으로는 세 요소가 핵심이다. 첫째, latent world modeling objective가 있어야 VLM representation이 미래 상태와 연결된다. 둘째, System-1이 intent를 우회하지 못하도록 structural bottleneck을 둬야 한다. 셋째, reasoning과 control이 같은 feature manifold를 공유해야 semantic-physical misalignment가 줄어든다.

## Important Caveats

검증 필요: 이 답은 DIAL 논문 내부 결과에 기반한다. Proprietary data, benchmark selection, baseline tuning, 실제 hardware variability가 결론에 어느 정도 영향을 줬는지는 독립 재현 전까지 열어둬야 한다.

## Linked Pages

- [[2026 - DIAL Decoupling Intent and Action via Latent World Modeling]]
- [[Latent World Modeling]]
- [[Vision-Language-Action Models]]
