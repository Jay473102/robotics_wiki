---
type: question
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - question
  - cloth-manipulation
  - physical-ai
sources:
  - raw/papers/frobt-13-1752914.pdf
---

# What Blocks General Robotic Cloth Manipulation?

## Short Answer

일반적인 cloth manipulation의 병목은 단일 모델 성능보다 데이터, state representation, action primitive, metric, sensing이 함께 얽힌 시스템 문제다. Gu et al. 2026은 unfolding/folding 연구 41편을 정리하면서 특히 Sim2Real gap, real-world data collection cost, folding metric 부재, 복잡한 garment state, vision-only failure mode를 반복 병목으로 제시한다.

## Why This Question Matters

Cloth manipulation은 Physical AI가 rigid object manipulation을 넘어 실사용 환경으로 가는지 확인하는 좋은 시험대다. 수건 한 장을 펴는 것과 뒤집힌 긴팔 티셔츠를 인식해 접는 것은 같은 "cloth"라도 state complexity와 primitive 요구가 크게 다르다.

## Current Answer

- Simulation만으로는 cloth stiffness, mass, texture, air interaction, contact를 충분히 맞추기 어렵다.
- Real-world 데이터는 annotation, robot wear, sensing setup, human intervention 비용이 크다.
- Folding은 goal configuration이 다양해 success rate 정의가 논문마다 다르다.
- Vision-only system은 self-occlusion, multi-layer grasp, corner detection failure에 취약하다.
- Unified unfolding-to-folding policy는 유망하지만 아직 소수 연구만 다룬다.

## Useful Follow-Up Questions

- Folding consensus metric은 coverage, IoU, keypoint error, human-acceptable shape 중 무엇을 중심으로 잡아야 하는가?
- Dynamic primitive와 tactile sensing을 결합하면 large cloth와 multi-layer failure를 동시에 줄일 수 있는가?
- Human video를 쓰는 imitation learning은 robot embodiment gap을 어떻게 보정해야 하는가?
- LLM/VLM planner는 primitive selection에 머물러야 하는가, 아니면 latent policy와 end-to-end로 결합해야 하는가?

## Linked Pages

- [[2026 - Deep Learning-Based Robotic Cloth Manipulation Applications]]
- [[Robotic Cloth Manipulation]]
- [[Cloth Manipulation Learning Paradigms]]
