---
type: paper
status: superseded
created: 2026-06-15
updated: 2026-06-15
tags:
  - unverified-reference
  - robot-dynamics
  - parameter-identification
  - friction
sources:
  - raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md
title: Raviola et al. dynamic parameter identification reference
authors:
year:
venue:
doi:
url:
---

# Unverified - Raviola Dynamic Parameter Identification Reference

## Status

이전 ingest에서 미검증으로 남겨둔 reference다. 이후 `raw/papers/robotics-10-00083-v3.pdf`가 추가되어 [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]로 확인되었다. 앞으로는 새 paper page를 primary reference로 사용한다.

## Claims In The Note

- Regressor를 $Y_{id}$, $Y_c$, $Y_v$, $Y_{I,m}$ block으로 구성.
- Coulomb friction은 $\tanh(\dot q / 0.001)$ 형태로 근사.
- Viscous friction은 $\dot q$, motor inertia는 $\ddot q$에 대응.
- SVD/QR decomposition으로 identifiable base dynamic parameter를 선택.
- 5차 Finite Fourier Series 기반 excitation trajectory를 설계하고 regressor condition number를 최적화.
- UR3/UR5에서 temperature rise에 따른 viscous friction coefficient 감소 trend를 관찰.
- Tool 장착 시 dynamic parameter update 필요성을 언급.

## How To Use

이 페이지의 내용은 verified literature claim으로 쓰면 안 된다. 정확한 paper PDF, title, DOI, venue를 확보한 뒤 paper page로 승격해야 한다.

## Related

- [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]
- [[Robot Dynamics Parameter Identification]]
- [[Temperature-Friction Baseline]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
