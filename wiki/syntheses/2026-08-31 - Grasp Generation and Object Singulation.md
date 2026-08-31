---
type: synthesis
status: draft
created: 2026-08-31
updated: 2026-08-31
tags:
  - grasping
  - manipulation
  - bin-picking
  - object-singulation
  - generative-models
  - affordance
sources:
  - raw/papers/2608.26076v1.pdf
  - raw/papers/2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects.pdf
---

# Grasp Generation and Object Singulation

## Executive Summary

위키에는 "grasp"라는 같은 단어를 쓰지만 서로 링크되지 않은 두 축이 있다. 하나는 단일 물체의 $SE(3)$ grasp pose **분포를 생성**하는 축([[Generative Grasp Synthesis]], [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]])이고, 다른 하나는 얽힌 물체 더미에서 **어떤 primitive를 실행할지 고르는** 축([[Object Singulation]], [[Tangled-Prone Bin Picking]], [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]])이다.

두 축은 경쟁 관계가 아니라 **같은 파이프라인의 서로 다른 층**이다. 생성 축은 "이 물체를 어떻게 잡는가"의 해공간을 주고, singulation 축은 "지금 무엇을 대상으로 삼는가"를 정한다. 실제로 GraspMF의 실기 파이프라인은 SAM segmentation → grasp 샘플링 → RRT-Connect 계획인데, 이 구조는 **집을 물체가 이미 분리 가능하다는 가정** 위에서만 성립한다. 그 가정이 깨지는 지점이 정확히 singulation 축의 문제 영역이다.

추론: 두 축이 만나는 실질적 접점은 세 가지다. ① cluttered scene 조건부 grasp 분포 학습(= segmentation 의존성 제거), ② 밀리초 latency가 열어주는 closed-loop 재계획(bin picking은 본래 재관측·재계획 루프다), ③ grasp 분포 위에 얽힘 점수를 downstream 목적으로 얹는 구성. 위키에 이 셋을 실제로 수행한 자료는 아직 없다.

## Current Picture

### 축 1 — 분포 생성 (2026 ingest)

- 문제: 한 물체의 유효 grasp 집합은 $SE(3)$ 위의 multimodal 분포다. point estimate 회귀 대신 분포를 학습하면 여러 mode를 샘플링하고 collision avoidance·reachability 같은 downstream 목적과 합성할 수 있다.
- 계보: CVAE(6-DOF GraspNet) → diffusion/score(SE3-DiffusionFields, GraspLDM, VSIGD) → flow(EquiGraspFlow, BRIDGER) → few-step([[GraspMF Few-Step Grasp Generation]]).
- 현재 경쟁 지표는 품질(SR·EMD)과 **샘플링 속도**다. GraspMF는 $SO(3) \times \mathbb{R}^3$ 위 [[MeanFlow]] 정식화로 5 NFE 이하에서 품질을 유지하며 이 두 번째 축을 사실상 해소했다고 주장한다.
- 평가 프로토콜은 [[ACRONYM]] + Isaac Gym 실행 SR + EMD 커버리지로 수렴해 있다.

### 축 2 — 얽힘과 primitive 선택 (2023 자료)

- 문제: 산업용 bin에서 부품이 서로 얽히면 grasp 성공률을 아무리 올려도 여러 개가 딸려 올라오거나 분리되지 않는다. 처리량을 결정하는 것은 grasp 성공이 아니라 **singulation 성공**이다.
- 접근: depth image에서 pixel-wise [[Action Affordance Learning|action affordance]]를 예측하고 `pick` / `drop` / `pull` 중 하나를 고르는 계층형 정책(`PickNet`의 PickMap·SepMap, `PullNet`의 방향별 pull affordance). 학습 데이터는 simulator의 algorithmic supervisor로 self-supervised 수집한다.
- 얽힘은 접촉과 기하가 결합된 현상이라 sim-real gap이 크고, top-down depth는 occlusion과 missing geometry에 취약하다는 것이 위키에 기록된 한계다.

### 축 3 — 암묵적 grasp (배경)

[[Vision-Language-Action Models]] 계열은 grasp을 명시적 pose 분포가 아니라 policy 안에 암묵적으로 학습한다. [[Generative Grasp Synthesis]]에 이미 적어둔 추론대로, 명시적 grasp 생성은 계획 기반 파이프라인(segmentation → grasp 샘플링 → motion planning)에서 여전히 유효하다. 세 축의 정면 비교 자료는 위키에 없다.

## Evidence

- **Tier A**: GraspMF 본문 Table I–V — T=5에서 15.5ms, ACRONYM ID SR 87.40 / OOD 71.73, 전 sampling budget($T{=}1{\dots}100$)에서 OOD SR 표준편차 1.63. 실기 Franka Research 3 + Franka Hand, SAM segmentation, VAMP RRT-Connect, 물체 3종 9~10/10.
- **Tier A**: Zhang et al. 2023 본문 — `PickNet`/`PullNet` 구조, PhysX 기반 self-supervised 데이터 수집, Kawada NEXTAGE + Photoneo PhoXi 실기에서 약 90% 성공률.
- **Tier C (추론)**: 아래 Comparison의 "접점" 항목과 Implications의 파이프라인 구성은 두 자료를 위키 차원에서 결합한 에이전트 추론이다. 어느 논문도 상대 축을 다루지 않는다.

## Comparison

