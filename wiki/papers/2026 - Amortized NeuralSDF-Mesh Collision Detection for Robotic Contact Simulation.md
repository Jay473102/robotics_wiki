---
type: paper
status: draft
created: 2026-06-15
updated: 2026-06-15
tags:
  - collision-detection
  - neural-sdf
  - contact-simulation
  - amortized-optimization
  - differentiable-simulation
sources:
  - raw/papers/0c0760_a300ee12f6054b399ed0e4b4af409ca6.pdf
title: Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation
authors:
  - Jinhee Yun
  - Jeongmin Lee
  - Sunkyung Park
  - Dongjun Lee
year: 2026
venue: 검증 필요
doi:
url:
---

# Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation

## TL;DR

NeuralSDF는 non-convex geometry를 연속적이고 메모리 효율적으로 표현하지만, collision detection에서 반복적으로 query하면 느리다. 이 논문은 NeuralSDF-triangle collision을 constrained optimization으로 쓰고 KKT 조건을 loss로 만든 amortized model을 학습해 contact point를 한 번의 forward pass로 예측한다. 결과적으로 NeuralSDF+Frank-Wolfe 대비 큰 속도 이득을 보이며, VoxelSDF보다 훨씬 적은 메모리로 복잡한 contact simulation을 처리할 수 있다고 주장한다.

## Problem

로봇 contact simulation, manipulation, planning에서는 non-convex object 사이의 collision detection이 병목이 된다. Analytic primitive나 convex mesh 기반 알고리즘은 복잡한 형상을 다루기 어렵고, VoxelSDF는 빠르지만 discretization artifact와 높은 메모리 비용이 있다.

NeuralSDF는 continuous signed distance field와 category-level generalization을 제공하지만, SDF query가 neural network forward pass라서 iterative collision optimization과 결합하면 느리다. 논문은 이 query inefficiency가 NeuralSDF를 time-sensitive robotics simulation에 쓰기 어렵게 만든다고 본다.

## Core Idea

NeuralSDF-mesh collision을 mesh 전체에서 직접 풀지 않고 triangle 단위 NeuralSDF-triangle collision으로 나눈다. 각 triangle에서 barycentric coordinate $\alpha,\beta,\gamma$를 최적화해 signed distance가 최소인 점 $p=\alpha v_1+\beta v_2+\gamma v_3$를 찾는다.

이 최적화 문제의 KKT 조건을 유도한 뒤, 그 조건을 만족하는 contact point를 neural network가 직접 예측하게 한다. 즉 반복 최적화의 해를 매번 계산하는 대신, 최적화 해를 amortized prediction으로 근사한다.

관련 페이지:

- [[NeuralSDF Collision Detection]]
- [[Amortized NeuralSDF-Mesh Collision Detection]]
- [[Differentiable Dynamics]]

## Method

논문은 NeuralSDF-triangle collision을 다음 제약 최적화로 정식화한다.

$$
\min_{\alpha,\beta,\gamma} f_{\mathrm{SDF}}(\alpha v_1+\beta v_2+\gamma v_3)
$$

$$
\mathrm{s.t.}\quad \alpha+\beta+\gamma=1,\quad \alpha,\beta,\gamma \ge 0
$$

여기서 $v_1,v_2,v_3$는 triangle vertices이고, $p=\alpha v_1+\beta v_2+\gamma v_3$는 triangle 내부 contact candidate다. KKT 조건을 정리해 $p$가 최적해일 때의 gradient 조건을 만들고, 이를 optimality loss로 사용한다.

모델 구조는 auto-decoder 계열이다. vertex-level shape feature와 triangle-level shape feature를 함께 쓰고, shared MLP 구조로 vertex permutation에 equivariant하게 설계한다. shape feature는 dynamic code cloud를 사용하며, unseen object는 shape code만 최적화하고 network parameter는 고정하는 category-level generalization 흐름을 따른다.

## Data / Embodiment

