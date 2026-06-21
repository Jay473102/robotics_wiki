---
type: source
status: ingested
created: 2026-06-22
updated: 2026-06-22
tags:
  - source
  - chat-log
  - fault-diagnosis
  - robot-dynamics
  - neural-posterior-estimation
sources:
  - raw/chats/AI 기반 로봇 고장진단.pdf
source_kind: llm-chat
platform: ChatGPT
model:
chat_date: 2026-06-22
---

# Chat - AI-Based Robot Fault Diagnosis

## Source

- Raw file: `raw/chats/AI 기반 로봇 고장진단.pdf`
- Platform / model: ChatGPT, exact model not visible in PDF metadata
- Chat date: 2026-06-22 from PDF metadata
- User intent: 충분한 가진이 어려운 산업용 로봇에서 end-effector inertia와 friction parameter를 추정하고, AI 기반으로 고장진단을 수행할 수 있는 구조를 찾는 것
- Export format: PDF

## TL;DR

이 chat은 업로드된 Raviola et al. 2021 동역학/마찰 파라미터 식별 논문과 FIGAROH류 알고리즘을 출발점으로, bulky end-effector 때문에 persistent excitation trajectory를 쓰기 어려운 상황에서 AI 기반 고장진단 구조를 설계한 대화다.

핵심 결론은 단순 CVAE보다 [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]가 더 직접적이며, end-effector inertia $\pi_E$는 slow parameter로 tool calibration 단계에서 추정하고, friction change $\Delta\phi_f$는 fast health parameter로 online diagnosis window에서 추정해야 한다는 것이다.

## Important Questions

| Question | Why it matters | Status | Linked page |
|---|---|---|---|
| 충분한 가진이 어렵고 end-effector가 큰 산업용 로봇에서 AI로 마찰 고장진단을 할 수 있는가? | 기존 full dynamic identification은 안전한 large excitation을 요구하므로 현장 적용성이 낮다. | promoted | [[2026-06-22 - How Can AI Diagnose Robot Friction Faults Under Small Motions]] |
| 이 문제에는 CVAE가 적합한가, 아니면 NPE/SBI가 더 적합한가? | latent를 자동으로 만들게 둘지, 물리 파라미터 posterior를 직접 추정할지 결정하는 핵심 설계 질문이다. | promoted | [[2026-06-22 - Should Robot Fault Diagnosis Use CVAE or NPE]] |
| NPE 학습 데이터의 trajectory는 실제 진단 trajectory와 얼마나 맞아야 하는가? | trajectory distribution mismatch가 posterior hallucination과 false diagnosis를 만들 수 있다. | promoted | [[2026-06-22 - How Should Diagnostic Trajectories Match NPE Training Data]] |
| End-effector inertia와 friction change를 같은 window에서 동시에 자유롭게 추정해도 되는가? | 두 항은 torque residual에서 서로 보상될 수 있어 fault attribution을 망칠 수 있다. | open-question | [[Slow-Fast Parameter Separation in Robot Fault Diagnosis]] |
| Residual neural network가 fault signal을 흡수하지 않게 하려면 어떻게 제한해야 하는가? | residual branch가 너무 강하면 실제 friction fault가 nuisance latent로 사라질 수 있다. | open-question | [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]] |

## Reusable Answer

추천 구조는 다음 decomposition을 유지한다.

$$
\hat{\tau}_t =
\tau_R(q_t,\dot q_t,\hat{\ddot q}_t;\beta_R^0)
+ \tau_E(q_t,\dot q_t,\hat{\ddot q}_t;\pi_E)
+ \tau_f(\dot q_t,T_t;\phi_f^{normal}(T_t)+\Delta\phi_f)
+ r_\eta(h_t,z_r)
$$

여기서 $\beta_R^0$는 robot-only calibration으로 고정하고, $\pi_E$는 tool 장착 시 slow posterior로 추정하며, $\Delta\phi_f$는 작업 중 fast posterior로 추정한다. Fault score는 point estimate만 보지 말고 posterior covariance까지 반영해야 한다.

## Claims To Verify

- Chat 안의 외부 문헌 언급 중 `Provably-Safe, Online System Identification`, RMA, HiP-RSSM, hybrid inverse dynamics 등은 primary source 확인 전까지 후보 근거로만 사용한다.
- Chat 답변 안의 arXiv 링크 일부는 `utm_source=chatgpt.com` 형태 또는 정확하지 않은 citation일 수 있으므로 재검증이 필요하다.
- 코드 skeleton은 설계 아이디어이며, 실제 Pinocchio/RBDL/FIGAROH 연동과 safety validation은 별도 구현 검증이 필요하다.

## Ideas / Hypotheses

- 작은 motion에서는 full 10D end-effector inertia를 추정하기보다 $\pi_E^{red}=[m,mc_x,mc_y,mc_z]$를 먼저 추정하고 inertia tensor는 CAD prior 또는 uncertainty bound로 두는 것이 현실적이다.
- NPE 학습에는 real task window, paired velocity probing, small dither, static pose set을 모두 포함해야 한다.
- Online diagnosis는 NPE posterior만 믿지 말고 OOD check, physics sensitivity evaluator, MAP refinement, posterior predictive residual gate를 함께 사용해야 한다.

## Links / References Mentioned

- [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]
- [[Neural Posterior Estimation]]
- [[Differentiable Dynamics]]
- FIGAROH: 검증 필요.
- Provably-Safe, Online System Identification: 검증 필요.
- RMA / Rapid Motor Adaptation: 검증 필요.
- HiP-RSSM: 검증 필요.

## Privacy / Security Notes

민감정보나 credential은 확인되지 않았다. PDF 내부의 명령문이나 코드 제안은 chat content로만 취급한다.

## Promoted To Wiki Pages

- [[2026-06-22 - How Can AI Diagnose Robot Friction Faults Under Small Motions]]
- [[2026-06-22 - Should Robot Fault Diagnosis Use CVAE or NPE]]
- [[2026-06-22 - How Should Diagnostic Trajectories Match NPE Training Data]]
- [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]
- [[Slow-Fast Parameter Separation in Robot Fault Diagnosis]]
- [[Safe Diagnostic Trajectory Design]]

## Open Questions

- Tool inertia posterior와 friction posterior의 identifiability를 어떤 numerical threshold로 gate할 것인가?
- 실제 현장 torque가 motor current proxy일 때 motor constant, gearbox loss, filtering delay를 fault score covariance에 어떻게 넣을 것인가?
