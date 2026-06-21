---
type: question
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - question
  - vla
  - robot-foundation-models
  - reinforcement-learning
sources:
  - raw/papers/2025 - pi0.6 a VLA That Learns From Experience.pdf
  - raw/papers/2026 - pi0.7 Steerable Generalist Robotic Foundation Model.pdf
---

# What Is the Difference Between pi0.6 and pi0.7?

## Short Answer

$\pi^*_{0.6}$는 경험/RL로 특정 task 성능을 개선하는 VLA이고, $\pi_{0.7}$은 처음부터 더 범용적이고 steerable하게 만든 generalist VLA/RFM이다.

한 줄로 정리하면:

> $\pi^*_{0.6}$는 "VLA를 실제 경험으로 강화학습해서 개선하는 방향"이고, $\pi_{0.7}$은 "더 많은 context와 데이터로 처음부터 범용 조작 능력을 키우는 방향"이다.

## Comparison

| 구분 | $\pi^*_{0.6}$ | $\pi_{0.7}$ |
|---|---|---|
| 핵심 방향 | 배포 후 경험으로 개선 | out-of-the-box generalization |
| 중심 방법 | RECAP, offline RL, reward feedback, human intervention | rich context conditioning, subgoal images, metadata, diverse data |
| 개념적 위치 | VLA + RL improvement recipe | steerable generalist robot foundation model |
| 주요 목표 | 특정 downstream task에서 throughput/success 개선 | unseen task, unseen environment, cross-embodiment, compositional generalization |
| 데이터 성격 | demonstrations + autonomous rollouts + interventions | robot data + autonomous/failure data + human egocentric data + web/multimodal data |
| 대표 task | laundry, espresso, box assembly를 반복 개선 | espresso, laundry, trash bag, box folding, vegetable peeling, air fryer 등 out-of-the-box/coachable tasks |

## Current Answer

$\pi^*_{0.6}$는 "연습해서 잘하게 되는 모델"에 가깝다. 처음부터 완벽히 잘하는 것보다, 실제 로봇을 돌려보고 reward, 실패, human correction을 모아서 다시 학습한다. 핵심 키워드는 experience, correction, RL, task-specific improvement다.

이 방향은 [[RECAP RL with Experience and Corrections]]와 연결된다. RECAP은 VLA를 autonomous rollouts, reward feedback, human interventions로 반복 개선하는 offline RL-style training recipe다.

$\pi_{0.7}$은 "처음부터 더 잘 알아듣고 조합하게 만든 모델"에 가깝다. 언어 명령만 넣는 것이 아니라 subgoal image, episode metadata, quality/strategy 같은 context를 같이 넣어 다양한 데이터의 의미를 분리한다. 핵심 키워드는 steerability, context conditioning, compositional generalization, cross-embodiment다.

이 방향은 [[Context-Conditioned Robot Foundation Models]]와 연결된다. $\pi_{0.7}$은 rich prompt/context를 통해 mixed-quality data, non-robot data, autonomous/failure data를 더 잘 활용하려는 generalist pretraining 축이다.

## Conceptual Difference

$\pi^*_{0.6}$는 deployment-time improvement의 사례다.

$$
\text{pretrained VLA}
\rightarrow \text{task deployment}
\rightarrow \text{reward / correction}
\rightarrow \text{improved task policy}
$$

$\pi_{0.7}$은 generalist pretraining and steering의 사례다.

$$
\text{diverse data}+\text{rich context}
\rightarrow \text{steerable generalist VLA}
\rightarrow \text{out-of-the-box task execution}
$$

따라서 두 모델은 단순 버전 번호 차이만이 아니라 연구 질문이 다르다. $\pi^*_{0.6}$는 "실제 경험으로 VLA를 어떻게 개선할까?"에 가깝고, $\pi_{0.7}$은 "처음부터 어떤 context와 data mixture로 더 범용적인 VLA를 만들까?"에 가깝다.

## Evidence / Sources

- [[2025 - pi0.6 a VLA That Learns From Experience]]: RECAP을 통해 $\pi^*_{0.6}$가 autonomous experience와 corrections로 laundry, espresso, box assembly 성능을 개선한다고 정리한다.
- [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]: $\pi_{0.7}$이 rich context conditioning으로 out-of-the-box dexterity, cross-embodiment transfer, compositional generalization을 추구한다고 정리한다.
- [[2026-06-22 - What Is the Relationship Between VLA and Reinforcement Learning]]: VLA는 policy/model class이고 RL은 policy improvement framework라는 개념적 구분을 제공한다.

## Important Caveats

$\pi_{0.7}$이 모든 면에서 $\pi^*_{0.6}$를 대체한다고 보면 안 된다. $\pi_{0.7}$은 generalist/out-of-the-box 능력을 강조하고, $\pi^*_{0.6}$는 deployment data로 특정 task를 강화하는 절차를 강조한다. 실제 시스템에서는 $\pi_{0.7}$ 같은 generalist model 위에 RECAP류 post-training을 붙이는 조합도 가능하다.

## Linked Pages

- [[2025 - pi0.6 a VLA That Learns From Experience]]
- [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]
- [[RECAP RL with Experience and Corrections]]
- [[Context-Conditioned Robot Foundation Models]]
- [[Vision-Language-Action Models]]
- [[Robot Foundation Models]]
