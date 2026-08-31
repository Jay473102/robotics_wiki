---
type: source
status: ingested
created: 2026-09-01
updated: 2026-09-01
tags:
  - source
  - grasping
  - flow-matching
  - generative-models
sources:
  - raw/papers/2608.26076v1.pdf
---

# Fast Generative Grasping via Lie Group-Constrained MeanFlow (GraspMF)

## Source

- Raw file: `raw/papers/2608.26076v1.pdf` (arXiv:2608.26076v1 [cs.RO], 2026-08-26)
- Type: 논문 (arXiv preprint, IEEE journal 양식 12쪽)
- Date: 2026-08-26 (v1)
- Authors: S. Talha Bukhari, Yi Wei, Ruiqi Ni, Zachary Kingston, Aniket Bera (Purdue University)
- Evidence tier: A (논문 본문)

파일명이 arXiv ID 그대로다. 명명 규칙에 맞추려면 papers 디렉터리 안에서 `2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow.pdf`로 바꿔야 하지만 `raw/`는 읽기 전용이므로 사용자 승인 대기.

## TL;DR

Diffusion·flow 기반 generative grasping은 품질은 좋지만 수십~수백 NFE(network function evaluation)가 필요해 반응형 closed-loop 실행에 못 쓴다. 이 논문은 MeanFlow(평균 속도 예측)를 product Lie group $G = SO(3) \times \mathbb{R}^3$ 위에 정식화한 **GraspMF**로, 5 NFE 이하에서 ACRONYM 기준 SOTA diffusion/flow baseline과 대등하거나 더 좋은 grasp 품질을 15.5ms(T=5) / 6.3ms(T=1) latency로 달성한다 (최대 39배 speedup). 핵심은 미분 항이 전혀 없는 대수적 semigroup consistency loss + 시간 대각선에서의 Riemannian CFM anchor 결합이다.

## Key Content

- 문제: SE(3) grasp 분포 학습에서 iterative sampling이 병목. Consistency/shortcut model은 self-referential target이라 transport field와의 정렬이 약함. MeanFlow는 구간 평균 속도라는 잘 정의된 양을 예측.
- 정식화: $SE(3)$ 대신 bi-invariant metric이 존재하는 직적군 $SO(3) \times \mathbb{R}^3$ 사용. Endpoint parameterization $X_\theta(H, s, t) \to \hat{H}_1$에서 평균 속도와 flow map을 closed form으로 유도.
- 학습: (1) 시간 대각선 $s{=}t$에서 CFM anchor (데이터 분포에 고정), (2) semigroup identity $\Phi_{s,t} = \Phi_{r,t} \circ \Phi_{s,r}$를 stop-gradient consistency loss로 (covariant derivative, JVP 없음), (3) 보조 SDF regression으로 기하 grounding.
- 결과: ACRONYM ID SR 87.40% (T=5), OOD 71.73%, 모든 sampling budget에서 안정 (OOD SR 표준편차 1.63). Baseline은 low budget에서 붕괴 (SE3Dif T=1에서 6.65%).
- 실기: Franka Research 3 + SAM segmentation + VAMP RRT-Connect로 가정용 물체 3종 9~10/10 성공.

## Notes / Marginalia Check

PDF annotation 확인 완료: 하이퍼링크뿐, 사용자 필기·하이라이트 없음.

## Claims To Verify

- "최대 39× speedup"은 SE3Dif(600.1ms) 대비 T=5(15.5ms) 기준. VSIGD 대비로는 ~73×라서 abstract 수치가 보수적인 쪽.
- Concurrent work(Zhong et al., Riemannian MeanFlow ICML 2026)의 decomposed objective가 열등하다는 주장(Table III, SR −25.15pt)은 저자 자신의 재현 기반이므로 해당 논문 원문과 교차 확인 필요.
- 코드 공개 여부는 본문에 언급 없음.

## Promoted To Wiki Pages

- [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]] — paper 페이지.
- [[GraspMF Few-Step Grasp Generation]] — method 페이지.
- [[Generative Grasp Synthesis]] — 문제 영역 concept.
- [[Flow Matching]] — 기반 생성 모델 concept.
- [[MeanFlow]] — few-step 생성 concept.
- [[ACRONYM]] — benchmark 페이지.

## Open Questions

- 6.3ms 단일 스텝 추론이 실제 closed-loop replanning 성능 향상으로 이어지는가? 논문은 가능성만 언급 ("may achieve better performance").
- Semigroup identity가 회전 인자에서는 BCH bracket 항까지만 성립하는데, 큰 회전 chord에서 이 오차가 실제 성능에 미치는 영향은?
