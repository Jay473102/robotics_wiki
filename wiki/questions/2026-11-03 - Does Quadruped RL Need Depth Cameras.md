---
type: question
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [question, robotics, perception, reinforcement-learning]
sources:
  - https://arxiv.org/html/2606.25765v2
  - https://arxiv.org/html/2309.14341v1
  - https://arxiv.org/html/2408.13740v3
  - https://arxiv.org/html/2603.03138v1
---

# 4족 보행 RL은 depth 카메라를 학습에 사용하지 않는가

**그렇게 일반화할 수 없다.** 이 문헌 묶음에는 depth를 배포에도 사용하는 방법이 여럿 있다. 논문 수집 범위가 지각 기반 보행에 치우쳐 있으므로, 이 목록으로 전체 분야의 사용 빈도까지 판단하지는 않는다.

## 질문을 나누는 기준

| 확인할 위치 | 의미 |
|---|---|
| 배포 actor | 로봇이 실행 중 실제로 받는 입력 |
| 학습 teacher | 학생에게 동작을 가르치는 전문가의 입력 |
| 학습 critic | 가치 추정에만 허용한 추가 정보 |
| 보상·추정기 정답 | 행동을 평가하거나 표현을 학습시키는 정답 정보 |

StairMaster와 Extreme Parkour는 특권 지형 교사를 사용한 뒤 depth 학생을 학습한다. PIE는 단일 단계에서도 배포 가능한 actor와 특권 critic을 구분한다. LF2WB는 전방 depth로 만든 기억을 후진에 활용한다. [StairMaster](https://arxiv.org/html/2606.25765v2), [Extreme Parkour](https://arxiv.org/html/2309.14341v1), [PIE](https://arxiv.org/html/2408.13740v3), [LF2WB](https://arxiv.org/html/2603.03138v1)

## RBQ10에서의 의미

추론: "depth를 쓴다"보다 카메라 영상→유효성·시각 정보→지형 표현→기억→관절 출력의 실제 경로를 확인하는 것이 중요하다. 정답 높이맵을 critic이나 보상에 사용하는 것과 배포 actor에 넣는 것은 서로 다른 설정이다. 이 구분이 사용자가 정한 센서 입력 제한을 자동으로 바꾸지는 않는다.

## 연결

- [[Perceptive Legged Locomotion]] — 입력·출력 계약.
- [[2026-11-03 - Chat Quadruped Open Stair Learning]] — 원래 질문.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 논문 비교표.
- [[index]] — 전체 카탈로그.
