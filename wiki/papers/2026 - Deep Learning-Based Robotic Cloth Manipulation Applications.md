---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - cloth-manipulation
  - manipulation
  - physical-ai
  - survey
  - sim-to-real
sources:
  - raw/papers/frobt-13-1752914.pdf
title: Deep learning-based robotic cloth manipulation applications: systematic review, challenges and opportunities for physical AI
authors:
  - Ningquan Gu
  - Mitsuhiro Hayashibe
  - Kyo Kutsuzawa
  - Hui Yu
year: 2026
venue: Frontiers in Robotics and AI 13:1752914
doi: 10.3389/frobt.2026.1752914
url:
---

# Deep Learning-Based Robotic Cloth Manipulation Applications

## TL;DR

DL 기반 robotic cloth unfolding/folding 연구 41편을 정리한 systematic review다. 핵심 기여는 기존의 supervised/RL/IL 분류 대신, cloth를 어떻게 지각하고 표현하고 조작 행동으로 변환하는지에 따라 여섯 learning-and-control paradigm으로 재구성한 점이다. Physical AI 관점에서는 데이터 수집, Sim2Real, primitive action, metric 표준화, multimodal sensing이 병목으로 보인다.

## Problem

Cloth manipulation은 무한차원에 가까운 configuration space, self-occlusion, 복잡한 deformable dynamics 때문에 rigid object manipulation보다 어렵다. Unfolding과 folding은 세탁, 유통, 제조, 보조 로봇에서 기본 작업이지만, 초기 상태 다양성, garment shape, long-horizon dynamics, 평가 지표 불일치 때문에 일반화가 아직 약하다.

## Core Idea

논문은 deep learning 기반 cloth unfolding/folding 연구를 task, dataset, platform, primitive action, metric, failure mode, learning paradigm으로 분해한다. 특히 algorithm taxonomy를 다음 여섯 축으로 정리한다.

- Perception-guided heuristic methods
- Goal-conditioned manipulation policies
- Predictive and model-based state representation methods
- Reward-driven reinforcement learning over primitive actions
- Demonstration-driven skill transfer methods
- LLM-based planning methods

관련 페이지:

- [[Robotic Cloth Manipulation]]
- [[Cloth Manipulation Learning Paradigms]]
- [[Physical AI]]
- [[Vision-Language-Action Models]]

## Method

PRISMA guidelines를 따라 2019-2024년 문헌을 검색하고 41편을 선별했다. 분석 대상은 unfolding/folding task contents, dataset collection, manipulation platform, primitive actions, performance metrics, failure modes, learning/control paradigms다.

## Data / Embodiment

리뷰된 연구들은 주로 top-view RGB, depth, RGB-D, point cloud를 사용한다. Robot platform은 single-arm이 다수이고, dual-arm은 더 복잡한 cloth task에서 중요하다. End-effector는 parallel gripper가 주류지만, dexterous hand와 tactile/force sensing은 향후 기회로 정리된다.

## Evaluation

이 논문 자체는 survey이므로 새 benchmark를 제시하지 않는다. 대신 각 논문이 사용하는 coverage, action count, success rate, cloth particle distance, IoU류 metric과 failure mode를 비교한다. Unfolding은 coverage/action count가 비교적 자주 쓰이나, folding은 goal shape과 task 정의가 달라 metric 합의가 약하다.

## Results

- Simulation은 많이 쓰이지만 cloth property, visual diversity, dynamics mismatch 때문에 Sim2Real gap이 계속 남는다.
- Real-world data collection은 유용하지만 labor, robot wear, annotation cost, sensing limitation이 크다.
- Dynamic fling, drag/mop, air blowing 같은 primitive action이 larger garment와 efficiency 문제를 완화한다.
- LLM/VLM 기반 planning은 semantic reasoning과 high-level primitive selection에는 유망하지만, low-level 실시간 제어와 latency는 아직 한계다.

## Limitations

Survey 범위가 unfolding/folding에 집중되어 dressing, ironing, sewing 같은 cloth manipulation task는 주변부로만 다뤄진다. 또한 논문별 실험 환경과 metric이 달라 정량 비교는 제한적이다.

## Connections

이 리뷰는 [[Action Affordance Learning]], [[Object Singulation]], [[Vision-Language-Action Models]]와 연결된다. Deformable object manipulation에서 VLA/LLM을 바로 low-level policy로 쓰기보다, primitive action, metric, sensing, dataset 병목을 먼저 명확히 해야 한다는 근거를 준다.

## Contradictions / Updates

검증 필요: 논문은 2026년 2월 출판되었지만 literature coverage는 2019-2024년 중심이다. 2025-2026년 VLA, diffusion policy, robot foundation model 기반 cloth manipulation 후속 연구는 별도 업데이트가 필요하다.

## Open Questions

- Unfolding과 folding을 분리된 policy가 아니라 하나의 end-to-end policy로 안정적으로 학습할 수 있는가?
- Folding task에는 어떤 consensus metric이 필요한가?
- Cloth simulator는 어느 수준의 물성/공기역학/robot contact fidelity를 제공해야 Sim2Real에 충분한가?
- Tactile/force sensing은 multi-layer grasping, corner localization, occlusion 문제를 얼마나 줄이는가?
