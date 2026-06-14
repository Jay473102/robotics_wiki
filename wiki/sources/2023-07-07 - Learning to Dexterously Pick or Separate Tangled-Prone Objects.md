---
type: source
status: ingested
created: 2026-06-15
updated: 2026-06-15
tags:
  - source
  - paper
  - bin-picking
  - manipulation
sources:
  - raw/papers/2302.08152v2.pdf
---

# Learning to Dexterously Pick or Separate Tangled-Prone Objects Source

## Source

- Raw file: `raw/papers/2302.08152v2.pdf`
- Title: "Learning to Dexterously Pick or Separate Tangled-Prone Objects for Industrial Bin Picking"
- Authors: Xinyi Zhang, Yukiyasu Domae, Weiwei Wan, Kensuke Harada
- arXiv: `2302.08152v2 [cs.RO]`
- Date in PDF: 2023-07-07
- Project page in PDF: `https://xinyiz0931.github.io/tangle`

## Extraction Summary

이 논문은 얽힘이 쉬운 산업용 부품을 bin picking할 때, 단순히 집기 쉬운 물체만 찾는 대신 `picking`, `dropping`, `pulling` 행동을 계층적으로 선택하는 시스템을 제안한다.

핵심 구성은 [[Action Affordance Learning]] 기반의 `PickNet`과 `PullNet`이다. `PickNet`은 depth image에서 isolated object를 집을지, entangled object를 분리할지 판단하는 affordance map을 만든다. `PullNet`은 buffer bin 안에서 물체를 당길 위치와 방향을 예측한다.

## Evidence Notes

- PDF 초록은 real-world experiment에서 tangled-prone object picking success rate가 90%라고 보고한다.
- 학습 데이터는 physics simulator에서 algorithmic supervisor를 이용해 self-supervised 방식으로 수집한다.
- 실패 모드는 grasp failure, endless-chain 형태의 얽힘, tightly wedged objects, depth map noise, simulation-real contact mismatch로 정리된다.

## Created / Updated

- [[2023 - Learning to Dexterously Pick or Separate Tangled-Prone Objects]]
- [[Tangled-Prone Bin Picking]]
- [[Object Singulation]]
- [[Action Affordance Learning]]
