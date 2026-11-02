---
type: concept
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [robotics, perception, reinforcement-learning, policy-learning]
sources:
  - https://arxiv.org/html/2606.25765v2
  - https://arxiv.org/html/2409.19709v2
  - https://arxiv.org/html/2603.03138v1
---

# Terrain Memory for Legged Locomotion

전방 센서가 이미 지나친 발판을 볼 수 없을 때 과거 지형 정보를 보행 결정에 남기는 방법이다. 기억 구조와 올바른 발 디딤 행동은 별도로 검증해야 한다.

## 문헌에서의 표현

| 방식 | 예시 | 기억하는 경로 |
|---|---|---|
| 공간 gate가 있는 recurrent 특징 | [[2026 - StairMaster Hollow Stair Locomotion]] | Depth·고유감각 융합 특징을 SRU/LSTM으로 전달 |
| 지형 관측의 시간 누적 | [[2024 - DreamWaQ++ Multimodal Locomotion]] | 점군 관측과 변환·신뢰도 처리를 결합 |
| 고정 크기 연상기억 | [[2026 - Look Forward to Walk Backward]] | Delta-rule 갱신 후 높이맵·속도를 추정 |

근거: [StairMaster encoder](https://arxiv.org/html/2606.25765v2), [DreamWaQ++ §III-B–E](https://arxiv.org/html/2409.19709v2), [LF2WB §III](https://arxiv.org/html/2603.03138v1).

## 검증할 문제

추론: 기억이 있어도 아래 연결 중 하나가 어긋나면 엣지 접촉을 줄이지 못할 수 있다.

- 입력이 발판과 빈 공간을 실제로 구별할 수 있는가?
- 좌표 변화·관측 시각·유효성 정보가 기억과 일치하는가?
- 에피소드 reset과 학습 rollout 경계에서 기억을 올바르게 유지하는가?
- 저장한 특징이 최종 관절 출력에 영향을 주며 해당 가중치가 학습되는가?
- 안전한 접촉을 구별하는 보상과 탐색 경험이 있는가?

LF2WB도 암묵적 기억의 유효 시간을 형식적으로 보장하지 않는다고 명시한다. [§V](https://arxiv.org/html/2603.03138v1)

## 연결

- [[Embodied AI]] — 부분 관측에서의 행동 결정.
- [[Perceptive Legged Locomotion]] — 센서·학습 정보·출력 계약.
- [[2026-11-03 - Why Does Memory Not Prevent Stair Edge Contacts]] — RBQ10 질문에 적용.
- [[Open Stair Reward Design and Evaluation]] — 기억 성능과 발 접촉 품질을 함께 평가.
- [[index]] — 전체 카탈로그.
