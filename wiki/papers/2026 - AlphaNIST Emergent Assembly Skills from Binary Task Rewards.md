---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, manipulation, contact-simulation, gpu-simulation]
sources:
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
  - https://arxiv.org/abs/2610.13354v1
  - https://alpha-nist.github.io/
title: "AlphaNIST: Emergent Assembly Skills from Binary Task Rewards"
authors:
  - Octi Zhang
  - Iretiayo Akinola
  - Rosario Scalise
  - Mateo Guaman Castro
  - Patrick Yin
  - Tobias Widmer
  - Miles Macklin
  - Chris Amevor
  - Dylan Turpin
  - Dirk Van Gelder
  - Jan Carius
  - Ankur Handa
  - Gavriel State
  - Yunrong Guo
  - Yashraj Narang
year: 2026
venue: "arXiv preprint; ICRA 채택 여부 미확인"
doi: "10.48550/arXiv.2610.13354"
url: https://arxiv.org/abs/2610.13354v1
---

# AlphaNIST: Emergent Assembly Skills from Binary Task Rewards

AlphaNIST는 **다양한 reset 상태·성공률 기반 sampling·다중 과제 PPO·병렬 simulation**을 결합해, 조립 중간 동작을 지시하지 않고 완료 목표로 학습한다. NIST ATB1의 20개 단일 부품 과제를 공유 정책으로 학습해 98.2%의 **학습 성공률**을 보고했다. 별도 학습한 10개 부품 조립 정책은 84%를 보고했으며, 실물 실험과 20개 전체 연속 조립은 아직 제시하지 않았다.

## Problem

[[NIST Assembly Task Board 1]]은 peg·rod 삽입, gear 장착, connector 결합, nut threading 등 20개 assembly pair를 포함한다. 작은 부품을 집은 뒤 자세를 바꾸고 좁은 결합부에 넣거나 돌려 끼워야 한다. 다중 부품에서는 이미 설치한 부품이 다음 동작을 방해할 수 있다. 논문의 질문은 이런 과정의 단계·순서·진행 보상을 얼마나 직접 지정해야 하는가이다. [§I]

## Core Idea

| 요소 | 역할 |
|---|---|
| OmniReset을 확장한 cache | 바닥의 부품, in-hand grasp, 결합 근처, 부분 조립 등 학습을 시작할 상태를 제공 |
| Success-Guided Sampling의 beta sampling | 최근 성공률이 중간인 assembly–reset 쌍에 더 많은 경험을 배분 |
| 공통 완료 보상 | 형상이 달라도 완전한 조립이라는 목적을 공유 |
| 공유 정책과 병렬 PPO | 서로 다른 부품에서 얻은 경험을 한 정책에 축적 |

reset bank는 시범 행동을 가르치거나 실행할 stage를 지정하지 않는다. 다만 **시범이 없다는 말이 초기 상태·성공 기준·관측·제어 설계까지 없다는 뜻은 아니다.** [§IV-A–B; [[Reset-State Curricula for Sparse-Reward RL]]]

## Method

- 20개 과제에 대해 하나의 geometry-conditioned policy와 하나의 value function을 처음부터 학습한다. specialist 사전학습·distillation·과제별 value head·명시적 planner는 사용하지 않는다. [§II-B, §IV]
- reset 항목 $i$의 최근 성공률 $\hat p_i$에 대해 sampling 가중치는 $\varepsilon_q+\sqrt{\hat p_i(1-\hat p_i)}$에 비례한다. 모든 항목에 양의 확률을 남긴다. [Eq. (4)]
- 조립 상대 목표에 대한 오차 $d_{\mathrm{asm}}$가 $0.001\,\mathrm{m}$ 미만이면 성공 보상 1을 한 번 주고 종료한다. 매 스텝 action 크기·관절 속도·토크에 대한 제어 비용을 뺀다. **binary는 task reward의 성격이며 전체 reward가 0/1인 것은 아니다.** [Eqs. (5)–(6)]
- 여러 부품이면 모든 active pair가 조립되어야 성공 보상을 받는다. 개별 부품 완료 보상이나 강제 조립 순서는 없다. [§IV-C]
- 재현에 필요한 수식과 절차는 [[AlphaNIST Binary-Reward Assembly]]에 정리했다.

