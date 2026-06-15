---
type: method
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - bin-picking
  - manipulation
  - object-singulation
sources:
  - raw/papers/2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects.pdf
---

# Tangled-Prone Bin Picking

## Summary

Tangled-prone bin picking은 무작위로 쌓인 물체가 서로 얽히는 상황을 다루는 산업용 picking 문제다. 단일 물체를 집는 grasp planning만으로는 부족하고, 얽힌 물체를 분리하는 [[Object Singulation]] 전략이 필요하다.

## Basic Workflow

1. Depth image나 RGB-D observation에서 isolated object 후보를 찾는다.
2. isolated object가 있으면 collision-free grasp로 goal bin에 옮긴다.
3. 모두 얽혀 있으면 buffer bin, dropping, pulling 같은 분리 primitive를 실행한다.
4. 분리 후 다시 perception을 수행하고 picking을 반복한다.

## Representative Paper

- [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]]: `PickNet`과 `PullNet`으로 pick/drop/pull을 선택하는 계층형 policy를 제안한다.

## Implementation Notes

- Top-down depth image는 단순하고 빠르지만 occlusion과 missing geometry에 취약하다.
- 얽힘은 접촉과 기하가 결합된 현상이라 simulation-real gap이 크다.
- Buffer bin은 dense clutter에서 직접 pulling하지 않고 얽힘 정도를 낮추는 실용적 engineering trick으로 볼 수 있다.

## Open Questions

- 얽힘 상태를 vision-only로 판단할 수 있는 한계는 어디까지인가?
- force/torque, tactile sensing, wrist camera를 결합하면 어떤 failure mode가 줄어드는가?
