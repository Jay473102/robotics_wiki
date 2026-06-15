---
type: source
status: ingested
created: 2026-06-15
updated: 2026-06-15
tags:
  - source
  - paper
  - robot-dynamics
  - parameter-identification
  - friction
sources:
  - raw/papers/2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification.pdf
---

# Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification Source

## Source

- Raw file: `raw/papers/2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification.pdf`
- Title: "Effects of Temperature and Mounting Configuration on the Dynamic Parameters Identification of Industrial Robots"
- Authors: Andrea Raviola, Roberto Guida, Andrea De Martin, Stefano Pastorelli, Stefano Mauro, Massimo Sorli
- Venue: Robotics 2021, 10, 83
- DOI: `10.3390/robotics10030083`
- Published: 2021-06-29

## Extraction Summary

이 논문은 UR3와 UR5 협동로봇에서 동역학 base parameter를 식별하고, temperature와 mounting configuration이 torque estimation에 미치는 영향을 분석한다.

핵심 결과는 제조사 제공 정보만 쓸 때보다 torque estimation normalized error가 약 90% 감소했다는 점, joint temperature 상승에 따라 viscous friction coefficient가 UR3 약 20%, UR5 약 17% 감소했다는 점, mounting configuration에 따라 필요한 base dynamic parameter 수가 달라진다는 점이다.

## Created / Updated

- [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]
- [[Robot Dynamics Parameter Identification]]
- [[Temperature-Friction Baseline]]
