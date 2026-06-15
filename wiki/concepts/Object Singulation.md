---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - manipulation
  - bin-picking
  - object-singulation
sources:
  - raw/papers/2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects.pdf
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

## Related Concepts

- [[Action Affordance Learning]]
- [[Tangled-Prone Bin Picking]]

## Open Questions

- Singulation metric은 단일 object transport success, cycle time, downstream error 중 무엇을 중심으로 잡아야 하는가?
