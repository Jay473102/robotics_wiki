---
type: paper
status: active
created: 2026-11-03
updated: 2026-11-03
tags: [paper, reinforcement-learning, perception, humanoid, sim-to-real]
sources:
  - https://arxiv.org/abs/2609.28959v1
  - https://arxiv.org/html/2609.28959v1
title: "TactileStep: Sole Tactile Learning for Regulating Foot-Terrain Interaction in Humanoid Locomotion"
authors: [Zizhuo Wang, Ming-Ju Lee, Shaoting Zhu, Haozhe Lou, Hang Zhao, Yiming Li]
year: 2026
venue: arXiv preprint v1
doi: 10.48550/arXiv.2609.28959
url: https://arxiv.org/abs/2609.28959v1
---

# TactileStep

과제를 완주해도 거칠게 착지하거나 엣지에 불안정하게 설 수 있다는 문제를 다룬다. Unitree G1에서 발바닥 압력 정보를 사용해 착지 충격과 지지 품질을 개선하는 휴머노이드 연구다. [초록](https://arxiv.org/abs/2609.28959v1)

## 입력과 출력

Actor는 고유감각, depth history, 촉각 history를 사용한다. 촉각은 합력·접촉 면적 비율·압력 중심(CoP) 특징으로 표현한다. 관절 목표각 29개를 출력하고 PD로 실행하며, 두 critic이 보상 그룹을 담당한다. [§3.1–2](https://arxiv.org/html/2609.28959v1)

## 접촉 단계별 보상

| 단계 | 목적 |
|---|---|
| Swing | 정상적인 발 이동을 착지 벌점과 구분 |
| PreLanding | 접촉 전 과도한 하강 속도·가속도 억제 |
| Landing | 착지 순간 힘과 양의 힘 증가, 구간 peak 억제 |
| Stance | 접촉 면적과 CoP 여유 확보, 급격한 CoP 이동 억제 |

단계는 힘·면적·발 운동과 착지 이력으로 판별한다. 고정 보행 시계로 발 순서를 지시하는 것과 다르다. [§3.3 및 Algorithm 1](https://arxiv.org/html/2609.28959v1)

## RBQ10 적용과 한계

추론: 현재 RBQ10의 발 접촉 합력과 collider 최저점만으로 **실제 접촉 면적이나 CoP를 측정했다고 할 수 없다**. 착지 전 감속과 충격 비용은 참고할 수 있지만, 면적·CoP 보상에는 대응 센서나 검증된 추정기가 필요하다. 본문 개념식과 부록 구현식의 gating·정규화도 함께 확인해야 한다.

## 연결

- [[2026-09-24 - TactileStep Source]] — 본문·부록 확인 범위.
- [[2025 - BeamDojo Sparse Foothold Locomotion]] — 발 지지의 기하학적 대리 측정.
- [[Open Stair Reward Design and Evaluation]] — 접촉 단계별 보상 적용.
- [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]] — RBQ10 관측 한계와 비교.
- [[index]] — 전체 문헌 카탈로그.