## Data / Embodiment

- Isaac Lab의 GPU-parallel simulation, 7-DoF Franka Emika Panda와 parallel-jaw gripper. [§IV-D]
- 관측은 movable part·mating geometry·robot의 surface point cloud, proprioception, 직전 action이다. discrete task ID나 stage ID로 과제를 전달하지 않는다. actor와 critic은 파라미터를 분리한 SimBa 계열 네트워크다. [Fig. 3]
- 25 Hz에서 7차원 상대 관절 위치 목표와 1차원 gripper 명령을 출력하고 implicit impedance controller로 실행한다. [§IV-D]
- arm 관절 1–4 / 5–7의 속도 한계는 각각 2.175 / 2.61 rad/s, 토크 한계는 87 / 12 N·m이다. 이 제약은 simulation을 하드웨어 범위에 맞춘 것이며 실물 검증 결과는 아니다. [§IV-D, §VI]
- 1K–256K 병렬 환경으로 scale을 바꾸며, multi-GPU에서는 GPU당 4K 환경을 둔다. PPO iteration마다 환경당 32 step을 모으고 5 epoch·epoch당 4 minibatch로 최적화한다. [§IV-E]

## Evaluation / Results

### 1. 공유 정책과 specialist: 학습 성공 비교

64K 환경, 25K iteration 설정의 Fig. 5 / §V-A 결과다. 별도 정책 열은 과제별 정책 20개의 평균이며, **한 번의 rollout에서 보드의 20개 부품을 모두 완성하는 성공률이 아니다.**

| Task reward 설정 | 공유 정책 1개 | 별도 정책 20개 평균 |
|---|---:|---:|
| Sparse completion + control cost | 98.2% | 81.4% |
| 위 설정 + reach/alignment shaping | 17.8% | 78.3% |

dense 조건은 부품 중심에 대한 접근과 목표 조립 방향 정렬 항을 추가하며 두 계수는 각각 0.01이다. 이 특정 shaping이 joint learning에 불리했다는 결과이지, dense reward 일반의 불가능성을 보인 것은 아니다. [Eq. (7), §V-A]

공유 sparse 학습은 410 GPU-hours, 별도 sparse 정책 전체는 16.1K GPU-hours로 보고되어 총 device-hours가 약 39.3배 차이 난다. per-run interaction budget을 맞춘 비교이며 **전체 20개 specialist의 총 자원을 공유 정책 한 번과 동일하게 제한한 실험은 아니다.** [§V, Fig. 6]

### 2. Scale·sampling: 고정 reset bank 평가

Fig. 7은 25K-iteration checkpoint를 stochastic action으로 평가한다. 과제별 uniform sampling을 하는 공통 frozen mixed-reset bank, 5개 **평가 seed**, seed·과제당 32 trial, 20개 과제를 사용한다. 15초 내 완전 조립하면서 같은 step에 safety failure가 없어야 성공이다. 평가 seed 수를 독립적인 학습 seed 수로 바꾸어 읽으면 안 된다. [§V, Fig. 7]

| 256K 환경 학습 조건 | 평가 성공률 |
|---|---:|
| Sparse + beta sampling | 97.4% |
| Sparse + uniform sampling | 84.3% |
| Dense + beta sampling | 77.4% |
| Dense + uniform sampling | 34.3% |

위 수치는 앞의 98.2% 학습 성공률과 평가 절차가 다르다. mixed reset에는 이미 잡았거나 일부 조립한 상태도 포함되므로, 모든 시험이 테이블에서 시작한 전체 pickup-to-assembly 과정이라는 해석도 피한다. [§IV-B, §V]

### 3. 여러 부품: 부품 수별 별도 정책

