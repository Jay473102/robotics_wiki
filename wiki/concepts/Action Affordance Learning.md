---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - affordance
  - manipulation
  - policy-learning
sources:
  - raw/papers/2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects.pdf
---

# Action Affordance Learning

## Definition

Action affordance learning은 observation의 각 위치나 영역이 특정 행동을 성공시킬 가능성을 예측하는 방식이다. 로봇 조작에서는 grasp, push, pull, place 같은 action의 위치와 방향을 heatmap이나 score map으로 표현하는 경우가 많다.

## Why It Matters

Affordance map은 perception과 action selection을 직접 연결한다. 특히 cluttered manipulation에서는 물체별 pose를 완전히 복원하지 않아도 "어디를 잡거나 밀면 되는가"를 선택할 수 있다.

## Key Ideas

- Pixel-wise action score를 예측한다.
- 방향은 입력 이미지를 여러 각도로 회전하거나 action channel을 나누어 encode할 수 있다.
- Grasp-only가 아니라 pick/drop/pull처럼 여러 primitive 사이의 선택에도 사용할 수 있다.
- Self-supervised simulation data와 결합하면 manual labeling 부담을 줄일 수 있다.

## Related Papers

- [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]]

## Related Concepts

- [[Object Singulation]]
- [[Vision-Language-Action Models]]

## Open Questions

- Affordance map 기반 정책은 long-horizon task planning과 어떻게 결합하는 것이 좋은가?
