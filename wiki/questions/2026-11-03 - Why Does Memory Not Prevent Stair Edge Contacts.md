---
type: question
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [question, robotics, perception, reinforcement-learning]
sources:
  - https://arxiv.org/html/2606.25765v2
  - https://arxiv.org/html/2309.14341v1
  - https://arxiv.org/html/2603.03138v1
---

# LSTM을 넣어도 왜 계단 엣지를 밟는가

**기억은 과거 관측을 활용하는 기능이고, 안전한 착지는 관측·행동·학습 목적이 함께 만들어야 하는 결과다.** 특정 RBQ10 실패의 원인을 이 설명만으로 확정하지는 않는다.

## 문헌 근거

StairMaster는 공간 기억과 함께 hollow·edge 비용을 둔다. Extreme Parkour는 edge 비용 제거 실험을 별도로 수행한다. LF2WB는 기억 구조를 비교하지만 유효 기억 시간의 형식적 보장을 주장하지 않는다. [StairMaster Method](https://arxiv.org/html/2606.25765v2), [Extreme Parkour §4.3](https://arxiv.org/html/2309.14341v1), [LF2WB §V](https://arxiv.org/html/2603.03138v1)

## RBQ10 진단 순서

아래는 추론에 기반한 점검 순서다.

1. 발판·엣지가 입력에 들어왔는지, 결손이나 가림으로 사라졌는지 확인한다.
2. 기억을 reset한 시점과 로봇 좌표 변화를 대조한다.
3. 기억 특징이 최종 12개 관절 출력에 전달되고 그 가중치가 갱신되는지 확인한다.
4. 발 중심·최저점·실제 접촉 위치 중 어느 위치로 엣지 비용을 계산하는지 확인한다.
5. 안전하게 이동하는 것보다 정지·제자리 발 움직임이 유리한 보상 구간이 있는지 확인한다.

단일 출력망 실험에서는 actor의 모든 가중치가 갱신됐어도 16개 평가 모두 계단 초입 timeout으로 끝났다. 따라서 가중치 해제나 출력 통합만으로 문제를 해결했다고 볼 수 없다. 이 결과는 해당 학습 조건의 관측이며 구조 자체의 불가능성을 입증하지 않는다. [2026-10-27 평가](/home/jay/RBQ10_RL_compare_ws/reports/fused-joint-training-20261027-01/completed-run-report.json)

## 연결

- [[Terrain Memory for Legged Locomotion]] — 기억 표현과 검증 축.
- [[Open Stair Reward Design and Evaluation]] — 정체와 접촉 품질의 평가.
- [[2026-11-03 - Chat Quadruped Open Stair Learning]] — 원래 질문.
- [[index]] — 전체 카탈로그.
