---
type: concept
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [robotics, perception, reinforcement-learning, policy-learning, sim-to-real]
sources:
  - https://arxiv.org/html/2606.25765v2
  - https://arxiv.org/html/2309.14341v1
  - https://arxiv.org/html/2306.14874v1
  - https://arxiv.org/html/2408.13740v3
---

# Perceptive Legged Locomotion

지형에 대한 외부 관측을 몸체·관절 상태와 결합해 발걸음을 결정하는 보행 방법이다. Depth가 policy 입력으로 직접 들어갈 수도 있고, 점군·높이맵·추정 특징으로 변환되어 들어갈 수도 있다. [StairMaster Method](https://arxiv.org/html/2606.25765v2), [ANYmal Parkour §IV-B](https://arxiv.org/html/2306.14874v1)

## 비교해야 할 네 가지 계약

| 계약 | 구분할 내용 |
|---|---|
| 배포 입력 | 고유감각만 사용하는가, 현재 depth나 센서에서 만든 지형 표현도 사용하는가 |
| 학습 정보 | actor, teacher, critic, 보상, 추정기 정답에 각각 어떤 정보를 허용하는가 |
| 기억 | observation history, recurrent state, 명시적 지도 중 무엇을 유지하는가 |
| 행동 | 관절 목표를 직접 생성하는가, 상위 정책이 하위 기술·계획기를 선택하는가 |

예를 들어 PIE의 actor는 추정치를 받지만 critic은 정답 지형·속도를 받는다. Extreme Parkour는 지형 scandots 교사에서 depth 학생으로 증류한다. 따라서 **특권 지형으로 학습했다는 설명만으로 실물에서도 정답 지형을 입력한다고 판단할 수 없다.** [PIE §III-A](https://arxiv.org/html/2408.13740v3), [Extreme Parkour §3](https://arxiv.org/html/2309.14341v1)

## 관절 목표 출력과 하위 PD

StairMaster는 신경망이 관절 목표각을 만들고 PD가 토크로 변환한다. [Experimental Setup](https://arxiv.org/html/2606.25765v2) 이는 발 디딤 위치나 보행 순서를 상위 제어기가 고르는 것과 다른 역할이다.

추론: PD를 유지해도 새 정책이 만든 목표 궤적의 전체 몸체 안정성이 자동으로 보장되지는 않는다. 단일 출력망은 행동을 생성하는 경로를 단순화하지만, 접촉·속도·정지 조건의 검증을 대신하지 않는다.

## 연결

- [[Embodied AI]], [[Physical AI]] — 지각과 행동을 물리 상호작용으로 연결하는 사례.
- [[Terrain Memory for Legged Locomotion]] — 부분 관측의 기억.
- [[2026-11-03 - Does Quadruped RL Need Depth Cameras]] — blind와 perceptive의 구분.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌별 설계 비교.
- [[index]] — 전체 카탈로그.

## 열린 질문

센서 지연·결손을 포함한 실제 배포 입력에서도 학습 중의 안전한 착지 행동이 유지되는가?
