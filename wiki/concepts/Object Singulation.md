---
type: concept
status: draft
created: 2026-06-15
updated: 2026-11-03
tags:
  - manipulation
  - bin-picking
  - object-singulation
sources:
  - raw/papers/2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects.pdf
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
---

# Object Singulation

## Definition

Object singulation은 cluttered environment에서 개별 물체 하나를 다른 물체와 분리해 grasp, inspection, packing, assembly 같은 후속 작업이 가능하도록 만드는 조작 문제다.

## Why It Matters

산업용 bin picking에서는 물체가 겹치거나 벽에 붙어 있거나 서로 얽힌다. 단순 grasp 성공률만 높이면 여러 물체가 함께 이동할 수 있으므로, 실제 자동화에서는 singulation 성공이 처리량과 품질을 좌우한다.

## Key Ideas

- Non-prehensile manipulation: pushing, dragging, sweeping.
- Prehensile separation: grasp 후 dropping, pulling, shaking, regrasp.
- Learned affordance: perception에서 어떤 위치와 방향으로 분리 행동을 할지 예측한다.
- Buffer space: 복잡한 main bin 대신 별도 공간에서 얽힘을 줄인다.

## Related Papers

- [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]]
- [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]] — 조립 완료 보상을 학습하면서 부품을 밀어 접근 가능한 위치로 옮기는 행동을 관찰한 simulation 사례 (§I, §V-C–D). 얽힌 물체 분리 성능을 평가한 논문은 아니다.

## Related Concepts

- [[Action Affordance Learning]]
- [[Tangled-Prone Bin Picking]]
- [[AlphaNIST Binary-Reward Assembly]] — 후속 조립에 유용한 중간 동작을 별도 primitive나 동작 보상으로 지정하지 않는 학습 사례.

## Open Questions

- Singulation metric은 단일 object transport success, cycle time, downstream error 중 무엇을 중심으로 잡아야 하는가?
