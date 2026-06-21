---
type: source
status: ingested
created: 2026-06-21
updated: 2026-06-21
tags:
  - source
  - learning-note
  - signed-distance-field
  - collision-detection
sources:
  - raw/notes/논문 학습 자료 요청.pdf
source_kind: llm-generated-learning-material
---

# TE-SDF Learning Material Source

## Source

- Raw file: `raw/notes/논문 학습 자료 요청.pdf`
- Title in PDF metadata: "논문 학습 자료 요청"
- Author in PDF metadata: ChatGPT Deep Research
- Date in filesystem: 2026-06-21
- Source type: LLM-generated learning material / secondary explanatory note

## TL;DR

이 자료는 [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]를 바탕으로 SDF, tetramesh, TE-SDF encoding, Lipschitz pruning, distance-ordered truncation, Node-TES, Face-TES, cosine filter를 한국어로 설명한 학습용 2차 자료다. Primary source가 아니므로 수치와 주장 확정에는 원 논문을 우선 사용한다.

## Useful Explanations

- TE-SDF의 핵심을 "테트라 내부에서 후보 face set $E_t$만 사용해 SDF를 계산한다"는 관점으로 정리한다.
- Gap function $g_f(x)=d(x,f)-d(x,F)$와 후보 face 판정 문제를 단계적으로 설명한다.
- Node-TES와 Face-TES의 차이를 contact 처리 관점에서 설명한다.
- Cosine filter가 spurious contact feature를 제거하는 이유를 직관적으로 설명한다.

## Claims To Verify

- "충돌 검출 시간은 몇 밀리초 수준" 같은 성능 요약은 원 논문 Table II 기준으로 확인해야 한다.
- Deformation 대응 설명은 원 논문 Appendix/본문 범위와 정확히 맞는지 추가 확인이 필요하다.

## Promoted To Wiki Pages

- [[Tetra-Encoded Signed Distance Field]]
- [[TE-SDF Collision Detection]]
- [[Signed Distance Field Collision Detection]]

## Open Questions

- 이 학습 자료의 수식 번호와 원 논문 수식 번호가 모두 일치하는가?
- Cosine filter 설명을 실제 구현 pseudo-code와 연결해 별도 method note로 확장할 필요가 있는가?
