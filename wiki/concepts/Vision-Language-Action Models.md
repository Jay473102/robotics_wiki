---
type: concept
status: draft
created: 2026-06-14
updated: 2026-06-15
tags:
  - vla
  - robot-foundation-models
  - robotics
sources:
  - raw/notes/deep-research-report.md
  - raw/papers/2026 - DIAL Decoupling Intent and Action via Latent World Modeling.pdf
---

# Vision-Language-Action Models

## Definition

Vision-Language-Action Models, 또는 VLA 모델은 시각 입력과 언어 지시를 받아 로봇 행동을 출력하는 모델 계열이다. 일반적으로 perception-language grounding과 policy learning을 하나의 모델 또는 결합된 시스템으로 다룬다.

## Why It Matters

VLA는 로봇 foundation model의 핵심 후보 중 하나다. 자연어 지시, 시각 장면 이해, 조작 행동을 연결하므로 manipulation, mobile manipulation, household robotics, 산업용 task generalization과 직접 연결된다.

## Key Issues

- Action representation: end-effector pose, joint commands, discretized tokens, continuous control.
- Data mixture: robot demonstrations, human videos, simulation, web-scale vision-language data.
- Generalization: new objects, new scenes, new instructions, new embodiments.
- Evaluation: benchmark success rate와 실제 배포 성능 사이의 차이.
- Intent-action interface: VLM의 high-level reasoning을 low-level motor control로 어떻게 전달할지. [[2026 - DIAL Decoupling Intent and Action via Latent World Modeling]]은 latent visual foresight를 differentiable bottleneck으로 쓰는 설계를 제안한다.
- Training stability: end-to-end action supervision이 VLM semantic representation을 손상시키거나 shortcut learning을 만들 수 있어, decoupled warmup이나 auxiliary world modeling이 필요할 수 있다.

## Related Concepts

- [[Embodied AI]]
- [[Physical AI]]
- [[Robot Foundation Models]]
- [[Action Affordance Learning]]
- [[Latent World Modeling]]

## Open Questions

- VLA 모델은 embodiment 차이를 어떤 방식으로 흡수할 수 있는가?
- 언어/비전 사전학습과 로봇 행동 데이터의 최적 혼합 비율은 무엇인가?
- VLM-native feature space와 robot-specific visual feature space 중 어떤 것이 control grounding에 더 안정적인가?
- Latent foresight bottleneck은 planner-policy 분리와 end-to-end VLA 사이의 일반적인 절충점이 될 수 있는가?
