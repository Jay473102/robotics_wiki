---
type: method
status: draft
created: 2026-06-21
updated: 2026-06-21
tags:
  - reinforcement-learning
  - vla
  - robot-learning
  - advantage-conditioning
sources:
  - raw/papers/2025 - pi0.6 a VLA That Learns From Experience.pdf
---

# RECAP RL with Experience and Corrections

## Summary

RECAP, RL with Experience and Corrections via Advantage-conditioned Policies,는 VLA를 demonstrations, autonomous rollouts, reward feedback, human interventions로 반복 개선하는 offline RL-style training recipe다.

## Workflow

1. Task에 VLA를 배포해 episode outcome reward와 autonomous rollout을 수집한다.
2. 위험하거나 실패가 보이는 경우 expert teleoperation intervention을 기록한다.
3. 모든 데이터를 사용해 language-conditioned value function을 학습한다.
4. Value function으로 action advantage를 추정하고 improvement indicator를 만든다.
5. Improvement indicator를 VLA prefix/context에 넣어 advantage-conditioned policy를 학습한다.
6. 개선된 policy를 다시 배포하고 반복한다.

## Why It Matters

VLA를 실제 배포 task에서 개선하려면 demonstration만으로는 부족하다. RECAP은 large VLA에 직접 PPO류 policy gradient를 적용하는 대신, off-policy/offline data를 재사용할 수 있는 value-based advantage conditioning을 사용한다.

## Key Design Choices

- Heterogeneous data를 버리지 않고 demonstrations, interventions, autonomous failures를 함께 쓴다.
- Value function은 실패 감지와 task completion progress를 추정한다.
- Policy extraction은 advantage-conditioned behavior cloning에 가깝다.
- Human-gated DAgger식 correction과 autonomous experience를 모두 포함한다.

## Failure Modes

- Reward labeling이 잘못되면 value function과 advantage indicator가 함께 오염된다.
- Human intervention 기준이 일관되지 않으면 correction data가 bias를 만들 수 있다.
- Safety-critical task에서는 autonomous rollout collection 자체가 위험할 수 있다.

## Related

- [[2025 - pi0.6 a VLA That Learns From Experience]]
- [[Vision-Language-Action Models]]
- [[Robot Foundation Models]]
- [[Context-Conditioned Robot Foundation Models]]
