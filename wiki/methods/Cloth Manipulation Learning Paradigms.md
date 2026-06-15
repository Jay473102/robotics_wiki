---
type: method
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - cloth-manipulation
  - manipulation
  - learning-paradigms
sources:
  - raw/papers/2026 - Deep Learning-Based Robotic Cloth Manipulation Applications.pdf
---

# Cloth Manipulation Learning Paradigms

## TL;DR

Cloth unfolding/folding 연구는 단순히 supervised/RL/IL로 나누기보다, perception, representation, planning/control 구조로 나누는 편이 실용적이다. Gu et al. 2026은 여섯 paradigm을 제시하며, 각 paradigm은 데이터 요구량, Sim2Real 리스크, metric, failure mode가 다르다.

## Paradigms

- Perception-guided heuristic: keypoint, contour, mask를 예측하고 hand-crafted routine으로 행동한다.
- Goal-conditioned manipulation policy: 현재 cloth state와 목표 이미지를 함께 조건으로 action을 낸다.
- Predictive/model-based representation: cloth dynamics나 latent state transition을 학습해 look-ahead planning에 쓴다.
- Reward-driven RL over primitive actions: pick, drag, fling 같은 primitive parameter를 reward로 학습한다.
- Demonstration-driven skill transfer: expert, teleoperation, human video, simulation oracle demonstration을 imitation한다.
- LLM-based planning: LLM/VLM이 cloth state와 instruction을 보고 primitive sequence나 sub-goal을 고른다.

## Practical Reading

Perception-guided 방식은 structured folding에는 해석 가능하고 강하지만, wrinkle/topology 변화에 취약하다. Reward-driven RL은 dynamic fling 같은 비직관적 primitive를 찾을 수 있으나 interaction cost와 Sim2Real gap이 크다. Demonstration-driven 방식은 real deployment에 가까운 데이터를 쓰기 좋지만 coverage가 일반화 한계를 결정한다. LLM-based planning은 semantic abstraction에 유리하지만 low-level continuous control과 실시간성은 별도 문제가 된다.

## Connections

- [[Robotic Cloth Manipulation]]
- [[Action Affordance Learning]]
- [[Vision-Language-Action Models]]

## Open Questions

- LLM/VLM 기반 high-level planner를 어떤 low-level cloth primitive library와 연결해야 latency와 robustness가 균형을 이루는가?
- Cloth dynamics model은 pixel/video prediction, particle graph, dense correspondence, latent foresight 중 어떤 표현이 가장 재사용 가능한가?
