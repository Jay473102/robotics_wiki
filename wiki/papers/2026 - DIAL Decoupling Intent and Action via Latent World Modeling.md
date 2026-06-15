---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - vla
  - latent-world-modeling
  - robot-foundation-models
  - humanoid
  - imitation-learning
sources:
  - raw/papers/2026 - DIAL Decoupling Intent and Action via Latent World Modeling.pdf
title: DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA
authors:
  - Yi Chen
  - Yuying Ge
  - Hui Zhou
  - Mingyu Ding
  - Yixiao Ge
  - Xihui Liu
year: 2026
venue: arXiv 2603.29844v1
doi:
url: https://xpeng-robotics.github.io/dial
---

# DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA

## TL;DR

DIAL은 VLA에서 VLM의 high-level intent와 robot policy의 low-level action 사이에 differentiable latent foresight bottleneck을 둔다. System-2는 VLM-native ViT latent space에서 미래 관측의 feature를 예측하고, System-1은 현재 관측과 예측된 latent intent를 비교해 action chunk를 생성한다. 논문은 RoboCasa GR1 Tabletop과 IRON-R01-1.11 real robot에서 성능, data efficiency, OOD generalization 개선을 보고한다.

## Problem

기존 hierarchical planner는 high-level plan과 low-level control 사이가 non-differentiable이라 latency가 크고 action gradient가 VLM을 개선하지 못한다. 반대로 end-to-end VLA는 VLM을 큰 multimodal encoder처럼 쓰다가 action supervision이 semantic representation을 손상시키거나 shortcut learning을 만들 수 있다.

## Core Idea

DIAL은 "intent"를 text나 pixel이 아니라 VLM 내부 ViT feature space의 future latent visual foresight로 표현한다. 이 latent intent가 반드시 System-1의 action generation 조건으로 쓰이도록 structural bottleneck을 만든다.

관련 페이지:

- [[Vision-Language-Action Models]]
- [[Latent World Modeling]]
- [[Robot Foundation Models]]
- [[Embodied AI]]

## Method

- System-2: pretrained VLM에 learnable query token을 붙이고, 현재 관측과 언어 지시를 받아 $H$ step 뒤 관측의 ViT feature를 예측한다.
- System-1: shared frozen ViT로 현재 관측을 encode하고, 예측된 latent foresight와 함께 flow-matching 기반 DiT policy가 action chunk를 생성한다.
- Objective: latent world modeling loss는 예측 intent $x_t$와 $Enc_{ViT}(o_{t+H})$의 MSE로 정의된다.
- Training: decoupled warmup에서 System-2는 latent future prediction을, System-1은 ground-truth future feature 조건의 motor control을 먼저 학습한 뒤 end-to-end joint optimization으로 넘어간다.

## Data / Embodiment

Simulation은 RoboCasa GR1 Tabletop 24개 task를 사용한다. Robot state/action은 dual arms, hands, waist, end-effector pose를 포함한 47차원 표현이다. Human data는 EgoDex `basic_pick_place` subset 27,419 trajectories를 사용한다.

Real-world는 IRON-R01-1.11 humanoid robot에서 수행하며, head 3-DoF가 추가된 50차원 state/action space를 쓴다. Pick & Place와 Pouring task를 구성하고, task별 120 robot trajectories 및 32k proprietary factory robot trajectories, 30k EgoDex trajectories를 섞은 pretraining을 보고한다.

## Evaluation

논문은 다섯 research questions를 평가한다: 성능/샘플 효율, architecture ablation, human data scalability, real-world robustness, latent foresight interpretability. Simulation OOD는 unseen appearance, unseen combinations, unseen object types로 나눈다. Real-world OOD는 combinatorial generalization, distractor robustness, instance-level transfer로 나눈다.

## Results

- RoboCasa GR1 Tabletop full-data setting에서 평균 70.2% success rate를 보고한다.
- Few-shot setting에서 task당 100 trajectories로 58.3% success rate를 보고한다.
- DIAL-DINO는 58.3%에서 47.2%로 떨어져, VLM-native feature alignment가 중요하다는 ablation 근거로 쓰인다.
- Human data는 pick-and-place와 OOD 성능을 올리지만, articulated task는 EgoDex coverage mismatch 때문에 개선되지 않았다고 해석한다.
- Real-world에서 decoupled warmup 제거는 in-distribution 평균 77.5%에서 57.5%, OOD 평균 58.3%에서 30.0%로 하락한다고 보고한다.

## Limitations

논문은 arXiv preprint이며, 일부 real-world data는 proprietary factory trajectories라 재현성이 제한된다. System-1은 상대적으로 작은 DiT backbone이고, VLM-native ViT는 안정적 feature alignment를 위해 frozen으로 둔다. 저자들은 future work로 larger System-1, ViT end-to-end fine-tuning, action-free human video 기반 latent foresight pretraining을 제안한다.

## Connections

DIAL은 [[Vision-Language-Action Models]]에서 "VLM을 encoder로만 쓰지 말고 predictive intent generator로 쓰자"는 강한 설계 방향을 제시한다. [[Latent World Modeling]]은 high-level reasoning과 low-level control 사이의 interface로 쓰이며, [[Physical AI]] 관점에서는 human video와 robot data를 연결하는 cross-embodiment learning 사례다.

## Contradictions / Updates

검증 필요: 보고된 SOTA, 10배 data efficiency, real-world generalization은 논문 내부 benchmark 기준이다. 독립 재현, benchmark version, baseline tuning, proprietary data 영향은 별도 확인이 필요하다.

## Open Questions

- Latent foresight bottleneck은 다른 VLM backbone과 robot embodiment에서도 같은 효과를 내는가?
- VLM-native feature space가 항상 최선인가, 아니면 task에 따라 DINO/robot-specific encoder가 더 유리한 경우가 있는가?
- Action-free human video를 latent world modeling pretraining에 쓰면 embodiment gap을 얼마나 줄일 수 있는가?
- Decoupled warmup은 모든 end-to-end VLA에 필요한 일반 원칙인가, DIAL 구조에 특화된 안정화 장치인가?
