---
type: source
status: ingested
created: 2026-06-15
updated: 2026-06-15
tags:
  - source
  - paper
  - cloth-manipulation
  - manipulation
  - physical-ai
sources:
  - raw/papers/frobt-13-1752914.pdf
---

# Deep Learning-Based Robotic Cloth Manipulation Review Source

## Source

- Raw file: `raw/papers/frobt-13-1752914.pdf`
- Title: "Deep learning-based robotic cloth manipulation applications: systematic review, challenges and opportunities for physical AI"
- Authors: Ningquan Gu, Mitsuhiro Hayashibe, Kyo Kutsuzawa, Hui Yu
- Venue: Frontiers in Robotics and AI 13:1752914
- Published: 2026-02-06
- DOI: `10.3389/frobt.2026.1752914`

## Extraction Summary

이 systematic review는 2019-2024년에 발표된 deep learning 기반 cloth unfolding/folding 연구 41편을 PRISMA 절차로 선별해 분석한다. 기존 survey의 supervised/RL/IL 같은 학습 방식 분류가 너무 거칠다고 보고, cloth state를 어떻게 지각하고 표현하고 행동으로 연결하는지에 맞춰 여섯 가지 learning-and-control paradigm으로 재분류한다.

여섯 paradigm은 perception-guided heuristic, goal-conditioned manipulation policy, predictive/model-based state representation, reward-driven RL over primitive actions, demonstration-driven skill transfer, LLM-based planning이다. 논문은 데이터, Sim2Real, 플랫폼, primitive action, 평가 지표, failure mode도 함께 비교한다.

## Evidence Notes

- 대상 논문은 41편이며, manipulation task는 unfolding/folding에 집중한다.
- Simulation 데이터가 많이 쓰이지만 cloth 물성, 시각 다양성, dynamics mismatch, unmodeled interaction 때문에 Sim2Real gap이 핵심 병목으로 정리된다.
- Folding은 success metric 정의가 논문마다 달라 표준 지표 부재가 문제로 지적된다.
- LLM-based planning은 고수준 primitive 선택에는 유용하지만 latency와 low-level control 연결이 아직 약한 방향으로 정리된다.

## Notes / Marginalia Check

PDF annotation을 확인했지만 사용자 highlight, text note, ink note는 없었고 `/Link` annotation만 존재했다. 따라서 별도 필기에서 유래한 질문은 없으며, 본문 discussion과 future opportunities에서 재사용 가치가 큰 질문을 승격했다.

## Created / Updated

- [[2026 - Deep Learning-Based Robotic Cloth Manipulation Applications]]
- [[Robotic Cloth Manipulation]]
- [[Cloth Manipulation Learning Paradigms]]
- [[2026-06-15 - What Blocks General Robotic Cloth Manipulation]]
