---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, robotics, sim-to-real]
sources:
  - https://arxiv.org/abs/2603.03138v1
  - https://arxiv.org/html/2603.03138v1
title: "Look Forward to Walk Backward: Efficient Terrain Memory for Backward Locomotion with Forward Vision"
authors: [Shixin Luo, Songbo Li, Yuan Hao, Yaqi Wang, Jun Zheng, Jun Wu, Qiuguo Zhu]
year: 2026
venue: ICRA 2026; accepted according to arXiv metadata
doi: 10.48550/arXiv.2603.03138
url: https://arxiv.org/abs/2603.03138v1
---

# Look Forward to Walk Backward

LF2WB는 전진하면서 본 지형을 기억해, 뒤쪽 카메라 없이 후진할 때 활용한다. **후방 시야가 없다는 뜻이지 depth를 사용하지 않는다는 뜻은 아니다.** [초록](https://arxiv.org/abs/2603.03138v1)

## 기억과 학습

전방 depth와 고유감각 특징을 DeltaNet-Transformer에 넣는다. Delta-rule 갱신으로 고정 크기의 연상기억을 유지하고, 주변 높이맵과 몸체 속도를 추정한다. Actor는 추정값을, critic은 정답 지도·속도를 사용하며 추정기와 PPO를 함께 학습한다. [§III](https://arxiv.org/html/2603.03138v1)

학습은 chunkwise 계산을 지원하고 배포는 고정 크기 상태의 recurrent 추론을 사용한다. rollout 경계를 넘는 기억 유지와 에피소드 reset 처리가 구현의 중요한 부분이다. [§III-B–D](https://arxiv.org/html/2603.03138v1)

## 평가와 한계

Lite3에서 기억 backbone을 비교하고 실제 전진·후진 장애물 통과를 보인다. 저자는 기억 유효 시간의 형식적 보장은 없으며, 단순한 상황에서도 실패할 수 있다고 명시한다. [§IV–V](https://arxiv.org/html/2603.03138v1)

## RBQ10 연결

[로컬 구현](/home/jay/RBQ10_RL_compare_ws/training/lf2wb/README.md)은 순차 recurrent 계산을 사용하고 원문의 병렬 학습 커널·전체 curriculum을 재현하지 않았다고 명시한다. 추론: 구현 존재나 초기 학습 로그를 열린 계단 완주 검증으로 해석하면 안 된다.

## 연결

- [[2026-03-03 - LF2WB Source]] — 원문과 로컬 구현 출처.
- [[2024 - PIE Implicit-Explicit Parkour]] — 추정기와 비대칭 actor-critic 비교.
- [[Terrain Memory for Legged Locomotion]] — LSTM과 연상기억의 검증 축.
- [[2026-11-03 - Why Does Memory Not Prevent Stair Edge Contacts]] — 기억과 안전한 발 디딤의 차이.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌 비교.
- [[index]] — 전체 문헌 카탈로그.
