---
type: source
status: ingested
created: 2026-11-03
updated: 2026-11-03
tags: [source, reinforcement-learning, manipulation, contact-simulation]
sources:
  - raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf
  - https://arxiv.org/abs/2610.13354v1
  - https://alpha-nist.github.io/
---

# AlphaNIST Source

AlphaNIST는 다양한 reset 상태와 성공률 기반 sampling을 이용해, 조립 완료 보상을 받는 다중 과제 정책을 학습한다. 결과는 **시뮬레이션**에 한정되며, 20개 단일 부품 과제의 학습 성공률과 별도 정책의 10개 부품 조립 성공률을 구분해야 한다.

## Source

- 제목: *AlphaNIST: Emergent Assembly Skills from Binary Task Rewards*.
- 저자: Octi Zhang 외 14명; NVIDIA / University of Washington. 전체 명단은 [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]].
- 발행: arXiv:2610.13354v1, 2026-10-09. 2026-11-03 확인 시 v1만 등재되어 있다.
- 원본: `raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf`.
- 수집: 사용자가 지정한 [공식 프로젝트](https://alpha-nist.github.io/)에서 논문을 식별한 뒤 [arXiv v1 PDF](https://arxiv.org/pdf/2610.13354v1)를 다운로드했다. 8쪽, 25,142,546 bytes. 원본 바이트를 수정하지 않았다.
- SHA-256: `96f23d6034c91718549214705cee7bd9458b6ae6149ba5e0cf242ade8641f83c`.
- Evidence tier: **A** — 저자 논문과 공식 프로젝트. 결과 수치는 저자 보고이며 독립 재현 결과가 아니다.
- arXiv 라이선스: CC BY 4.0. 원문·저자 출처를 위에 명시하며, 아래 위키 문서는 한국어 요약 및 별도 표시한 해석이다.
- Venue: arXiv comments에 ICRA라고 적혀 있으나, 이 표기만으로 학회 채택·발표를 확정하지 않는다.

## Key Content

| 원문 위치 | 확인한 내용 | 해석 경계 |
|---|---|---|
| §IV-B, Eqs. (3)–(4) | OmniReset 상태 bank와 성공률 기반 beta sampling | reset 상태는 시범 궤적이 아니지만 초기화 설계는 존재함 |
| §IV-C, Eqs. (5)–(6) | 완료 시 1회 보상 + 매 스텝 action·관절 속도·토크 비용 | 총 보상 전체가 0/1인 것은 아님 |
| §V-A, Figs. 5–6 | 공유 sparse 정책 98.2%, 분리 sparse 정책 평균 81.4% | 64K 환경, 25K iteration의 학습 성공 비교 |
| §V-B, Fig. 7 | 256K 환경 sparse beta 97.4%, uniform 84.3% | 고정 mixed-reset bank 평가; 실물·미지 과제 평가가 아님 |
| §V-D, Table I | 10개 active pair 정책의 episode 성공률 84% | 부품 수마다 별도 학습·평가; 20개 전체 보드 완료와 다름 |
| §VI | 모든 결과는 simulation; 실물 이전과 20개 연속 조립은 향후 과제 | hardware 속도·토크 제약만으로 sim-to-real 성공을 주장할 수 없음 |

## Notes / Marginalia Check

- 사용자가 필기한 파일이 아니라 공개 arXiv 원본을 수집했다.
- PDF의 압축 객체 stream 4개를 포함해 annotation subtype을 확인했다. `/Link` 81개를 찾았고, `/Text`, `/Highlight`, `/Ink`, `/FreeText`, `/Underline` 등 필기·강조 annotation은 발견하지 못했다.
- PDF 텍스트를 추출하고 정책 구조·보상 수식이 있는 페이지를 렌더링해 확인했다. 링크 annotation을 사용자 메모로 취급하지 않았다.

## Claims To Verify

- 공식 구현: 논문 §I는 검토·수정 기간 이후 공개 예정이라고 적었다. 2026-11-03 확인한 프로젝트·논문에서 공식 구현 링크를 찾지 못했다. 제3자 구현을 공식 코드로 취급하지 않는다.
- 센서 기반 관측, 지연·접촉 모델 오차에 대한 실물 성능은 미검증이다.
- dense shaping 열위는 논문이 시험한 reach/alignment 항과 계수에 관한 결과이며, 모든 shaping 설계에 대한 결론이 아니다.

## Promoted To Wiki Pages

- [[index]] — 이 원자료와 파생 문서의 카탈로그.
- [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]] — 논문 방법·평가·한계.
- [[AlphaNIST Binary-Reward Assembly]] — 학습 및 제어 절차.
- [[Reset-State Curricula for Sparse-Reward RL]] — reset coverage와 sampling의 구분.
- [[NIST Assembly Task Board 1]] — 과제·성공 판정·평가 조건.
- [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]] — 조립 결과를 다른 RL 문제에 적용할 때의 질문.

## Open Questions

- near-complete reset을 포함한 혼합 초기 상태 평가와, 모든 부품을 테이블에서 집어 시작하는 평가는 얼마나 다른가?
- 접촉·센서 오차를 넣어도 emergent regrasp와 threading이 유지되는가?
