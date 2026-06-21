---
type: concept
status: draft
created: 2026-06-21
updated: 2026-06-21
tags:
  - robot-foundation-models
  - vla
  - prompting
  - compositional-generalization
sources:
  - raw/papers/2026 - pi0.7 Steerable Generalist Robotic Foundation Model.pdf
  - raw/papers/2025 - pi0.6 a VLA That Learns From Experience.pdf
---

# Context-Conditioned Robot Foundation Models

## Definition

Context-conditioned robot foundation model은 language instruction뿐 아니라 subgoal images, episode metadata, quality/strategy labels, advantage indicators, embodiment/control metadata 같은 추가 context를 prompt나 prefix로 받아 행동을 조절하는 로봇 foundation model이다.

## Why It Matters

로봇 데이터는 task, embodiment, operator strategy, success quality가 섞여 있다. 같은 명령이라도 "빠르게", "정확하게", "실패를 회피하며", "특정 subgoal을 따라" 수행해야 할 수 있다. Context conditioning은 이 ambiguity를 줄여 mixed-quality data와 diverse strategy를 더 잘 활용하게 한다.

## Key Ideas

- [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]은 subgoal images, detailed language, episode metadata로 $\pi_{0.7}$을 steerable하게 만든다.
- [[2025 - pi0.6 a VLA That Learns From Experience]]는 value function에서 나온 advantage/improvement indicator를 condition으로 사용한다.
- Context는 training-time data disambiguation과 inference-time steering 양쪽에 쓰일 수 있다.
- Rich context가 없는 baseline은 diverse data의 mode averaging이나 failure imitation에 더 취약할 수 있다.

## Related Papers

- [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]
- [[2025 - pi0.6 a VLA That Learns From Experience]]

## Related Concepts

- [[Vision-Language-Action Models]]
- [[Robot Foundation Models]]
- [[RECAP RL with Experience and Corrections]]

## Open Questions

- Context metadata를 사람이 얼마나 제공해야 하고, 얼마나 자동 생성할 수 있는가?
- Generated subgoal image나 quality metadata가 틀렸을 때 policy가 failure를 감지할 수 있는가?
- Context conditioning은 embodiment transfer를 돕는가, 아니면 특정 platform metadata에 과적합하게 만드는가?
