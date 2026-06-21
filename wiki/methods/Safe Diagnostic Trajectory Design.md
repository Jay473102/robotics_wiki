---
type: method
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - method
  - trajectory-design
  - fault-diagnosis
  - robot-dynamics
  - safety
sources:
  - raw/chats/AI 기반 로봇 고장진단.pdf
---

# Safe Diagnostic Trajectory Design

## Summary

Safe diagnostic trajectory design은 bulky tool이나 좁은 작업공간 때문에 full persistent excitation trajectory를 수행할 수 없을 때, friction과 reduced end-effector inertia를 식별하는 데 필요한 최소 motion family를 안전 제약 안에서 설계하는 방법이다.

## Trajectory Families

학습 및 진단에 포함할 trajectory family:

- Static pose set: gravity torque로 $m,mc_x,mc_y,mc_z$를 관찰한다.
- Small local dither: 충돌 없는 작은 진폭으로 local sensitivity를 얻는다.
- Paired velocity probing: $+\dot q$와 $-\dot q$ plateau를 만들어 Coulomb friction sign effect를 분리한다.
- Multi-level velocity plateau: viscous friction slope를 보기 위해 두 개 이상의 velocity level을 둔다.
- Task-like passive window: 실제 작업 중 passive monitoring에 사용할 distribution을 포함한다.

## Safety Constraints

- Joint limit, velocity limit, acceleration limit.
- TCP sweep bound.
- Tool/fixture collision avoidance.
- Torque/current bound.
- Production task interruption budget.

## Evaluation Metrics

진단 trajectory는 단순히 "많이 흔드는" 것이 아니라 다음을 만족해야 한다.

- Friction sensitivity가 충분한가?
- End-effector inertia leakage가 작거나 covariance에 반영되는가?
- Observation matrix 또는 local Fisher information이 ill-conditioned하지 않은가?
- NPE training trajectory family 안에 들어오는가?
- Posterior predictive residual이 nominal range 안에 있는가?

## NPE Integration

[[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]에서는 학습 셋이 실제 diagnosis trajectory family를 포함해야 한다. 따라서 active diagnostic cycle을 쓸 경우, 실제로 실행할 safe probing generator를 simulation data generation에도 그대로 넣어야 한다.

## Failure Modes

- 작업 trajectory와 diagnostic trajectory를 섞어 학습했지만 inference에서 trajectory mode metadata를 주지 않으면 posterior가 mode ambiguity를 가질 수 있다.
- Turnaround 구간을 plateau와 함께 쓰면 acceleration/viscous/Coulomb effects가 섞일 수 있다.
- Safety envelope가 너무 좁으면 "insufficient excitation" 상태를 정상/고장으로 오판할 수 있다.

## Related

- [[2026-06-22 - How Should Diagnostic Trajectories Match NPE Training Data]]
- [[Slow-Fast Parameter Separation in Robot Fault Diagnosis]]
- [[Robot Dynamics Parameter Identification]]
