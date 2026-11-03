---
type: index
status: active
created: 2026-06-14
updated: 2026-11-03
tags:
  - index
  - robotics
  - physical-ai
sources: []
---

# Robotics / Physical AI Wiki Index

이 파일은 위키 전체를 탐색하기 위한 내용 중심 카탈로그다. 새 자료를 ingest할 때마다 갱신한다.

## Start Here

- [[Home]] - vault 소개와 사용법.
- [[Workflow]] - 자료 ingest, 질문 답변, 위키 점검 절차.
- [[Maintenance]] - 위키 점검 체크리스트와 `wiki/_meta/lint.py` 실행 방법.
- [[Chat Source Workflow]] - `raw/chats/` LLM 대화 기록을 source note와 위키 페이지로 승격하는 절차.
- [[Ontology]] - 지식 축, 관계 어휘, 태그 어휘, 근거 등급(Tier A/B/C).
- [[Templates]] - 페이지 템플릿과 frontmatter 명세.

운영 규칙 전체는 vault 루트의 `AGENTS.md`에 있다. Claude Code는 `CLAUDE.md`가 이를 import한다.

## Sources

- [[2026-10-09 - AlphaNIST Source]] - 공식 v1 PDF, 주석 검사, simulation 결과와 공개 범위.
- [[2026-11-03 - Chat Quadruped Open Stair Learning]] - RBQ10 보행 대화의 질문·문헌·검증 범위.
- [[2026-06-24 - StairMaster Source]] - 열린 계단 논문 v2와 저자 프로젝트.
- [[2023-09-25 - Extreme Parkour Source]] - 엣지 회피 보상과 ICRA 발표 정보.
- [[2023-06-26 - ANYmal Parkour Source]] - 계층형 구조와 supplementary 보상 표.
- [[2024-09-29 - DreamWaQ++ Source]] - multimodal 입력과 style reward curriculum.
- [[2025-02-14 - BeamDojo Source]] - 드문 발판의 지지 보상과 발 높이 항.
- [[2026-09-24 - TactileStep Source]] - 촉각과 접촉 단계별 보상.
- [[2024-08-25 - PIE Source]] - 비대칭 actor-critic과 명시·암묵 추정.
- [[2026-03-03 - LF2WB Source]] - 전방 지각으로 후진을 지원하는 지형 기억.
- [[2026-07-13 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]] - 사용자 제공 v1 PDF의 출처, 주석 검사와 검증 범위.
- [[2026-06-22 - AI-Based Robot Fault Diagnosis Chat]]
- [[2026-06-15 - Amortized NeuralSDF KKT Explanation Chat]]
- [[2026-06-21 - TE-SDF Learning Material]]
- [[2026-04-24 - pi0.7 Steerable Generalist Robotic Foundation Model]]
- [[2025-11-19 - pi0.6 a VLA That Learns From Experience]]
- [[2026-05-07 - TE-SDF Tetra-Encoded Signed Distance Field]]
- [[2026-03-06 - Amortized NeuralSDF-Mesh Collision Detection]]
- [[2026-03-31 - DIAL Decoupling Intent and Action via Latent World Modeling]]
- [[2026-02-06 - Deep Learning-Based Robotic Cloth Manipulation Review]]
- [[2026-06-15 - Small-Motion End-Effector Inertia and Friction Fault Diagnosis Note]]
- [[2023-07-07 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]]
- [[2021-06-29 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]
- [[2026-06-15 - LG CNS PhysicalWorks Deep Research Report]]

- [[2023-04-18 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]]
- [[2026-08-26 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]]

## Papers

- [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]] - diverse resets·SGS·PPO로 학습한 다중 과제 조립과 binary reward의 조건.
- [[2026 - StairMaster Hollow Stair Locomotion]] - 열린 계단의 depth·공간 기억·hollow/edge 벌점.
- [[2023 - Extreme Parkour with Legged Robots]] - 단일 지각 정책과 접촉 조건부 엣지 회피.
- [[2023 - ANYmal Parkour]] - 여러 보행 기술을 선택하는 계층형 시스템과 동작 정규화.
- [[2024 - DreamWaQ++ Multimodal Locomotion]] - 점군·고유감각 융합과 style reward 완화.
- [[2025 - BeamDojo Sparse Foothold Locomotion]] - 휴머노이드 발바닥 중첩과 두 critic 학습.
- [[2026 - TactileStep Sole Tactile Locomotion]] - 촉각 기반 착지 충격과 지지 품질 개선.
- [[2024 - PIE Implicit-Explicit Parkour]] - 추정기와 PPO를 동시에 학습하는 4족 parkour.
- [[2026 - Look Forward to Walk Backward]] - Delta-rule 기억으로 전방 시야 밖 후진 지형을 추정.
- [[2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation]] - URDF 그래프 조건부 CFM으로 여러 다관절 손의 palm pose와 관절값을 직접 생성한다.
- [[2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration]] - neural SDF로 대응점 없이 point cloud를 정렬한다.
- [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]] - MeanFlow를 SO(3)×R3에 정식화해 5 NFE 이하로 SOTA급 grasp을 생성한다 (GraspMF).
- [[2026 - pi0.7 Steerable Generalist Robotic Foundation Model]]
- [[2025 - pi0.6 a VLA That Learns From Experience]]
- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]
- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]]
- [[2026 - DIAL Decoupling Intent and Action via Latent World Modeling]]
- [[2026 - Deep Learning-Based Robotic Cloth Manipulation Applications]]
- [[2020 - The Frontier of Simulation-Based Inference]]
- [[2019 - Automatic Posterior Transformation for Likelihood-Free Inference]]
- [[2022 - Neural Posterior Domain Randomization]]
- [[2021 - A Differentiable Newton-Euler Algorithm for Real-World Robotics]]
- [[2021 - Effects of Temperature and Mounting Configuration on Dynamic Parameters Identification]]
- [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]]
- [[Unverified - Raviola Dynamic Parameter Identification Reference]] - superseded by the verified Raviola paper page.

