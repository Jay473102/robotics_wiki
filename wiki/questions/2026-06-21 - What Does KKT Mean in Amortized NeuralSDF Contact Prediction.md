---
type: question
status: draft
created: 2026-06-21
updated: 2026-06-21
tags:
  - question
  - optimization
  - neural-sdf
  - collision-detection
sources:
  - raw/chats/내용 파악 요약.pdf
  - raw/papers/2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation.pdf
---

# What Does KKT Mean in Amortized NeuralSDF Contact Prediction?

## Short Answer

KKT condition은 제약조건이 있는 최적화 문제에서 "이 점이 제약 영역 안에서 더 이상 좋아질 수 없는 최적점인가"를 판정하는 조건이다. Amortized NeuralSDF-mesh collision에서는 삼각형 내부의 점 중 NeuralSDF 값이 최소가 되는 contact point를 찾아야 하므로, KKT condition을 contact point optimality의 label-free supervision signal로 쓴다.

## Why This Question Matters

이 논문의 핵심은 Frank-Wolfe 같은 반복 최적화로 매번 contact point를 찾는 대신, neural network가 한 번의 forward pass로 contact point를 예측하게 만드는 것이다. KKT condition은 그 예측점이 최적해에 가까운지 검사하는 수학적 기준이다.

## Current Answer

삼각형 꼭짓점이 $v_1,v_2,v_3$일 때 삼각형 내부 점은 barycentric coordinate로 쓴다.

$$
p=\alpha v_1+\beta v_2+\gamma v_3
$$

제약조건은 다음이다.

$$
\alpha+\beta+\gamma=1,\quad \alpha,\beta,\gamma \ge 0
$$

NeuralSDF-triangle collision은 삼각형 위에서 $f_{\mathrm{SDF}}(p)$를 최소화하는 문제로 볼 수 있다. KKT condition은 이 constrained optimization의 최적점이 만족해야 하는 stationarity, primal feasibility, dual feasibility, complementary slackness 조건을 제공한다.

논문은 이 조건을 정리해 예측된 contact point가 최적점에 가까운지 재는 optimality loss로 사용한다. 따라서 정답 contact point label을 미리 만들지 않아도, 네트워크가 "반복 최적화로 얻어야 할 점"을 직접 예측하도록 학습할 수 있다.

## Evidence / Sources

- [[2026 - Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation]]: NeuralSDF-triangle collision을 constrained optimization으로 정식화하고 KKT 기반 optimality loss를 사용한다.
- [[2026-06-15 - Amortized NeuralSDF KKT Explanation Chat]]: KKT, posterior, amortized neural network의 차이를 사용자가 이해하기 쉽게 풀어 설명한 secondary chat source다.

## Important Caveats

Chat 설명은 secondary source다. KKT 식의 부호, transpose, active set convention은 원 논문 수식으로 확인해야 한다.

## Linked Pages

- [[Amortized NeuralSDF-Mesh Collision Detection]]
- [[NeuralSDF Collision Detection]]
- [[Differentiable Dynamics]]
