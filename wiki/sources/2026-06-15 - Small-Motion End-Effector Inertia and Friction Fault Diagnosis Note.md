---
type: source
status: processed
created: 2026-06-15
updated: 2026-06-15
tags:
  - source-note
  - fault-diagnosis
  - robot-dynamics
  - friction
sources:
  - raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md
---

# Small-Motion End-Effector Inertia and Friction Fault Diagnosis Note

## TL;DR

이 노트는 충분한 persistent excitation trajectory를 수행하기 어려운 산업용 로봇에서, 큰 end-effector가 달린 상태의 tool inertia와 effective friction을 작은 작업 motion만으로 추정하고, 온도에 따른 정상 마찰 변화와 실제 마찰 고장 성분을 분리하는 방법론을 제안한다.

핵심 구조는 `simulation-pretrained NPE -> differentiable dynamics MAP refinement -> real temperature-friction baseline -> uncertainty-aware fault score`다.

## Main Idea

- 기존 full dynamic parameter identification은 좋은 condition number를 갖는 excitation trajectory가 필요하다.
- 산업 현장에서는 bulky end-effector, 충돌 위험, 제한된 작업 공간 때문에 그런 trajectory를 반복 수행하기 어렵다.
- 따라서 robot body parameter는 사전 식별값 $\beta_R^0$로 고정하고, $\pi_E$와 $\phi_f^{eff}$만 분리 추정한다.
- simulation은 temperature-friction 관계를 배우는 데 쓰지 않고, $q,\dot q,\tau \rightarrow \pi_E,\phi_f^{eff}$ posterior estimator를 학습하는 데 쓴다.
- 정상 온도-마찰 baseline $g^{real}(T)$는 실제 정상 warm-up 데이터로만 구축한다.
- 최종 고장 feature는 $\Delta\phi_f^{fault} = \phi_f^{eff} - g^{real}(T)$로 정의한다.

## Extracted References

- [[2020 - The Frontier of Simulation-Based Inference]]
- [[2019 - Automatic Posterior Transformation for Likelihood-Free Inference]]
- [[2022 - Neural Posterior Domain Randomization]]
- [[2021 - A Differentiable Newton-Euler Algorithm for Real-World Robotics]]
- [[Unverified - Raviola Dynamic Parameter Identification Reference]]

## Derived Wiki Pages

- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
- [[2026-06-15 - Small-Motion Tool Inertia and Friction Fault Diagnosis]]
- [[Simulation-Based Inference]]
- [[Neural Posterior Estimation]]
- [[Differentiable Dynamics]]
- [[Temperature-Friction Baseline]]
- [[Robot Dynamics Parameter Identification]]

## Encoding Note

The raw note's Korean body text appears mojibake in the command-line environment, but equations, English technical terms, section structure, and embedded URLs were readable enough to extract the method. If the original note is still readable in Obsidian, future refinement should use that view as the source of truth for Korean prose.