## Concepts

- [[Reset-State Curricula for Sparse-Reward RL]] - 초기 상태 coverage·sampling·완료 목표를 분리하는 학습 설계.
- [[Perceptive Legged Locomotion]] - 보행 정책의 센서·특권 정보·행동·하위 PD 계약.
- [[Terrain Memory for Legged Locomotion]] - 가려진 발판의 기억과 안전한 착지의 구분.
- [[Embodied AI]] - 환경 안에서 지각, 추론, 행동을 결합하는 AI.
- [[Physical AI]] - 물리 세계에서 작동하는 범용 지능과 로봇 시스템에 대한 넓은 축.
- [[Vision-Language-Action Models]] - 시각, 언어, 행동을 연결하는 로봇 foundation model 계열.
- [[Simulation-Based Inference]]
- [[Neural Posterior Estimation]]
- [[Differentiable Dynamics]]
- [[Temperature-Friction Baseline]]
- [[Slow-Fast Parameter Separation in Robot Fault Diagnosis]]
- [[Robot Dynamics Parameter Identification]]
- [[Object Singulation]]
- [[Action Affordance Learning]]
- [[Robot Foundation Models]]
- [[Context-Conditioned Robot Foundation Models]]
- [[Robot Fleet Orchestration]]
- [[Robotic Cloth Manipulation]]
- [[Latent World Modeling]]
- [[Signed Distance Field Collision Detection]]
- [[Tetra-Encoded Signed Distance Field]]
- [[NeuralSDF Collision Detection]]
- [[Neural Implicit Surface Representation]] - SDF를 접촉 계산과 지각 양쪽에서 공유하는 상위 표현 개념.
- [[Point Cloud Registration]] - 두 point cloud를 정렬하는 문제와 그 강건성 축.
- [[Flow Matching]] - velocity field 회귀로 분포를 운반하는 생성 모델 프레임워크. pi0 계열 action head의 기반.
- [[MeanFlow]] - 구간 평균 속도를 학습해 1~수 스텝 생성을 얻는 few-step 프레임워크.
- [[Generative Grasp Synthesis]] - grasp pose와 다관절 손 구성의 분포를 생성 모델로 학습하는 문제 영역.
- [[Cross-Embodiment Dexterous Grasping]] - 손 구조·관절 차원이 다른 경우의 grasp 표현과 일반화 평가 범위.

