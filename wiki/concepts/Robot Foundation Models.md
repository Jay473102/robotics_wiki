---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - robot-foundation-models
  - physical-ai
  - vla
sources:
  - raw/notes/deep-research-report.md
---

# Robot Foundation Models

## Definition

Robot Foundation Models, 또는 RFM은 다양한 로봇 작업, 환경, embodiment에 걸쳐 재사용 가능한 perception-action prior를 학습하려는 모델 계열이다. 원자료 보고서에서는 LG CNS PhysicalWorks Forge가 RFM 학습용 데이터 파이프라인과 simulation 검증 루프를 제공한다고 설명한다.

## Why It Matters

로봇 학습은 데이터 수집 비용과 현장 검증 비용이 크다. RFM은 task별 개별 모델보다 더 넓은 일반화와 fine-tuning 효율을 목표로 하지만, 실제 현장에서는 data governance, embodiment mismatch, safety validation, deployment loop가 병목이 된다.

## Key Ideas

- Multimodal data: vision, language, proprioception, action, human video, teleoperation.
- Embodiment transfer: 다른 로봇 하드웨어 사이의 action representation 차이를 줄이는 문제.
- Simulation and synthetic data: real data 부족을 보완하지만 sim-to-real 검증이 필요하다.
- Operations feedback: 배포 후 실패/예외 데이터를 다시 학습 데이터로 환류한다.

## Related Concepts

- [[Vision-Language-Action Models]]
- [[Physical AI]]
- [[Robot Fleet Orchestration]]

## Open Questions

- RFM에서 foundation model의 범위는 perception encoder, action policy, world model, planner 중 어디까지인가?
- 현장 SI 플랫폼은 RFM 학습 데이터의 품질과 provenance를 어떤 방식으로 관리해야 하는가?