| Active assembly pairs | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Episode 성공률 (%) | 99 | 97 | 95 | 93 | 92 | 90 | 89 | 87 | 86 | 84 |

각 정책은 해당 active-pair 수로 학습·평가한다. 시간 제한은 pair당 15초이며 모든 pair가 완료되어야 episode가 성공한다. 1-pair 행의 99%를 앞의 20-task 학습 평균 98.2%와 같은 실험으로 합치지 않는다. [Table I, §V-D]

## Emergent Behavior

저자들은 peg를 내려놓고 끝부분으로 다시 잡기, board 접촉으로 connector 방향 바꾸기, fingertip tap으로 nut를 돌리기 등을 관찰했다. 여러 부품에서는 다른 부품을 처리한 뒤 미완성 부품으로 돌아가는 행동도 보였다. 이들은 명시적 planner나 동작 시범 없이 나타난 관찰 사례다. 모든 초기 상태에서 그러한 행동이 성공한다거나 일반적인 계획 능력이 검증되었다는 뜻은 아니다. [Figs. 8–9, §V-C–D]

## Limitations

1. **모든 결과는 simulation**이다. 센서 기반 점군, 지연, 접촉 모델 오차에 대한 실물 반복성은 후속 검증 대상이다. [§VI]
2. 단일 episode에서 최대 10개 pair를 다뤘다. 전체 20개 pair 조립은 향후 과제다. [§VI]
3. 완료에 가까운 상태도 제공하는 reset 설계와 대규모 경험 수집에 의존한다. 성공률만으로 reset 생성 비용·배포 초기 상태의 난이도·전체 학습 비용을 생략하지 않는다.
4. 시험한 reach/alignment shaping과 fixed coefficient를 넘어, task별 재설계·다른 shaping·다른 simulator에서도 같은 우열이 유지되는지는 미확인이다.
5. §I는 코드 공개를 검토·수정 후로 예고했다. 2026-11-03 확인한 공식 프로젝트·논문에서 구현 링크를 찾지 못했으며, 이 위키에서 학습을 재현하지 않았다.

## Connections

- [[AlphaNIST Binary-Reward Assembly]] — implemented-by: reset–sampling–reward–PPO 절차.
- [[Reset-State Curricula for Sparse-Reward RL]] — uses: 성공에 도달할 기회를 만드는 초기 상태 분포.
- [[NIST Assembly Task Board 1]] — evaluated-on: 단일 부품 및 여러 부품 평가를 구분하는 benchmark.
- [[Object Singulation]] — 저자들이 관찰한 pushing·sliding은 이후 grasp를 가능하게 하는 중간 행동의 사례다.
- [[RECAP RL with Experience and Corrections]] — 비교: RECAP의 시범·개입·pretrained VLA 개선과, AlphaNIST의 simulation PPO from scratch는 학습 전제가 다르다.
- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] — answers: sparse reward가 성립하는 조건과 보행 문제로의 적용 범위.

## Contradictions / Updates

- 2026-11-03: 최초 ingest. 기존 보행 문서의 shaping을 틀렸다고 대체하지 않는다. 과제·reset 분포·실패 비용이 다른 연구이며 이식 가능성은 별도 실험 질문이다.

## Notes / Marginalia

공개 v1 PDF에 Link annotation 81개를 확인했고 필기·하이라이트 annotation은 발견하지 못했다. 검사·원본 checksum은 [[2026-10-09 - AlphaNIST Source]]에 기록했다.

## Open Questions

- 낯선 부품·목표 배치·초기 상태에 대한 일반화는 얼마나 되는가?
- 물리적 센서 오차와 마찰·접촉 오차에서 10-pair completion이 얼마나 유지되는가?
- 넓은 reset coverage와 다중 과제 경험 중 어느 부분이 작은 부품의 grasp 학습에 가장 중요한가?

근거: [저자 논문 v1](https://arxiv.org/html/2610.13354v1), [공식 프로젝트](https://alpha-nist.github.io/), 로컬 원본 PDF. 문서의 수치는 별도 표시가 없으면 저자 보고(Tier A)다.
