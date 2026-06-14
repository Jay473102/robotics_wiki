---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - world-modeling
  - vla
  - robot-foundation-models
sources:
  - raw/papers/260329844v1 1_260615_004135.pdf
---

# Latent World Modeling

## Definition

Latent world modeling은 미래 상태를 raw pixel이나 explicit state로 직접 예측하지 않고, encoder 내부의 latent feature space에서 예측하는 world modeling 접근이다. DIAL에서는 VLM의 native ViT feature space 안에서 미래 관측 feature를 예측해 robot policy의 intent bottleneck으로 사용한다.

## Why It Matters

로봇 VLA에서 language-level plan은 해석 가능하지만 low-level control과 끊어지기 쉽고, direct action prediction은 VLM의 semantic prior를 망가뜨릴 수 있다. Latent world modeling은 "무엇이 되어야 하는가"를 continuous differentiable representation으로 전달해 high-level reasoning과 action learning을 연결할 수 있다.

## Key Ideas

- Future prediction target은 $Enc_{ViT}(o_{t+H})$ 같은 pretrained visual feature일 수 있다.
- Latent foresight는 policy가 현재 상태와 목표 미래 상태의 차이를 계산하는 interface가 된다.
- Feature-space consistency가 중요하다. DIAL은 System-2와 System-1이 같은 frozen ViT feature manifold를 공유하도록 설계한다.
- Decoupled warmup은 world model과 policy가 서로 불안정한 초기 prediction에 끌려가지 않게 하는 안정화 절차다.

## Related Papers

- [[2026 - DIAL Decoupling Intent and Action via Latent World Modeling]]

## Related Concepts

- [[Vision-Language-Action Models]]
- [[Robot Foundation Models]]
- [[Embodied AI]]

## Open Questions

- Latent target은 VLM-native ViT feature, self-supervised visual feature, robot-specific feature 중 무엇이 가장 transfer에 강한가?
- Latent foresight가 실제 causal dynamics를 학습했는지, 또는 benchmark shortcut을 학습했는지 어떻게 평가할 것인가?
