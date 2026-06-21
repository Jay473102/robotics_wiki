---
type: entity
status: draft
created: 2026-06-21
updated: 2026-06-21
tags:
  - company
  - robot-foundation-models
  - vla
sources:
  - raw/papers/2025 - pi0.6 a VLA That Learns From Experience.pdf
  - raw/papers/2026 - pi0.7 Steerable Generalist Robotic Foundation Model.pdf
entity_type: company
---

# Physical Intelligence

## Snapshot

Physical Intelligence는 $\pi_{0.6}$, $\pi^*_{0.6}$, $\pi_{0.7}$ 계열 VLA/robot foundation model 논문을 발표한 조직으로, generalist robotic manipulation과 real-world deployment learning을 중심 주제로 삼는다.

## Product / Platform

- $\pi^*_{0.6}$: RECAP을 통해 real-world reward feedback, autonomous rollout, intervention data로 개선되는 VLA.
- $\pi_{0.7}$: rich context conditioning과 diverse robot/non-robot data를 활용하는 steerable generalist robotic foundation model.

## Technical Claims

- $\pi^*_{0.6}$는 laundry, espresso, box assembly hard task에서 throughput을 두 배 이상 개선하고 failure를 약 절반으로 줄였다고 보고된다.
- $\pi_{0.7}$은 task-specific post-training 없이 out-of-the-box dexterity, instruction generalization, cross-embodiment transfer, compositional task generalization을 보인다고 주장된다.

## Evidence

- [[2025 - pi0.6 a VLA That Learns From Experience]]
- [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]

## Market / Deployment

논문은 real homes, office espresso machine, factory packaging-style box assembly, 여러 robot platform을 언급한다. 다만 상용 제품 범위, 고객 배포 규모, model/data 공개 여부는 원 PDF만으로 확정하기 어렵다.

## Related Entities

- [[Robot Foundation Models]]
- [[Vision-Language-Action Models]]
- [[Context-Conditioned Robot Foundation Models]]

## Open Questions

- Physical Intelligence의 모델/데이터/SDK 공개 범위는 어디까지인가?
- 논문 속 long-horizon task 성능이 반복 가능한 독립 benchmark에서도 유지되는가?
- Deployment safety, remote intervention, failure logging pipeline은 어떻게 운영되는가?
