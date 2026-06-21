---
type: question
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - question
  - trajectory-design
  - neural-posterior-estimation
  - fault-diagnosis
sources:
  - raw/chats/AI 기반 로봇 고장진단.pdf
---

# How Should Diagnostic Trajectories Match NPE Training Data?

## Short Answer

NPE가 학습 때와 완전히 같은 trajectory를 볼 필요는 없지만, 실제 diagnosis에 사용할 trajectory family는 학습 셋에 들어가야 한다. 중요한 것은 동일한 궤적이 아니라 동일한 분포와 식별 정보 구조다.

## Why This Question Matters

NPE는 window $D=\{q,\dot q,\tau,T\}_{1:T}$를 보고 posterior $q_\psi(\theta\mid D)$를 출력한다. 실제 trajectory가 학습 trajectory distribution 밖이면 posterior가 과신된 잘못된 값을 낼 수 있다.

## Current Answer

작업 중 passive monitoring으로 friction을 추정할 경우, 실제 작업 log에서 나온 $q,\dot q,\tau$ window를 학습 셋에 포함해야 한다. 단순 복사보다 time stretch, noise, pose offset, parameter randomization을 통해 task-family distribution을 만든다.

작업 전/후 별도 diagnostic cycle을 수행할 경우, 실제 작업 trajectory와 비슷할 필요는 작다. 대신 실제로 실행할 diagnostic probing family를 학습 셋에 넣어야 한다.

마찰 식별에는 다음 패턴이 중요하다.

- $+\dot q$와 $-\dot q$ 방향 모두 포함
- 두 개 이상의 velocity level
- plateau 구간
- turnaround 구간 제거 또는 별도 mask
- 작은 TCP sweep
- collision/torque/speed safety constraint 만족

따라서 학습 셋은 다음 mixture가 되어야 한다.

$$
D_{train}
= D_{task-like}
\cup D_{paired-velocity}
\cup D_{small-dither}
\cup D_{static-pose}
$$

실제 진단 때는 NPE만 믿지 않고 다음 gate를 함께 둔다.

- trajectory feature OOD check
- physics sensitivity evaluator
- MAP refinement
- posterior predictive residual check

## Evidence / Sources

- [[2026-06-22 - AI-Based Robot Fault Diagnosis Chat]]: trajectory family mismatch와 NPE OOD risk를 다룬 source.
- [[Safe Diagnostic Trajectory Design]]: diagnostic probing family와 safety constraint를 정리한 method page.

## Important Caveats

Passive monitoring과 active diagnostic cycle은 요구하는 training distribution이 다르다. 두 모드를 같은 NPE model로 처리하려면 trajectory mode metadata나 mixture-aware training이 필요하다.

## Linked Pages

- [[Safe Diagnostic Trajectory Design]]
- [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]
- [[Robot Dynamics Parameter Identification]]
