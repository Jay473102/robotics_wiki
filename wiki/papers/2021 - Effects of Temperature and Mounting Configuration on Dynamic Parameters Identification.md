---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - robot-dynamics
  - parameter-identification
  - friction
  - temperature
  - collaborative-robots
sources:
  - raw/papers/robotics-10-00083-v3.pdf
title: Effects of Temperature and Mounting Configuration on the Dynamic Parameters Identification of Industrial Robots
authors:
  - Andrea Raviola
  - Roberto Guida
  - Andrea De Martin
  - Stefano Pastorelli
  - Stefano Mauro
  - Massimo Sorli
year: 2021
venue: Robotics 10(3):83
doi: 10.3390/robotics10030083
url: https://doi.org/10.3390/robotics10030083
---

# Effects of Temperature and Mounting Configuration on the Dynamic Parameters Identification of Industrial Robots

## TL;DR

UR3/UR5의 동역학 base parameter를 LS/WLS 기반으로 식별하고, temperature와 mounting configuration이 torque estimation에 미치는 영향을 분석한 논문이다. 제조사 제공 parameter만 사용할 때 대비 torque estimation error를 약 90% 줄였고, joint temperature 상승에 따라 viscous friction coefficient가 UR3 약 20%, UR5 약 17% 감소한다고 보고한다.

## Problem

산업용 로봇 제조사는 link mass와 center of mass 일부는 제공하지만 inertia, motor inertia, Coulomb friction, viscous friction 등은 충분히 제공하지 않는 경우가 많다. 이 값이 부정확하면 torque prediction, energy optimization, safety evaluation, diagnostics/prognostics의 신뢰도가 낮아진다.

## Core Idea

동역학 방정식을 regressor form으로 쓰고, excitation trajectory를 통해 base dynamic parameter를 식별한다.

$$
\tau = Y_B(q,\dot q,\ddot q)p_B
$$

식별 후 temperature 변화와 mounting configuration 변화가 같은 모델 구조 안에서 어떻게 반영되는지 분석한다.

## Method

- UR3/UR5에 5th order Finite Fourier Series 기반 persistent excitation trajectory를 명령한다.
- TCP/IP feedback에서 joint temperature, angular position, velocity, motor current를 125 Hz로 수집한다.
- Motor current, gear ratio, torque constant로 joint torque를 계산한다.
- Least Squares와 Weighted Least Squares로 base dynamic parameter를 추정한다.
- SVD 분석으로 base dynamic parameter 수를 정한다.

## Data / Embodiment

- Robot: Universal Robots UR3, UR5.
- Additional validation: URSim digital twin에서 ceiling-mounted UR5를 검증한다.
- Mounting: base joint axis가 gravity vector와 정렬되는 경우와 그렇지 않은 경우를 구분한다.

## Evaluation

식별된 parameter로 validation trajectory의 joint torque를 예측하고 measured torque와 비교한다. Temperature effect는 동일 trajectory를 반복 수행하면서 joint temperature가 상승하는 조건에서 viscous friction coefficient 변화를 본다.

## Results

- 제조사 제공 정보만 사용하는 경우 대비 torque estimation normalized error가 약 90% 감소한다.
- Temperature 상승에 따라 viscous friction coefficient가 선형적으로 감소하는 경향을 보이며, PDF는 UR3 약 20%, UR5 약 17% 감소를 보고한다.
- Ground/ceiling처럼 mounting configuration이 바뀌면 regressor를 새 configuration에 맞게 재계산해야 한다.
- Base joint axis가 gravity vector와 정렬되지 않으면 54개 base dynamic parameter가 필요하고, ground/ceiling처럼 정렬되는 경우 52개만 관여한다고 설명한다.

## Limitations

- Temperature-friction 관계는 실험한 온도 범위에서 관찰된 것이다. 전체 Universal Robots working range인 0-50도 범위에 대한 mapping은 future work로 남긴다.
- WLS는 더 정확할 수 있지만 계산 시간이 LS보다 크게 늘어난다.
- URSim validation은 digital twin 기반이므로 실제 ceiling mount 실험과 동일하다고 볼 수는 없다.

## Connections

- [[Robot Dynamics Parameter Identification]]
- [[Temperature-Friction Baseline]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]

## Contradictions / Updates

기존 [[Unverified - Raviola Dynamic Parameter Identification Reference]] 페이지에서 미확정으로 남겨둔 Raviola reference는 이 PDF로 확인되었다. 앞으로는 이 페이지를 primary reference로 사용한다.

## Open Questions

- Temperature, wear, lubrication 상태를 분리해 friction drift를 추정하려면 어떤 실험 설계가 필요한가?
- Full excitation이 어려운 실제 생산 셀에서는 어떤 subset parameter만 안정적으로 갱신할 수 있는가?
