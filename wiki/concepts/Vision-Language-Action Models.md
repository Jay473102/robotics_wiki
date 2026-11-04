---
type: concept
status: draft
created: 2026-06-14
updated: 2026-11-05
tags:
  - vla
  - robot-foundation-models
  - robotics
sources:
  - raw/notes/deep-research-report.md
  - raw/papers/2026 - DIAL Decoupling Intent and Action via Latent World Modeling.pdf
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
---

# Vision-Language-Action Models

## Definition

Vision-Language-Action Models, 또는 VLA 모델은 시각 입력과 언어 지시를 받아 로봇 행동을 출력하는 모델 계열이다. 일반적으로 perception-language grounding과 policy learning을 하나의 모델 또는 결합된 시스템으로 다룬다.

## Why It Matters

VLA는 로봇 foundation model의 핵심 후보 중 하나다. 자연어 지시, 시각 장면 이해, 조작 행동을 연결하므로 manipulation, mobile manipulation, household robotics, 산업용 task generalization과 직접 연결된다.

## Key Issues

- Action representation: end-effector pose, joint commands, discretized tokens, continuous control.
- Data mixture: robot demonstrations, human videos, simulation, web-scale vision-language data.
- Generalization: new objects, new scenes, new instructions, new embodiments.
- Evaluation: benchmark success rate와 실제 배포 성능 사이의 차이.
- Intent-action interface: VLM의 high-level reasoning을 low-level motor control로 어떻게 전달할지. [[2026 - DIAL Decoupling Intent and Action via Latent World Modeling]]은 latent visual foresight를 differentiable bottleneck으로 쓰는 설계를 제안한다.
- Training stability: end-to-end action supervision이 VLM semantic representation을 손상시키거나 shortcut learning을 만들 수 있어, decoupled warmup이나 auxiliary world modeling이 필요할 수 있다.

## Related Concepts

- [[Embodied AI]]
- [[Physical AI]]
- [[Robot Foundation Models]]
- [[Action Affordance Learning]]
- [[Latent World Modeling]]

## Open Questions

- VLA 모델은 embodiment 차이를 어떤 방식으로 흡수할 수 있는가?
- 언어/비전 사전학습과 로봇 행동 데이터의 최적 혼합 비율은 무엇인가?
- VLM-native feature space와 robot-specific visual feature space 중 어떤 것이 control grounding에 더 안정적인가?
- Latent foresight bottleneck은 planner-policy 분리와 end-to-end VLA 사이의 일반적인 절충점이 될 수 있는가?

## Pose action과 하위 제어의 연결

[[2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning]]은 고정 pi0.5-LIBERO의 pose 명령을 [[PolicyIK Joint-Reference Control]]로 실행한다. Side-mounted OpenArm에 맞게 하위 정책을 재학습하고 공통 adapter를 사용한 변형 LIBERO-Object 10과제에서 성공률 95.7%를 보고했다. Hand-tuned DLS는 96.7%이므로 모든 baseline보다 높은 결과는 아니다 (§5.1.3, Table 2, Appendix G; Tier A).

추론: VLA가 생성한 목표의 적절성과 하위 controller의 pose 실행 정확도를 나눠 진단할 수 있다. [[Learned Closed-Loop Inverse Kinematics]]와 [[2026-11-05 - How Should Pose Reaching and Holding Be Evaluated]]는 그 실행 계층의 개념·평가 기준을 정리한다. 이 논문의 연결 실험은 simulation이며 실물 VLA task 성공으로 확대하지 않는다.