## Methods

- [[AlphaNIST Binary-Reward Assembly]] - reset bank, beta sampling, 완료 보상과 제어 비용을 결합한 PPO 조립 절차.
- [[Open Stair Reward Design and Evaluation]] - 엣지·발 높이·착지·지지·정체를 분리해 설계하고 평가하는 절차.
- [[Physics-Informed Neural Posterior Estimation for Robot Fault Diagnosis]]
- [[Safe Diagnostic Trajectory Design]]
- [[RECAP RL with Experience and Corrections]]
- [[TE-SDF Collision Detection]]
- [[Amortized NeuralSDF-Mesh Collision Detection]]
- [[Cloth Manipulation Learning Paradigms]]
- [[Small-Motion Tool Inertia and Friction Fault Diagnosis]]
- [[Tangled-Prone Bin Picking]]
- [[SDFReg Point Cloud Registration]]
- [[GraspMF Few-Step Grasp Generation]] - MeanFlow 기반 밀리초 단위 grasp pose 샘플링 절차.
- [[GraspGraphNet Graph-Structured Grasp Generation]] - differentiable FK와 dynamic world edges를 결합한 palm+joint CFM 절차.

## Entities

- [[Physical Intelligence]]
- [[LG CNS PhysicalWorks]]

## Benchmarks

- [[NIST Assembly Task Board 1]] - 20개 assembly pair와 single-pair·multi-pair·실물 평가의 구분.
- [[ModelNet40]] - 합성 CAD shape 기반 registration benchmark. cross-category 일반화 측정.
- [[3DMatch]] - Kinect 실내 RGB-D scan 기반 실 데이터 registration benchmark.
- [[ACRONYM]] - 시뮬레이션 기반 대규모 parallel-jaw grasp 데이터셋. SE(3) grasp 생성 연구의 표준.

## Syntheses

- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] - 핵심 문헌 6편·관련 2편 비교와 RBQ10 실험의 적용 한계.
- [[2026-06-15 - Small-Motion Tool Inertia and Friction Fault Diagnosis]]
- [[2026-06-15 - LG CNS PhysicalWorks]]

## Questions

- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] - AlphaNIST의 조건과 보행 보상 설계로의 적용 한계.
- [[2026-11-03 - Does Quadruped RL Need Depth Cameras]] - 학습 전용 지형과 실제 배포 지각 입력의 차이.
- [[2026-11-03 - Why Does Memory Not Prevent Stair Edge Contacts]] - LSTM·출력 구조·접촉 보상의 역할과 진단 순서.
- [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]
- [[2026-06-22 - What Is the Difference Between pi0.6 and pi0.7]]
- [[2026-06-22 - What Is the Relationship Between VLA and Reinforcement Learning]]
- [[2026-06-22 - How Should Diagnostic Trajectories Match NPE Training Data]]
- [[2026-06-22 - Should Robot Fault Diagnosis Use CVAE or NPE]]
- [[2026-06-22 - How Can AI Diagnose Robot Friction Faults Under Small Motions]]
- [[2026-06-22 - How Does TE-SDF Compute Distance]]
- [[2026-06-21 - What Does KKT Mean in Amortized NeuralSDF Contact Prediction]]
- [[2026-06-15 - How Should VLA Models Bridge Intent and Action]]
- [[2026-06-15 - What Blocks General Robotic Cloth Manipulation]]