| 축 | 결정 변수 | 관측 | 학습 신호 | 평가 | 지배적 실패 모드 |
|---|---|---|---|---|---|
| 분포 생성 (GraspMF) | 연속 pose $H = (R,p) \in SO(3)\times\mathbb{R}^3$ | 물체 단위 point cloud 1024점, centroid 정규화 | ACRONYM의 sim 판정 grasp 라벨 ~780K (supervised) | Isaac Gym SR + EMD + latency | 부분 관측 편향(centroid 정규화가 가시 표면 쪽으로 치우침), cluttered·dexterous 미지원 |
| Singulation (PickNet/PullNet) | 이산 primitive + pixel 위치·방향 | bin 전체 top-down depth image | simulator algorithmic supervisor (self-supervised) | 실기 성공률, cycle time | 얽힘 판정 실패, occlusion, sim-real gap |
| 암묵적 (VLA) | action chunk | multimodal, 언어 조건 | 원격조작 시연 + 경험 | 태스크 성공률 | 위키에 grasp 단위 분석 자료 없음 |

접점 정리:

- **접점 1 — segmentation 가정.** GraspMF는 물체 단위 point cloud를 입력으로 받고, 실기에서는 SAM으로 잘라 쓴다. 얽힌 bin에서는 segmentation이 성립하지 않거나, 성립해도 잡으면 딸려 올라온다. GraspMF 페이지의 열린 질문("cluttered scene 조건부 분포 학습, 물체 단위 segmentation 의존성 제거")과 [[Object Singulation]]의 문제 정의는 사실상 같은 벽의 양면이다.
- **접점 2 — 재계획 비용.** [[Tangled-Prone Bin Picking]]의 기본 루프는 실행 → 재관측 → 재계획이다. 추론: 물체당 100 grasp를 6.3~15.5ms에 뽑는 생성기는 이 루프에서 grasp 재계획을 사실상 공짜로 만들어 primitive 선택만 남긴다. 단 GraspMF 논문은 closed-loop replanning을 실증하지 않았고("may achieve better performance") 이는 그 페이지의 명시적 limitation이다.
- **접점 3 — downstream 목적으로서의 얽힘.** [[Generative Grasp Synthesis]]는 분포 학습의 장점으로 "downstream 목적과의 합성"을 든다. SepMap이 표현하는 얽힘 정도는 collision·reachability와 같은 층위의 목적 함수로 볼 수 있다. 추론: grasp 분포 샘플에 얽힘 점수로 rejection/reweighting을 거는 구성이 자연스럽지만, 위키에 이를 수행한 자료는 없다.
- **접점 4 — 기하 표현 공유.** GraspMF는 보조 SDF regression으로 flow map을 물체 기하에 grounding한다([[Neural Implicit Surface Representation]]). 얽힘 역시 접촉·기하 결합 현상이다. 열린 질문: 같은 SDF 특징이 얽힘 판정에도 쓰일 수 있는가. [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]의 확장 사례가 된다.

## Implications

- **파이프라인 층 분리가 유효하다.** 추론: singulation은 "무엇을 대상으로 삼는가"(이산 선택), 생성은 "그 대상을 어떻게 잡는가"(연속 분포)로 나누면 두 자료를 그대로 쌓을 수 있다. 이 분리에서 병목은 두 층 사이의 인터페이스, 즉 clutter 안에서 물체 단위 조건을 어떻게 만들 것인가다.
- **속도 개선의 수혜자는 단일 물체 grasp이 아니라 루프 전체일 가능성이 크다.** 단일 물체 table-top에서 600ms를 15ms로 줄이는 것의 실효 이득은 제한적이다. 반복 재계획이 본질인 bin picking 쪽이 latency 개선이 실제로 값을 하는 곳이다. 검증 필요: 이 주장을 뒷받침하는 실험 자료는 위키에 없다.
- **평가 프로토콜이 서로 호환되지 않는다.** 생성 축은 [[ACRONYM]] 기반 sim SR + EMD, singulation 축은 실기 성공률·cycle time을 쓴다. 두 축을 잇는 연구가 나오려면 clutter 안에서의 분포 커버리지를 재는 지표가 필요한데, EMD는 이미 부분 관측에서 reference set 의존성 문제를 드러냈다.
- **위키 유지관리:** 이 페이지가 두 축의 허브 역할을 한다. grasp 관련 새 자료를 ingest할 때 어느 축에 속하는지, 접점 1~4 중 무엇을 건드리는지 먼저 판정한다.

## What To Watch

- GraspMF future work의 dual-arm $SE(3)\times SE(3)$과 contact manifold 확장 — cluttered·dexterous 방향으로 실제로 가는지.
- Cluttered scene 조건부 grasp 분포 학습(segmentation 없는 조건화)의 최신 상태. 위키에 자료 없음.
- Few-step 생성기를 실제 closed-loop replanning 루프에 넣은 실증. 동적 장면 성공률 개선폭.
- Tactile / force-torque 결합이 얽힘 판정 실패를 얼마나 줄이는가 ([[Tangled-Prone Bin Picking]]과 [[Robotic Cloth Manipulation]]이 같은 질문을 공유한다).
- 명시적 grasp 생성 + motion planning vs end-to-end [[Vision-Language-Action Models]]의 산업 배치 비교 자료.

## Open Questions

- 열린 질문: clutter 안에서 "이 물체의 grasp 분포"를 조건화하는 최소 인터페이스는 무엇인가 — instance mask, 3D bounding box, 아니면 조건 없이 scene 전체 grasp field인가?
- 열린 질문: 얽힘 정도를 grasp 분포의 reweighting 항으로 표현할 수 있는가, 아니면 별도 primitive 선택 층이 원리적으로 필요한가?
- 열린 질문: sim 판정 grasp 라벨(ACRONYM)과 simulator algorithmic supervisor(PickNet 계열)는 둘 다 시뮬레이션 의존인데, 얽힘 접촉의 sim-real gap이 grasp의 그것보다 큰가?
