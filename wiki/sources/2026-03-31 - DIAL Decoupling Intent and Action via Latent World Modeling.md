---
type: source
status: ingested
created: 2026-06-15
updated: 2026-06-15
tags:
  - source
  - paper
  - vla
  - latent-world-modeling
  - robot-foundation-models
sources:
  - raw/papers/260329844v1 1_260615_004135.pdf
---

# DIAL Source

## Source

- Raw file: `raw/papers/260329844v1 1_260615_004135.pdf`
- Title: "DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA"
- Authors: Yi Chen, Yuying Ge, Hui Zhou, Mingyu Ding, Yixiao Ge, Xihui Liu
- arXiv: `2603.29844v1 [cs.RO]`
- Date in PDF: 2026-03-31
- Project page in PDF: `https://xpeng-robotics.github.io/dial`

## Extraction Summary

DIAL은 end-to-end VLA에서 VLM을 단순 encoder로 쓰는 대신, System-2가 VLM-native ViT feature space 안에서 미래 latent foresight를 예측하고, System-1이 이 latent intent와 현재 관측을 비교해 action chunk를 생성하도록 만든다. 이 differentiable latent intent bottleneck이 high-level intent와 low-level motor control을 구조적으로 연결한다는 주장이다.

## Evidence Notes

- RoboCasa GR1 Tabletop simulation 24개 task에서 full-data 평균 success rate 70.2%를 보고한다.
- Few-shot setting에서는 task당 100 trajectory로 58.3%를 보고하며, 논문은 기존 full-data baseline보다 적은 demonstration으로 높은 성능을 냈다고 주장한다.
- Human demonstrations는 EgoDex `basic_pick_place` subset 27,419 trajectories와 real-world pour subset 3,205 trajectories를 사용한다.
- Real-world IRON-R01-1.11 robot 실험에서 decoupled warmup과 human data가 OOD robustness에 중요하다고 보고한다.

## Notes / Marginalia Check

PDF annotation을 확인했지만 사용자 highlight, text note, ink note는 없었고 `/Link` annotation만 존재했다. 본문에는 Q1-Q5 research questions가 명시되어 있어, 이 질문들을 사용자 위키의 재사용 질문으로 승격했다.

## Created / Updated

- [[2026 - DIAL Decoupling Intent and Action via Latent World Modeling]]
- [[Latent World Modeling]]
- [[Vision-Language-Action Models]]
- [[2026-06-15 - How Should VLA Models Bridge Intent and Action]]