- ShapeNet의 mug와 bottle category를 사용해 seen/unseen object generalization을 평가한다.
- Contact simulation 시나리오는 Mug-Rack, Bottle-Holder, Gear-Gear, Bolt-Nut이다.
- 첫 두 시나리오에는 Franka Emika Panda와 parallel gripper가 등장한다.
- Contact solver는 cascaded Newton-based augmented Lagrangian, CANAL 방법을 사용했다고 보고한다.

## Evaluation

비교 대상은 크게 세 가지다.

- `NeuralSDF + Ours`: 제안한 amortized collision detector.
- `NeuralSDF + FW`: NeuralSDF와 Frank-Wolfe iterative optimization.
- `VoxelSDF + FW`: VoxelSDF와 Frank-Wolfe iterative optimization.

평가 축은 triangle-level optimality와 계산 시간, object-level contact 수/시간/메모리, simulation-level stability, unseen object generalization, ablation이다.

## Results

- Triangle-level 평가에서 제안법은 triangle당 약 0.038 ms로 수렴한다고 보고하며, NeuralSDF+FW는 동일 optimality 수준에 5-11 iteration과 30-65 ms가 필요하다고 보고한다.
- Table II 기준 object-level scenario에서 NeuralSDF+Ours의 메모리는 약 60.8 MB로 보고되고, VoxelSDF+FW는 수 GB에서 18 GB 이상까지 올라간다.
- Mug-Rack, Bottle-Holder, Gear-Gear, Bolt-Nut simulation에서 NeuralSDF 기반 방법은 VoxelSDF보다 contact를 더 안정적으로 만든다고 보고한다.
- Seen/unseen mug와 bottle의 optimality 및 NME 차이가 크지 않아 category-level generalization이 가능하다고 주장한다.
- Ablation에서는 KKT 기반 optimality loss를 제거하면 성능이 크게 나빠져 핵심 구성요소임을 보인다.

## Limitations

- Learning-based predictor라서 training dataset의 triangle size 조건과 다른 mesh에서는 성능이 떨어질 수 있다. 논문은 remeshing을 적용 방안으로 제시한다.
- Contact prediction은 NeuralSDF 품질에 의존한다.
- High-precision contact가 필요한 작업에서는 제안법만으로 충분하지 않을 수 있고, NeuralSDF+FW의 warm start로 사용하는 hybrid refinement가 필요할 수 있다.
- 실험 category가 mug/bottle 중심이라 arbitrary object category에 대한 일반화는 추가 검증이 필요하다.
- 검증 필요: PDF 안에서 code release, dataset split, 학회/저널 peer-review 상태는 확인하지 못했다.

## Connections

- [[Differentiable Dynamics]]: NeuralSDF와 amortized model이 모두 differentiable하므로 gradient-based manipulation/planning에 연결될 수 있다.
- [[Physical AI]]: 고속 contact-rich simulation은 로봇 foundation model, sim-to-real, synthetic data loop의 하위 인프라로 중요하다.
- [[Robot Foundation Models]]: 직접 RFM 논문은 아니지만, 복잡한 물체 접촉을 빠르게 계산하는 simulator substrate로 연결될 수 있다.

## Contradictions / Updates

아직 위키 내 기존 페이지와 직접 충돌하는 주장은 없다. 다만 VoxelSDF 대비 장점은 이 논문 실험 설정의 triangle/object/contact scenario에 한정해 해석해야 한다.

## Notes / Marginalia

PDF annotation marker 검색에서 사용자 highlight/text/ink note는 확인하지 못했다.

## Open Questions

- NeuralSDF model 자체의 학습 비용과 contact detector 학습 비용까지 포함하면, 반복 최적화 baseline 대비 전체 연구/운영 비용은 어떻게 달라지는가?
- Contact solver가 요구하는 contact normal, penetration depth, friction cone 정보까지 학습 예측으로 안정적으로 제공할 수 있는가?
- Collision avoidance planning에서 false negative contact 예측의 위험을 어떻게 bound하거나 conservative하게 만들 수 있는가?
