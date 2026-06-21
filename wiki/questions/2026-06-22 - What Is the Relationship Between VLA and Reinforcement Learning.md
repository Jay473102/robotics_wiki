---
type: question
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - question
  - vla
  - reinforcement-learning
  - robot-foundation-models
sources:
  - raw/papers/2025 - pi0.6 a VLA That Learns From Experience.pdf
  - raw/papers/2026 - pi0.7 Steerable Generalist Robotic Foundation Model.pdf
---

# What Is the Relationship Between VLA and Reinforcement Learning?

## Short Answer

VLA와 Reinforcement Learning은 같은 위상의 개념이 아니다.

VLA는 로봇 정책 또는 foundation model의 형태이고, RL은 그 정책을 개선하는 학습 원리 또는 최적화 절차다.

$$
\text{VLA} = \text{무엇을 실행하는 모델인가?}
$$

$$
\text{RL} = \text{그 모델을 어떻게 더 좋게 만들 것인가?}
$$

## Why This Question Matters

VLA와 RL을 같은 종류의 모델로 보면 혼동이 생긴다. 실제 로봇 foundation model 연구에서는 VLA를 imitation learning, supervised fine-tuning, offline RL, online RL, preference learning, correction learning 등 여러 방식으로 학습하거나 개선할 수 있다. 따라서 VLA는 policy class에 가깝고, RL은 training/update mechanism에 가깝다.

## Current Answer

VLA, 즉 Vision-Language-Action model은 시각 입력, 언어 지시, 로봇 상태를 받아 행동을 출력하는 policy architecture다.

$$
\text{vision}+\text{language}+\text{robot state}\rightarrow \text{action}
$$

예를 들면 $\pi_{0.7}$, $\pi_{0.6}$, DIAL 같은 모델은 VLA 또는 robot foundation model 계열로 볼 수 있다. 여기서 핵심 질문은 "로봇이 보는 것과 언어 명령을 어떻게 행동으로 연결할 것인가"다.

반면 RL은 특정 모델 형태가 아니다. RL은 policy가 환경에서 행동하고, reward나 success/failure feedback을 통해 더 좋은 행동을 하도록 업데이트하는 학습 framework다.

$$
\text{policy action}\rightarrow \text{reward / failure / correction}\rightarrow \text{policy improvement}
$$

따라서 RL은 작은 MLP policy에도 적용될 수 있고, diffusion policy에도 적용될 수 있고, VLA에도 적용될 수 있다.

## Conceptual Layers

| 구분 | VLA | Reinforcement Learning |
|---|---|---|
| 위상 | 모델 / 정책 구조 | 학습 방식 / 최적화 원리 |
| 입력 | vision, language, robot state | trajectory, reward, value, advantage |
| 출력 | action | policy update 또는 improved policy |
| 핵심 질문 | 무엇을 보고 어떤 행동을 낼까? | 어떤 행동이 더 좋았고 어떻게 개선할까? |
| 예시 | $\pi_{0.7}$, DIAL, RT 계열 VLA | PPO, offline RL, RECAP, advantage conditioning |

## In The Wiki

[[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]은 VLA/RFM 쪽이다. 핵심은 rich context conditioning, subgoal image, metadata, cross-embodiment generalization 같은 모델 구조와 데이터 조건화다.

[[2025 - pi0.6 a VLA That Learns From Experience]]와 [[RECAP RL with Experience and Corrections]]는 VLA에 RL을 붙인 경우다. 이미 있는 VLA를 autonomous rollout, reward feedback, human intervention으로 개선한다.

즉 다음처럼 볼 수 있다.

$$
\pi_{0.6}, \pi_{0.7} = \text{VLA policy}
$$

$$
\text{RECAP} = \text{그 VLA를 RL 방식으로 개선하는 recipe}
$$

## Practical Stack

현재 로봇 foundation model 흐름은 보통 다음 stack으로 이해할 수 있다.

1. VLA/RFM pretraining: robot demonstration, human video, web data, language/action data를 사용한다.
2. Supervised fine-tuning 또는 behavior cloning: 특정 task 행동을 학습한다.
3. RL, offline RL, preference learning, correction learning: 실제 배포 경험으로 성능을 개선한다.

즉 VLA는 RL 이전에도 존재할 수 있고, RL은 VLA 이후의 improvement stage로 붙을 수 있다.

## Important Caveats

RL이 항상 필요한 것은 아니다. 충분한 demonstration과 context conditioning만으로도 strong out-of-the-box VLA를 만들 수 있다. 반대로 실제 배포에서 속도, robustness, failure recovery를 개선하려면 RL이나 correction-based learning이 중요해진다.

VLA와 RL의 관계는 "둘 중 하나를 선택"하는 관계가 아니라, "VLA라는 policy를 RL로 개선할 수 있다"는 포함 관계에 가깝다.

## Linked Pages

- [[Vision-Language-Action Models]]
- [[Robot Foundation Models]]
- [[RECAP RL with Experience and Corrections]]
- [[2025 - pi0.6 a VLA That Learns From Experience]]
- [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]
