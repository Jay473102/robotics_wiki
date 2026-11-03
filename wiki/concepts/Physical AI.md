---
type: concept
status: draft
created: 2026-06-14
updated: 2026-11-03
tags:
  - physical-ai
  - robotics
sources:
  - raw/notes/deep-research-report.md
  - raw/papers/2026 - Deep Learning-Based Robotic Cloth Manipulation Applications.pdf
  - https://arxiv.org/html/2606.25765v2
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
---

# Physical AI

## Definition

Physical AI는 물리 세계에서 작동하는 AI 시스템을 포괄하는 개념이다. 로봇, 센서, 액추에이터, 제어, 월드 모델, 데이터 수집, 안전, 배포까지 포함하며, 소프트웨어 모델의 지능이 실제 물리 행동으로 구현되는 방식을 다룬다.

## Why It Matters

Physical AI는 연구 논문뿐 아니라 하드웨어, 제조, 운영 데이터, 규제, 비용 구조가 성능과 확산을 좌우한다. 따라서 논문 지식과 업체 동향을 같은 위키 안에서 연결할 가치가 크다.

## Related Concepts

- [[Embodied AI]]
- [[Vision-Language-Action Models]]
- [[Robot Foundation Models]]
- [[Robot Fleet Orchestration]]
- [[LG CNS PhysicalWorks]]
- [[Robotic Cloth Manipulation]]

## Open Questions

- Physical AI에서 foundation model의 스케일링 법칙은 어떤 데이터와 embodiment에 의해 제한되는가?
- 실제 상용화의 병목은 모델 성능, 데이터, 하드웨어 비용, 안전, 운영 중 어디에 있는가?
- Deformable object manipulation처럼 simulator fidelity와 metric 표준화가 약한 영역에서 Physical AI의 일반화 성능을 어떻게 평가해야 하는가?

## 보행과 센서 기반 제어

- [[Perceptive Legged Locomotion]] — 실제 센서 입력과 학습 전용 정보를 구분하는 사례.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 로봇 형태·센서·접촉 형상이 학습 결과에 미치는 영향을 검토하는 문헌 묶음.

## 접촉이 많은 조립과 학습 초기화

- [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]] — 완료 목표를 공유하는 여러 조립 과제의 simulation PPO 사례. 실물 성능은 아직 검증 대상이다.
- [[AlphaNIST Binary-Reward Assembly]] — reset 상태·sampling·제어 비용을 포함하는 학습 절차.
- [[Reset-State Curricula for Sparse-Reward RL]] — 유용한 경험을 만들기 위한 초기 상태 설계. 시범 행동을 주지 않아도 simulator·목표·초기화에 대한 사전 정보는 필요하다.
- [[NIST Assembly Task Board 1]] — 같은 보드에서도 단일 부품·여러 부품·실물이라는 평가 범위를 구분해야 한다.
