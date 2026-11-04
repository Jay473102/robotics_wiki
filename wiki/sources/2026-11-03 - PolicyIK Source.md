---
type: source
status: ingested
created: 2026-11-05
updated: 2026-11-05
tags: [source, reinforcement-learning, manipulation, robot-learning]
sources:
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
  - https://arxiv.org/abs/2611.05372v1
  - https://tinaliu0123.github.io/PolicyIK/
  - https://github.com/Tinaliu0123/PolicyIK/tree/3459223d3cd523c9e35875f6567787ff0ffe9788
---

# PolicyIK Source

PolicyIK는 목표 pose로 이동한 뒤 정밀하게 유지하는 관절 reference 제어기를 RL로 학습한다. 시뮬레이션의 단일 시도·재시도 결과와 실물의 reaching·holding 결과를 분리해야 하며, encoder와 FK 기반 실물 오차는 외부 계측으로 확인한 절대 정확도가 아니다.

## Source

- 제목: *PolicyIK: High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning*.
- 저자: Yuhan Liu, Xinqi Liu, Zixuan Dong, Keith W. Ross, Shenji Wan. 첫 세 저자는 equal contribution; New York University / New York University Abu Dhabi.
- 발행: arXiv:2611.05372v1, 2026-11-03. 2026-11-05 확인 시 v1만 등재되어 있다. Venue는 preprint로 기록한다.
- DOI: `10.48550/arXiv.2611.05372`.
- 원본: `raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf`.
- 수집: 사용자 PDF 링크에서 [버전을 고정한 v1 PDF](https://arxiv.org/pdf/2611.05372v1)를 다운로드했다. 29쪽, 2,624,485 bytes. 원본 바이트를 수정하지 않았다.
- SHA-256: `3606c4fc9f9a972d29484992650f79e53ec4d02221451cc6f779baed3ae74626`.
- Evidence tier: **A** — 저자 논문·공식 프로젝트·공식 코드 문서. 성능은 저자 보고이며 독립 재현 결과가 아니다.
- 구현: [공식 repository](https://github.com/Tinaliu0123/PolicyIK), 확인한 main commit `3459223d3cd523c9e35875f6567787ff0ffe9788`. [README](https://github.com/Tinaliu0123/PolicyIK/blob/3459223d3cd523c9e35875f6567787ff0ffe9788/README.md)와 [hardware README](https://github.com/Tinaliu0123/PolicyIK/blob/3459223d3cd523c9e35875f6567787ff0ffe9788/hardware/README.md)를 읽었다. 학습·평가 코드 실행, checkpoint 검증, 실물 재현은 수행하지 않았다.

## Key Content

| 원문 위치 | 확인한 내용 | 해석 경계 |
|---|---|---|
| §4.1–4.3, Eqs. (2)–(7) | 누적 reference, command-state feedback, coarse/fine pose, 오차별 gain, tracking·progress·dwell reward | 기하학적 IK map의 근사만이 아니며 총 보상은 dense |
| §5.1, Table 1, Appendix C | 단일 시도 strict 93.49%, 재시도 포함 98.92% | 동일 시간·시도 수의 비교가 아님; strict는 마지막 1초 평균 오차 기준 |
| §5.1.3, Table 2, Appendix G | 고정 pi0.5-LIBERO의 controller 교체: 95.7% | side-mounted OpenArm용 재학습; hand-tuned DLS는 96.7% |
| §5.2, Table 3, Appendices H–I | 실물 OpenArm 60과제, 25초에서 reached 54/60, held 43/60 | 직접 실물 학습; encoder+FK 측정; baseline 실행 제약이 완전히 같지 않음 |
| Appendix H, hardware README | FlashSAC+HER, near-goal/reverse curriculum, latent-alignment critic, scripted demonstration replay | demonstration-free PPO 또는 그대로의 sim-to-real 결과가 아님 |
| Appendix J, Table 13 | 별도 xArm7 정책의 standard·large-rotation 각각 60/60 | 로봇별 재학습; standard에서는 DLS/QP/MPC도 60/60 |

## Notes / Marginalia Check

- 사용자가 필기한 파일이 아니라 공개 arXiv 원본을 수집했다.
- 압축 객체 stream 10개를 포함해 annotation subtype을 확인했다. `/Link` 371개를 찾았고 `/Text`, `/Highlight`, `/Ink`, `/FreeText`, `/Underline` 등 필기·강조 subtype은 발견하지 못했다. Flattened annotation의 부재까지 보증하는 검사는 아니다.
- PDF 텍스트를 추출하고 Table 1·Figure 3 페이지를 렌더링해 확인했다. 링크 annotation은 사용자 메모로 취급하지 않았다.

## Claims To Verify

- 외부 tracker, tool calibration, payload·온도·장기 drift 조건에서 실제 Cartesian 정확도를 별도 확인해야 한다.
- OpenArm 실물 seed 간 분산과 더 넓은 goal/workspace 분포에 대한 일반화는 이 요약의 확인 범위를 넘는다.
- 공식 구현 공개와 재현 성공은 별개다. 0.035 ms actor forward 시간도 FK·통신·하위 제어를 포함한 loop latency가 아니다 (§5.1.1).

## Promoted To Wiki Pages

- [[index]] — 원자료와 파생 문서의 카탈로그.
- [[2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning]] — 논문 방법·결과·평가 범위.
- [[PolicyIK Joint-Reference Control]] — 관측·reference·보상·학습 절차.
- [[Learned Closed-Loop Inverse Kinematics]] — 실행 dynamics와 command state를 포함하는 학습형 pose 제어.
- [[2026-11-05 - How Should Pose Reaching and Holding Be Evaluated]] — 오차 통계·holding window·시간·재시도·계측의 분리.

## Open Questions

- 같은 총 실행 시간과 retry budget에서도 baseline 대비 이점이 유지되는가?
- FK 모델의 오차와 실제 tool pose 오차를 나눠 측정하면 어떤 한계가 드러나는가?
