---
type: entity
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - lg-cns
  - physical-ai
  - robot-foundation-models
  - robot-operations
sources:
  - raw/notes/deep-research-report.md
entity_type: product-platform
---

# LG CNS PhysicalWorks

## Snapshot

PhysicalWorks는 원자료 보고서 기준 LG CNS의 RX(Robot Transformation) 플랫폼 브랜드다. 보고서는 하위 구성요소를 `PhysicalWorks Forge`와 `PhysicalWorks Baton`으로 구분한다. Forge는 로봇 학습 데이터와 RFM 학습/검증 루프, Baton은 이기종 로봇 운영/관제와 workflow orchestration을 담당하는 것으로 정리한다.

검증 필요: 원자료의 외부 citation이 채팅 내부 참조 형태라 공식 URL과 보도자료 원문을 별도로 재확인해야 한다.

## Product / Platform

- `PhysicalWorks Forge`: 인간 작업 데이터, 실제 현장 데이터, simulation/world model 데이터를 결합해 [[Robot Foundation Models]] 또는 VLA/RL 정책 학습에 쓰는 데이터 파이프라인으로 설명된다.
- `PhysicalWorks Baton`: WMS/MES/설비/센서/CCTV/로봇 상태를 하나의 workflow로 묶어 작업 할당, 동선 최적화, 예외 대응, KPI 관제를 수행하는 계층으로 설명된다.
- 보고서는 `Physical Pose`라는 표현은 공식 명칭으로 확인되지 않았고 `PhysicalWorks Forge`를 잘못 들었을 가능성이 높다고 정리한다.

## Technical Claims

- Forge: data collection, automatic data quality control, simulation validation, retraining loop.
- Baton: heterogeneous robot fleet operation, real-time monitoring, mathematical optimization, agentic AI 기반 실행 계획.
- Learning-operation feedback loop: 운영 중 발생한 예외와 현장 데이터를 다시 학습 데이터로 환류.

검증 필요: API, SDK, ROS 2/VDA5050 지원 여부, 데이터 포맷, 센서 BOM, latency/SLA, 정확도, 가격, 보안 아키텍처는 보고서도 공개 자료에서 확인 불가로 표시한다.

## Evidence

현재 이 페이지의 근거는 [[2026-06-15 - LG CNS PhysicalWorks Deep Research Report]]와 `raw/notes/deep-research-report.md`다. 원문 보고서는 여러 공식/비공식 자료를 조사한 2차 보고서이지만, 저장된 markdown에는 실제 URL이 남아 있지 않다.

## Market / Deployment

보고서가 언급하는 사례:

- 20곳 이상 고객사 PoC.
- 부산 스마트시티에서 순찰, 바리스타, 짐캐리, 청소 로봇 통합 관제.
- 컬리 물류센터 휴머노이드 PoC 협약.
- 보안, 물류, 제조, 데이터센터 vertical 확장.

검증 필요: 위 사례의 날짜, 계약 범위, 실제 운영 성과 수치.

## Related Entities

- LG CNS
- Skild AI
- Dexmate
- Config

## Related Concepts

- [[Physical AI]]
- [[Robot Foundation Models]]
- [[Robot Fleet Orchestration]]
- [[Vision-Language-Action Models]]

## Open Questions

- Forge가 실제로 어떤 robot data schema와 training stack을 지원하는가?
- Baton은 fleet management 표준이나 기존 WMS/MES와 어떤 integration contract를 제공하는가?
- PoC에서 측정되는 success metric은 작업 정확도, cycle time, downtime, 운영비 중 무엇인가?
