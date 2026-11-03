---
type: benchmark
status: active
created: 2026-11-03
updated: 2026-11-03
tags:
  - benchmark
  - manipulation
  - reinforcement-learning
  - contact-simulation
sources:
  - https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
  - https://arxiv.org/html/2610.13354v1
  - https://alpha-nist.github.io/
---

# NIST Assembly Task Board 1

## Snapshot

NIST Assembly Task Board #1(ATB1)은 peg insertion, gear meshing, electrical connector insertion, nut threading 능력을 평가하는 조립 artifact다. **보드 자체와 특정 논문이 정한 학습·평가 프로토콜은 구분한다.** 아래 RL 수치·시간 제한은 AlphaNIST의 simulator 실험 설정이며 보드 공통의 공식 성공률 기준이 아니다.

NIST는 부품의 크기·형상·위치·종류를 설계 요인으로 설명하고 replication 지침, CAD/STL, benchmark template을 제공한다. 근거: [NIST 공식 설명, Task Board #1](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly), Tier A, 확인 2026-11-03.

## Task Definition

AlphaNIST는 ATB1을 **20개 assembly pair**로 정의한다. Pair는 이동 가능한 part, 고정된 mating geometry, 완성된 상대 pose로 이루어진다. 작은 부품의 grasp, transport, 정렬, 삽입·나사 체결과 실패 후 복구가 필요하다. 최소 4 mm 크기의 부품과 좁은 여유 공간을 포함한다. 근거: [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]], §I, III-A.

| 문제 설정 | 한 에피소드의 목표 | 구분할 점 |
|---|---|---|
| Single-pair, multi-task | 20개 task 중 선택된 한 pair 완료 | 한 정책이 20종을 다루어도 보드 전체를 한 번에 조립한 것은 아님 |
| Multi-pair | 여러 active pair를 모두 완료 | Pair 수마다 정책을 별도로 학습·평가 |
| Full-board episode | 20개 pair를 하나의 episode에서 완료 | AlphaNIST v1의 향후 과제 |

근거: §III-A, V-D–VI, Table I. 완성된 전체 보드 이미지와 성공 episode의 task 범위를 혼동하지 않는다.

## Data / Scale

- AlphaNIST는 Franka Panda와 parallel-jaw gripper를 시뮬레이션한다. 정책 입력은 robot state와 part·mating geometry·robot의 표면 점군이다 (§IV-D).
- Reset bank에는 loose part, pickup, transport, near-mating, partial assembly가 포함된다. 성공률 집계는 이러한 시작 상태 전체를 포함한다 (§IV-B, V).
- Joint/specialist 비교는 run당 64K 환경·25K iteration이다. 별도의 scaling 실험은 1K–256K 환경을 비교한다. Specialist 20개의 총 학습 비용은 shared policy 한 개와 다르다 (§V-A–B).
- NIST의 실물 artifact와 AlphaNIST의 simulator asset을 같은 검증 대상이라고 가정하지 않는다. 이 페이지는 다른 구현의 asset·마찰·공차까지 일치함을 확인하지 않았다.

## Metrics

**AlphaNIST 단일 pair 성공 판정:** 논문 정의의 assembly error $d_{\mathrm{asm}}^e<0.001\,\mathrm m$일 때 완료 task reward를 한 번 지급하고 종료한다. 전체 학습 보상에는 별도 제어 비용이 있다 (§IV-C).

**Scaling evaluation:** 25K-iteration checkpoint에서 stochastic action을 사용하고, 공통 frozen mixed-reset bank를 task별 uniform sampling한다. Task당 32회 × 20 task × 5 evaluation seed이며 mean±standard deviation을 보고한다. 15초 이내 완료하면서 동시에 safety failure가 없어야 성공이다 (§V, Fig. 7). Evaluation seed 수를 독립 training seed 수로 해석하지 않는다.

**Multi-pair:** 모든 active pair가 완성될 때만 task 성공이며 pair당 15초를 허용한다. 각 정책의 학습·평가 active pair 수가 같다 (§V-D, Table I). 이 수치는 training 비교의 98.2%와 다른 실험이다.

## Known Results

다음은 AlphaNIST v1의 저자 보고값이며 이 위키에서 독립 재현하지 않았다.

| 64K 환경·25K iteration 학습 비교 | Shared policy | Separate policies 평균 |
|---|---:|---:|
| Binary task reward + control cost | 98.2% | 81.4% |
| 위 보상 + reach/alignment shaping | 17.8% | 78.3% |

근거: §V-A, Fig. 5. 비교한 shaping 계수는 각각 0.01이다. 이 표만으로 모든 dense reward 설계의 우열을 결정할 수 없다.

| 별도의 256K scaling 평가 | Beta sampling | Uniform sampling |
|---|---:|---:|
| Binary task reward + control cost | 97.4% | 84.3% |
| Dense shaping 추가 | 77.4% | 34.3% |

근거: §V-B, Fig. 7. 98.2% 학습 성공률과 97.4% 평가 성공률을 같은 분포의 scale 변화로 비교하지 않는다.

| Active pair 수 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Multi-pair 성공률 (%) | 99 | 97 | 95 | 93 | 92 | 90 | 89 | 87 | 86 | 84 |

근거: Table I. **10-pair 84%는 별도 정책의 결과**이며, single-pair 정책을 변경 없이 적용한 zero-shot sequence 결과가 아니다.

## Caveats

- AlphaNIST의 모든 결과는 simulation이다. 실제 보드·sensor observation·latency·접촉 오차에 대한 transfer와 반복성은 검증 예정으로 남긴다 (§VI).
- 평가 bank는 mixed reset이다. 전체 성공률이 loose-start pickup부터 시작한 성공률이나 unseen geometry 성능을 뜻하지 않는다 (§V).
- 하드웨어에 맞춘 속도·토크 제한은 현실적인 제어 범위를 설정하지만 실물 검증을 대신하지 않는다 (§IV-D, VI).
- 추론: 연구 간 비교에는 episode 목표, 시작 상태, 관측, simulator·asset, 시간 제한과 실패 판정을 함께 맞춰야 한다. 같은 보드 이름이나 성공률 단위만으로 순위를 정할 수 없다.

## Related Papers

- [[Physical AI]] — 실제 조립 artifact와 simulation 학습·실물 배포의 검증 범위를 연결한다.
- [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]] — 이 페이지의 multi-task·multi-pair RL 결과 근거.
- [[2026-10-09 - AlphaNIST Source]] — 논문 및 프로젝트 확인 기록.
- [[AlphaNIST Binary-Reward Assembly]] — uses: 이 benchmark를 다루는 reset·sampling·PPO 절차.
- [[Reset-State Curricula for Sparse-Reward RL]] — 초기 상태 분포가 학습과 평가 해석에 미치는 영향.
- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] — 보상 비교 결과를 다른 과제로 옮길 때의 질문.

## Open Questions

- 같은 실물 보드에서 loose-start와 intermediate-start 성공률·완료 시간을 어떻게 나누어 보고할 것인가?
- Sensor-derived 관측과 반복 가능한 접촉 조건에서 multi-pair 성능이 유지되는가?
- 20-pair episode와 초기·중간 실패에서의 복구를 동일 protocol로 평가할 수 있는가?
