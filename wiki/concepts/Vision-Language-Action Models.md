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

## Related Concepts

- [[Embodied AI]]
- [[Physical AI]]
- [[Robot Foundation Models]]
- [[Action Affordance Learning]]

## Open Questions

- VLA 모델은 embodiment 차이를 어떤 방식으로 흡수할 수 있는가?
- 언어/비전 사전학습과 로봇 행동 데이터의 최적 혼합 비율은 무엇인가?
