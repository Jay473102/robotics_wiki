---
type: synthesis
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - industry
  - physical-ai
  - robot-foundation-models
  - robot-operations
sources:
  - raw/notes/deep-research-report.md
---

# LG CNS PhysicalWorks

## Executive Summary

원자료 보고서 기준 [[LG CNS PhysicalWorks]]는 로봇의 학습과 운영을 같은 브랜드 아래 묶는 산업형 Physical AI 플랫폼이다. `Forge`는 데이터 수집, 큐레이션, RFM/VLA/RL 학습, simulation 검증을 담당하고, `Baton`은 이기종 로봇과 설비를 workflow 단위로 운영하는 관제/오케스트레이션 계층으로 정리된다.

가장 중요한 해석은 "로봇 모델 자체"보다 "학습 루프와 현장 운영 루프를 SI 역량으로 묶는 상용화 프레임"이라는 점이다.

## Current Picture

보고서는 PhysicalWorks를 다음 구조로 본다.

- 학습 계층: [[Robot Foundation Models]], [[Vision-Language-Action Models]], 강화학습, simulation, teleoperation/human video data.
- 운영 계층: [[Robot Fleet Orchestration]], WMS/MES/설비 연계, work order, robot status, CCTV/sensor fusion.
- 피드백 루프: 현장 예외와 KPI를 다시 데이터 선별과 재학습으로 연결.

## Evidence

원자료 보고서에 따르면 LG CNS는 Forge/Baton의 공개 기능, PoC, 부산 스마트시티 적용, 컬리 물류센터 실증, Skild AI/Dexmate/Config 관련 협력 등을 언급한다.

검증 필요: 저장된 raw markdown의 citation이 외부 URL이 아니라 채팅 내부 참조라서, 이 synthesis는 일단 2차 보고서 기반 정리다. 공식 보도자료와 제품 페이지 URL을 확보하면 `sources`와 evidence section을 갱신해야 한다.

## Comparison

보고서는 경쟁 비교군을 두 축으로 나눈다.

- Forge 유사: NVIDIA Isaac GR00T/Isaac Sim 같은 robot foundation model, simulation, synthetic data 생태계.
- Baton 유사: InOrbit, Formant, SVT Robotics, 클로봇 CROMS 같은 robot operations/fleet orchestration 플랫폼.

해석: PhysicalWorks의 차별점은 학습과 운영을 한 스토리로 묶는 점이고, 약점은 공개 스펙이 적어 기술 실사가 어렵다는 점이다.

## Implications

- 산업용 Physical AI의 병목은 모델 성능만이 아니라 데이터 수집, 검증, 현장 integration, 운영 KPI, 안전/보안이다.
- RFM/VLA가 실제 현장에 들어가려면 Forge 같은 데이터/검증 계층과 Baton 같은 운영 계층이 연결되어야 한다.
- 구매자 관점에서는 공개 데모보다 PoC metric, interface contract, data governance, cyber/OT security를 확인해야 한다.

## What To Watch

- 컬리 물류센터 PoC에서 작업 정확도, 수행 속도, 기존 방식 대비 효율 개선이 공개되는지.
- Forge의 데이터 포맷, API, supported embodiments가 공개되는지.
- Baton의 fleet control latency, safety boundary, WMS/MES integration 방식이 공개되는지.
- 국내 AI 기본법, 개인정보/영상정보, 산업용 로봇 안전, OT 보안 기준과 제품 기능이 어떻게 연결되는지.
