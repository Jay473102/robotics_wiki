---
type: concept
status: draft
created: 2026-11-05
updated: 2026-11-05
tags:
  - robotics
  - manipulation
  - reinforcement-learning
  - robot-learning
  - robot-dynamics
sources:
  - raw/papers/2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning.pdf
  - https://arxiv.org/html/2611.05372v1
---

# Learned Closed-Loop Inverse Kinematics

## Definition

목표 end-effector pose와 현재 로봇 상태를 받아 관절 명령의 **반복 갱신 규칙**을 학습하는 IK 접근이다. Static geometric IK가 $FK(q^\ast)=T_g$를 만족하는 관절 구성을 찾는 문제라면, 여기서는 실제 position controller를 거쳐 목표에 도달하고 머무는 실행 과정까지 목표로 삼는다. 이 페이지는 PolicyIK를 통한 구체적 사례 정리이며 전체 learned IK 문헌을 포괄하는 survey는 아니다. [원문 §§2–3](https://arxiv.org/html/2611.05372v1)

## Why It Matters

유한한 controller gain과 중력 하에서는 기하학적으로 맞는 $q^\ast$를 명령해도 measured pose가 목표에 정지하지 않을 수 있다. PolicyIK의 시뮬레이션처럼 feedforward 없는 비포화 PD를 가정하면 정적 평형은 아래와 같다. [원문 §4.1, App. A, Eq. 11](https://arxiv.org/html/2611.05372v1)

$$
K_p(z^\ast-q^\ast)=\tau_g(q^\ast),\qquad
z^\ast=q^\ast+K_p^{-1}\tau_g(q^\ast).
$$

따라서 목표에서 필요한 command $z^\ast$와 measured joint $q^\ast$가 다를 수 있다. 위 식은 특정 controller 가정 아래의 설명이며 gravity feedforward가 있는 모든 실물 제어기의 잔차를 그대로 기술하는 식은 아니다.

## Key Ideas

### 명령의 기억도 시스템 상태다

[[PolicyIK Joint-Reference Control]]은 $z_t=\operatorname{clip}(z_{t-1}+\eta\beta_ta_t)$로 reference를 누적한다. Zero action은 holding offset을 보존한다. 반면 measured joint를 매번 anchor로 삼으면 정책이 그 offset을 계속 다시 출력해야 한다. [원문 §4.1](https://arxiv.org/html/2611.05372v1)

같은 관절 상태에서도 이전 reference가 다르면 position controller가 만드는 다음 움직임이 달라진다. 그러므로 $d_t=z_{t-1}-q_t$를 policy에 입력한다. 이는 neural recurrent memory를 넣는 것과 별개로, action interface가 만드는 내부 상태를 명시적으로 드러내는 선택이다.

### 정밀 제어에는 관측·action·목적의 규모가 맞아야 한다

PolicyIK는 coarse/fine pose-error channel로 미세 residual을 드러내고, 현재 오차에 따른 gain으로 근접 시 reference 갱신량을 줄인다. Training objective도 approach tracking, best-so-far progress, tolerance 내부 dwell을 함께 포함한다. Fine feature 하나만 추가한 방법이나 binary-only reward 학습으로 축약할 수 없다. [원문 §§4.2–4.3](https://arxiv.org/html/2611.05372v1)

추론: 이 조합은 “정확한 관절 해 예측”과 “정확한 closed-loop 실행”을 별도 설계 문제로 보게 한다. 다만 classical differential IK·QP·MPC도 feedback 제어를 하므로 closed-loop 자체가 RL만의 특징은 아니다. 비교할 차이는 update law의 학습 여부, 관측·action interface, 학습 목적 및 제약이다. [비교 대상: 원문 §5.1, Apps. E, I](https://arxiv.org/html/2611.05372v1)

### Reaching과 holding은 다른 사건이다

$$
\rho_t=\max\!\left(\frac{e_p(t)}{1\,\mathrm{mm}},\frac{e_R(t)}{0.2^\circ}\right).
$$

$\rho_t\leq1$은 두 오차가 동시에 허용 범위 안이라는 뜻이다. 그러나 언제, 얼마 동안 이 조건을 만족해야 하는지는 별도 평가 정의다.

| 지표 | PolicyIK의 구체적 정의 | 읽을 때 주의점 |
|---|---|---|
| Simulation strict success | 5.3초 시도 마지막 1초의 평균 위치·회전 오차가 각각 threshold 이하 | 매 sample의 containment와 다름 |
| Simulation containment | 마지막 1초 모든 sample에서 $\rho_t\leq1$ | 단일 시도 92.4%; strict 93.5%와 구분 |
| Hardware reaching | 두 오차가 threshold 안에서 적어도 0.5초 연속 유지 | 이후 이탈해도 reached로 집계 |
| Hardware holding | 25초 예산의 마지막 5초 동안 매 sample에서 $\rho_t\leq1$ | OpenArm 43/60; reaching은 54/60 |

평균 terminal error, 성공 비율, 최초 도달 시간, 연속 holding은 서로 대체할 수 없다. Retry를 허용한 simulation deployment의 98.9%도 단일 시도 93.5%와 실행 예산을 함께 비교해야 한다. [원문 §§3, 5.1–5.2, Tables 1, 3–4](https://arxiv.org/html/2611.05372v1)

### FK 정확도와 외부 공간 정확도를 분리한다

Hardware pose error는 joint encoder와 modeled gripper frame의 FK로 계산된다. 따라서 $1\,\mathrm{mm}$ 결과는 해당 모델과 encoder 기준의 pose regulation 증거다. 추론: 외부 계측으로 확인하지 않은 calibration, 링크 변형, backlash 등의 오차까지 포함한 절대 TCP 정확도를 같은 수치로 보증할 수는 없다. [측정 정의: 원문 §5.2, App. I](https://arxiv.org/html/2611.05372v1)

## Evidence Limits / Reuse

- PolicyIK는 학습한 low-level update rule의 유효성을 보였지만, 비교군과 학습 비용·제어 주기·reference 제약이 모두 같지는 않다. Hardware policy 10 Hz와 classical baseline 50 Hz, 서로 다른 command lead/bound 설정을 함께 기록해야 한다. [원문 Apps. H–I, Tables 11–12](https://arxiv.org/html/2611.05372v1)
- OpenArm hardware는 simulation weights 없이 직접 학습했다. xArm7 결과는 xArm7용 별도 simulation/hardware 학습 정책이며 OpenArm 정책의 zero-shot 이전 실험이 아니다. [원문 §5.2, App. J](https://arxiv.org/html/2611.05372v1)
- 추론: 상위 planner·VLA·grasp generator와 연결할 때는 목표 pose 생성과 실행 정확도를 나누어 진단할 수 있다. 이 논문의 VLA 연결 근거는 side-mounted OpenArm으로 재학습한 정책의 시뮬레이션 pick-and-place 평가다.
- 열린 질문: 모델 오차, 외부 pose feedback, 접촉, payload 변화, collision constraint까지 포함해도 동일한 learned update rule의 이점이 유지되는가?

## Related Papers

- [[2026 - PolicyIK High-Precision Inverse Kinematics for Robot Arms with Reinforcement Learning]] — implemented-by: 이 개념의 직접 사례와 ablation 근거.
- [[2026-11-03 - PolicyIK Source]] — 원자료 범위와 확인 기록.

## Related Concepts

- [[Physical AI]] — 추론: 실제 controller interface와 동역학이 학습 문제의 일부가 되는 사례다.
- [[Vision-Language-Action Models]] — uses: 상위 pose 명령과 하위 실행을 분리한 시뮬레이션 평가와 연결된다.
- [[Generative Grasp Synthesis]] — 추론: 생성된 grasp pose의 품질과 팔의 pose 실행 품질을 구분하는 downstream 연결이다. PolicyIK가 grasp 생성 자체를 평가한 것은 아니다.
- [[2026-11-05 - How Should Pose Reaching and Holding Be Evaluated]] — answers: reaching·평균 오차·연속 holding·측정 좌표계의 구분.

## Contradictions / Updates

- 2026-11-05: PolicyIK v1을 근거로 개설. 문헌 전체에 대한 일반화와 위키의 재사용 해석에는 별도로 추론 표시를 붙였다.
