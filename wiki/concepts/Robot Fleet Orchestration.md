---
type: concept
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - fleet-management
  - robot-operations
  - industrial-automation
sources:
  - raw/notes/deep-research-report.md
---

# Robot Fleet Orchestration

## Definition

Robot fleet orchestration은 여러 종류의 로봇, 설비, 작업 지시, 현장 센서를 하나의 운영 workflow로 묶어 작업 할당, 경로/동선 최적화, 예외 대응, KPI 관제를 수행하는 계층이다.

## Why It Matters

로봇이 한두 대를 넘어 제조/물류 현장에 다수 배치되면 개별 로봇의 autonomy보다 전체 throughput, congestion, downtime, safety, WMS/MES 연계가 더 중요해진다.

## Key Ideas

- Heterogeneous fleet: AMR, AGV, 모바일 매니퓰레이터, 사족/이족 로봇, 고정 설비를 함께 다룬다.
- Work order integration: WMS/MES/ERP/설비 시스템의 지시를 로봇 실행 계획으로 변환한다.
- Real-time operations: robot state, location, CCTV, sensor, facility state를 보고 예외를 처리한다.
- Optimization: 작업 배분, 충돌/혼잡 회피, 동선 최적화, priority scheduling.

## Related Pages

- [[LG CNS PhysicalWorks]]
- [[Physical AI]]
- [[Robot Foundation Models]]

## Open Questions

- Fleet orchestration이 저수준 motion control까지 책임져야 하는가, 아니면 task allocation과 monitoring에 머물러야 하는가?
- 다중 제조사 로봇을 연결할 때 표준 interface와 vendor-specific adapter의 경계는 어디인가?
