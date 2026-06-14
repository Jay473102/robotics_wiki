---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - cloth-manipulation
  - deformable-object-manipulation
  - manipulation
sources:
  - raw/papers/frobt-13-1752914.pdf
---

# Robotic Cloth Manipulation

## Definition

Robotic cloth manipulation은 수건, 천, 의류처럼 deformable한 물체를 로봇이 인식하고 펼치고 접고 정렬하고 이동하는 조작 문제다. 대표 task는 cloth unfolding, folding, smoothing, dressing, ironing, sewing이다.

## Why It Matters

Cloth는 self-occlusion, wrinkle, topology 변화, 복잡한 contact dynamics 때문에 Physical AI의 좋은 stress test다. Household robot, laundry automation, apparel logistics, manufacturing, assistive robotics와 직접 연결된다.

## Key Ideas

- State representation: keypoint, contour, dense correspondence, particle/graph state, latent visual state.
- Primitive action: pick-and-place, drag, mop, fling, air blowing, tactile-guided sliding.
- Data: simulation, real robot interaction, teleoperation, human video, UV/color labels.
- Evaluation: unfolded coverage, action count, folding success rate, goal similarity, failure mode breakdown.
- Sensing: RGB-D가 주류이나 tactile/force/proprioception이 occlusion과 multi-layer grasping 문제를 보강할 수 있다.

## Related Papers

- [[2026 - Deep Learning-Based Robotic Cloth Manipulation Applications]]

## Related Concepts

- [[Cloth Manipulation Learning Paradigms]]
- [[Action Affordance Learning]]
- [[Physical AI]]

## Open Questions

- Deformable object에서 일반화의 단위는 garment category, material, topology, task goal 중 무엇인가?
- Cloth manipulation policy는 primitive hierarchy를 명시적으로 가져야 하는가, 아니면 end-to-end action chunk로 충분한가?
- Real-world 데이터 수집 비용을 줄이기 위해 human video와 teleoperation을 어떻게 결합해야 하는가?
