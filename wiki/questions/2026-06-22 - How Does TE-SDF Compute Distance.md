---
type: question
status: draft
created: 2026-06-22
updated: 2026-06-22
tags:
  - question
  - signed-distance-field
  - collision-detection
  - te-sdf
sources:
  - raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf
  - raw/notes/논문 학습 자료 요청.pdf
---

# How Does TE-SDF Compute Distance?

## Short Answer

TE-SDF의 거리 계산 핵심은 전체 mesh surface를 전부 검사하지 않고, query point가 들어 있는 tetrahedron에 미리 연결해 둔 후보 face 집합만 검사하는 것이다.

일반 SDF 거리 계산은 어떤 점 $x$에서 전체 표면 face 집합 $F$까지의 최소 거리다.

$$
d(x,F)=\min_{f\in F} d(x,f)
$$

TE-SDF는 tetrahedral mesh의 각 tetrahedron $t$마다, 그 안의 점에서 closest face가 될 가능성이 있는 face 집합 $E_t$를 미리 저장한다. 그러면 $x \in t$일 때 전체 $F$를 보지 않고 다음처럼 계산한다.

$$
d(x,F)=d(x,E_t)=\min_{f\in E_t} d(x,f)
$$

## Why This Question Matters

TE-SDF가 voxel SDF나 NeuralSDF와 다른 지점이 바로 거리 계산 방식이다. Voxel SDF는 grid 값 보간으로 빠른 query를 얻지만 memory cost가 커지고, NeuralSDF는 network inference로 compact representation을 얻지만 query overhead가 생긴다. TE-SDF는 tetrahedron별 후보 triangle에 대해 exact point-triangle distance를 계산해 memory와 query cost 사이의 다른 trade-off를 만든다.

## Current Answer

Runtime 거리 계산은 다음 순서로 볼 수 있다.

1. Query point $x$가 어느 tetrahedron $t$ 안에 있는지 찾는다.
2. 그 tetrahedron에 저장된 encoded face set $E_t$를 가져온다.
3. $E_t$ 안의 각 triangle face까지 point-triangle distance를 계산한다.
4. 그중 최소값을 unsigned distance로 사용한다.
5. $t$가 내부 tetrahedron이면 음수, 외부 tetrahedron이면 양수 부호를 붙여 SDF 값을 만든다.

SDF 값은 다음 형태다.

$$
\phi_G(x)=
\begin{cases}
-d(x,E_t), & t \in T_{BI}\cup T_I \\
+d(x,E_t), & t \in T_{BO}\cup T_O
\end{cases}
$$

여기서 중요한 점은 $E_t$가 임의의 face 모음이 아니라는 것이다. TE-SDF는 preprocessing 단계에서 각 face $f$가 tetrahedron $t$ 내부의 어떤 점에서 closest face가 될 수 있는지 판정한다.

이를 위해 gap function을 쓴다.

$$
g_f(x)=d(x,f)-d(x,F)
$$

어떤 $x \in \mathrm{int}(t)$에서 $g_f(x)=0$이면, face $f$는 그 점에서 전체 surface 중 closest face가 될 수 있으므로 $E_t$에 포함된다.

## Encoding-Time Acceleration

모든 face를 모든 tetrahedron에 대해 직접 검사하면 비싸다. TE-SDF는 다음 방식으로 encoded face set을 만든다.

- Lipschitz pruning: 너무 멀어서 closest face가 될 수 없는 face를 빠르게 제거한다.
- GPU sampling: 남은 후보 face에 대해 tetrahedron 내부 sample point에서 gap function을 평가한다.
- Distance-ordered truncation: 필요하면 $E_t$의 face 수를 $E_{\max}$로 제한한다.

Distance-ordered truncation은 memory와 runtime을 줄일 수 있지만, deep interior SDF accuracy를 낮출 수 있다. Collision detection에서는 near-surface exactness가 특히 중요하므로, 표면 근처 거리 정확도를 우선한다.

## Evidence / Sources

- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]: TE-SDF를 tetrahedron별 encoded face set과 localized exact distance evaluation으로 설명한다.
- [[Tetra-Encoded Signed Distance Field]]: $d(x,F)=d(x,E_t)$ 관계와 encoded face set 개념을 정리한다.
- [[TE-SDF Collision Detection]]: Node-TES, Face-TES runtime query와 GPU 구현 관점을 정리한다.
- [[2026-06-21 - TE-SDF Learning Material]]: SDF, tetramesh, gap function, Lipschitz pruning, Node-TES/Face-TES를 설명하는 2차 학습 자료다.

## Important Caveats

TE-SDF의 distance query는 exact point-triangle distance를 사용하지만, encoded face set이 충분히 보존된다는 전제가 필요하다. Sampling density, tetrahedralization quality, exterior tetrahedral region, truncation setting이 잘못되면 SDF error가 생길 수 있다.

## Linked Pages

- [[Tetra-Encoded Signed Distance Field]]
- [[TE-SDF Collision Detection]]
- [[Signed Distance Field Collision Detection]]
- [[2026 - TE-SDF Tetra-Encoded Signed Distance Field]]
