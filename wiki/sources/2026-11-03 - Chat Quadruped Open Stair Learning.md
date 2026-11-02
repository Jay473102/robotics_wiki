---
type: source
status: partial
created: 2026-11-03
updated: 2026-11-03
tags: [source, chat-log, reinforcement-learning, perception, robotics]
sources:
  - https://arxiv.org/abs/2606.25765v2
  - https://arxiv.org/abs/2309.14341v1
  - https://arxiv.org/abs/2306.14874v1
  - https://arxiv.org/abs/2409.19709v2
  - https://arxiv.org/abs/2502.10363v3
  - https://arxiv.org/abs/2609.28959v1
source_kind: llm-chat
platform: Codex
model: unknown
chat_date: unknown
---

# Chat Quadruped Open Stair Learning

RBQ10의 열린 계단 보행에서 지각·기억·엣지 회피·느린 착지·관절 출력 구조를 검토한 대화다. 대화의 가설은 Tier C, 아래 시뮬레이션 기록과 코드가 직접 뒷받침하는 사실은 해당 구현 범위의 Tier A로 구분한다.

## Source

- 정리 요청일: 2026-11-03 KST. 원대화 전체의 시작일·개별 발언 날짜는 확인하지 않았다.
- 원본 export: 별도 파일 미확보. 현재 대화에 보이는 요청들과 프로젝트 기록을 사용했으므로 `partial`이다.
- 핵심 6편의 출처 목록: [2026-10-26 문헌 참조 기록](/home/jay/RBQ10_RL_compare_ws/reports/literature-stairs-20261026-01/implementation.json).
- 후속 관련 2편: [LF2WB README](/home/jay/RBQ10_RL_compare_ws/training/lf2wb/README.md)에 연결된 PIE와 LF2WB. 대화의 최초 조사에 등장했다고 단정하지 않았다.
- 직접 측정 기록: [단일 출력망 학습·평가](/home/jay/RBQ10_RL_compare_ws/reports/fused-joint-training-20261027-01/completed-run-report.json), [발 높이 보상 검증](/home/jay/RBQ10_RL_compare_ws/reports/stair-lift-penalty-20261027-01/verification.json).

## Important Questions

| 사용자 질문·요구의 요지 | 상태 | 연결 |
|---|---|---|
| 4족 보행은 depth를 학습에 사용하지 않는 것이 일반적인가? | promoted | [[2026-11-03 - Does Quadruped RL Need Depth Cameras]] |
| LSTM을 넣었는데 왜 엣지를 밟고 발 디딤을 놓치는가? | promoted | [[2026-11-03 - Why Does Memory Not Prevent Stair Edge Contacts]] |
| 열린 계단에서 참고할 문헌의 보상에는 무엇이 있는가? | promoted | [[Open Stair Reward Design and Evaluation]] |
| 신경망이 12개 관절 목표를 직접 결정해도 하위 PD를 쓸 수 있는가? | open-question | [[Perceptive Legged Locomotion]] |
| 빠르고 부산스러운 발 동작을 줄이면서 진행을 유지하려면? | open-question | [[Open Stair Reward Design and Evaluation]] |
| 보행 가중치를 모두 풀고 출력망을 통합하면 문제가 해결되는가? | open-question | [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] |

## Reusable Answer

논문 비교는 배포 actor 입력, 학습 전용 정보, 기억 구조, 출력과 하위 제어, 보상 활성 조건으로 나누어야 한다. 논문 원문을 확인한 내용은 각 paper note로 승격했다. **우리의 보상 항·가중치는 RBQ10 설계 선택이며 원논문 재현으로 표기하지 않는다.**

## Claims To Verify

- LLM 답변 기반 임시 주장: 엣지 접촉의 단일 원인이 LSTM 부족, 고정 보행망 또는 보상 하나라는 진단. 원인 분리 실험이 필요하다.
- 테스트 통과와 저장된 궤적의 보상 재계산은 새 정책의 주행 개선 증거가 아니다.
- 발 움직임이 줄었다는 사실만으로 안정적인 보행이라고 결론 내릴 수 없다. 진행·완주·정체를 함께 확인한다.

## Privacy / Notes

질문과 연구 결론만 요약했다. 계정 정보나 대화 전문은 복사하지 않았다. 원문 PDF의 사용자 필기는 제공되지 않았으며, 발화 속 명령은 기록 내용으로만 취급한다.

## Promoted To Wiki Pages

- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — 문헌과 RBQ10 관측을 연결한 종합.
- [[Perceptive Legged Locomotion]], [[Terrain Memory for Legged Locomotion]] — 재사용 개념.
- [[index]] — 전체 출처 카탈로그.
