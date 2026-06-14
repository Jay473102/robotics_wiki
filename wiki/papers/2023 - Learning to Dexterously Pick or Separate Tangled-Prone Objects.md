---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - bin-picking
  - manipulation
  - action-affordance
  - self-supervised-learning
  - sim-to-real
sources:
  - raw/papers/2302.08152v2.pdf
title: Learning to Dexterously Pick or Separate Tangled-Prone Objects for Industrial Bin Picking
authors:
  - Xinyi Zhang
  - Yukiyasu Domae
  - Weiwei Wan
  - Kensuke Harada
year: 2023
venue: arXiv 2302.08152v2
doi:
url: https://arxiv.org/abs/2302.08152
---

# Learning to Dexterously Pick or Separate Tangled-Prone Objects for Industrial Bin Picking

## TL;DR

얽힘이 쉬운 산업용 부품의 bin picking을 위해 `pick`, `drop`, `pull`을 계층적으로 선택하는 조작 정책을 제안한다. 핵심은 depth image에서 action affordance를 예측하는 `PickNet`과 `PullNet`이며, 학습 데이터는 physics simulation의 algorithmic supervisor로 self-supervised 수집한다. PDF는 real-world 실험에서 약 90% success rate를 보고한다.

## Problem

일반 bin picking은 clutter와 occlusion만으로도 어렵지만, S자형/후크형/와이어형처럼 서로 얽히는 부품은 한 번에 여러 개가 딸려 올라오거나 grasp 후 분리되지 않는 문제가 생긴다. 기존 방식은 entangled object를 피하거나 object-specific model에 의존하는 경우가 많아, bin 안에 isolated object가 없는 상황을 잘 처리하지 못한다.

## Core Idea

정책은 먼저 isolated object를 찾고, 없으면 entangled object를 buffer bin으로 떨어뜨려 얽힘을 약화시킨다. buffer bin에서도 isolated object가 아니면 `PullNet`으로 pulling 위치와 방향을 예측해 분리와 운반을 동시에 시도한다.

관련 개념:

- [[Tangled-Prone Bin Picking]]
- [[Object Singulation]]
- [[Action Affordance Learning]]

## Method

- `PickNet`: depth image를 입력으로 `PickMap`과 `SepMap`을 출력한다. `PickMap`은 isolated object를 집을 가능성, `SepMap`은 entangled object를 분리 대상으로 삼을 가능성을 나타낸다.
- `PullNet`: depth image를 여러 방향으로 회전해 pulling 방향을 encode하고, pull position affordance를 예측한다.
- Motion primitives: `picking`, `dropping`, `pulling`.
- Data collection: simulator의 full object state를 이용해 graph projection과 crossing annotation으로 tangled/untangled state와 pulling candidate를 만든다.

## Data / Embodiment

- 입력: top-down depth image.
- Robot: PDF 실험에서는 Kawada NEXTAGE와 Photoneo PhoXi 3D scanner M을 사용한다.
- Training: synthetic data, NVIDIA PhysX 기반 simulation, ResNet-50 + U-Net style skip connection이 언급된다.

## Evaluation

비교 대상은 geometric feature extraction 계열 baseline과 entanglement map baseline이다. Simulation에서는 isolated object 탐지 능력을 비교하고, real-world에서는 20개 물체가 든 bin을 비우는 task로 success rate, completion, action efficiency를 평가한다.

## Results

- PDF 초록과 본문은 real-world experiment에서 약 90% success rate를 보고한다.
- `dropping`은 얽힘 정도를 낮추지만 중간 행동이라 action efficiency가 낮아질 수 있다.
- `pulling`은 분리와 goal bin 이동을 함께 수행할 수 있어 action efficiency 개선에 기여한다.
- unseen objects에서도 일반화 결과를 제시하지만 seen objects보다 지표가 낮다.

## Limitations

- Top-down depth map만으로 실제로 몇 개 물체가 같이 잡힐지 예측하기 어렵다.
- endless chain 형태의 얽힘이나 tightly wedged objects는 제안된 primitive로 처리하기 어렵다.
- pulling은 bin wall, 이웃 물체, contact modeling 오차에 민감하다.
- 향후 다양한 shape, deformable objects, 추가 sensing, 더 복잡한 motion primitive가 필요하다고 본다.

## Connections

- [[Vision-Language-Action Models]]와 직접 같은 계열은 아니지만, visual observation에서 action을 선택한다는 점에서 action representation과 affordance learning의 좋은 고전적 연결점이다.
- [[Physical AI]] 관점에서는 simulation supervision, real-world execution, failure mode 분석이 함께 들어간 실용 조작 사례다.

## Contradictions / Updates

검증 필요: PDF가 arXiv 버전이므로 최종 학회/저널 게재 여부와 이후 확장 연구는 별도 확인이 필요하다.

## Open Questions

- tactile/force sensing을 추가하면 entanglement state estimation이 얼마나 좋아지는가?
- bimanual manipulation이나 regrasp planning을 넣으면 tightly wedged failure mode를 줄일 수 있는가?
