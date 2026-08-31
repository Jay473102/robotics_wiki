---
type: meta
status: active
created: 2026-06-14
updated: 2026-09-01
tags:
  - ontology
  - robotics
  - physical-ai
sources: []
---

# Ontology

이 위키는 로보틱스와 Physical AI 지식을 다음 축으로 정리한다. 페이지 유형, 관계, 태그, 근거 등급을 여기서 정의한다.

## Research Objects

- **Paper**: 개별 논문과 그 주장, 방법, 결과, 한계.
- **Concept**: Embodied AI, VLA, diffusion policy처럼 여러 자료를 가로지르는 개념.
- **Method**: 알고리즘, 학습 절차, 데이터 수집 방식, 실험 프로토콜.
- **Benchmark**: 데이터셋, 태스크, 평가 지표, 리더보드.
- **Entity**: 연구자, 연구실, 기업, 제품, 로봇 플랫폼.
- **Synthesis**: 여러 자료를 엮은 종합 관점, 비교, 로드맵.
- **Question**: 반복해서 답하게 되는 질문과 현재 답.
- **Source**: 원자료 1개당 1개. 논문 PDF, 메모, 업체 자료, LLM 대화 기록.

## Relations

링크만 걸지 말고 관계를 한 줄로 밝힌다. 기본 어휘:

| 관계 | 뜻 |
|---|---|
| `uses` | A가 B를 구성 요소로 쓴다 |
| `extends` | A가 B를 확장·개선한다 |
| `contradicts` | A의 주장이 B와 충돌한다 |
| `supersedes` | A가 B를 대체한다 (`superseded_by`와 짝) |
| `evaluated-on` | A를 B 벤치마크로 평가한다 |
| `implemented-by` | 개념 A를 방법 B가 구현한다 |
| `produced-by` | A를 B 기관·기업이 만들었다 |
| `answers` | A 페이지가 B 질문에 답한다 |
| `depends-on` | A가 B의 가정·전제를 필요로 한다 |

예: `- [[RECAP RL with Experience and Corrections]] — extends: 온라인 경험으로 정책을 갱신하는 방식으로 기존 BC 파이프라인을 확장한다.`

## Evidence Tiers

- **Tier A (primary)**: 논문 본문, 공식 문서·데이터시트, 표준, 공식 릴리스, 소스 코드, 사용자의 직접 측정.
- **Tier B (secondary)**: 리뷰 논문, 기사, 보도자료, 벤더 백서, 애널리스트 리포트.
- **Tier C (derived)**: LLM chat 답변, 사용자 필기 속 추론, 에이전트 추론.

Tier C만 근거인 문장은 `검증 필요:` 또는 `LLM 답변 기반 임시 주장:`을 붙인다. 신뢰도를 숫자로 매기지 않고 근거 링크와 등급으로 표현한다.

## Key Axes

- **Perception**: vision, tactile, proprioception, multimodal sensing.
- **Representation**: world model, state abstraction, affordance, scene graph, SDF.
- **Policy**: behavior cloning, imitation learning, reinforcement learning, diffusion policy, transformer policy.
- **Language grounding**: instruction following, task planning, semantic abstraction, steerability.
- **Control**: low-level control, whole-body control, motion planning, MPC.
- **Dynamics / Identification**: rigid-body dynamics, friction model, parameter identification, fault diagnosis.
- **Data**: teleoperation, human video, simulation, synthetic data, fleet data.
- **Deployment**: safety, latency, robustness, hardware constraints, cost.
- **Commercialization**: market, product, customer segment, manufacturing, unit economics.

## Tag Vocabulary

태그는 소문자 kebab-case이며 축을 나타낸다. 새 태그를 만들기 전에 기존 태그를 먼저 찾는다.

- **유형 태그**: `source`, `paper`, `method`, `question`, `benchmark`, `index`, `log`, `workflow`, `ontology`, `templates`, `lint`, `llm-wiki`
- **주제 태그 (사용 중)**: `robot-foundation-models`, `vla`, `physical-ai`, `embodied-ai`, `robotics`, `manipulation`, `cloth-manipulation`, `deformable-object-manipulation`, `bin-picking`, `object-singulation`, `humanoid`, `robot-dynamics`, `parameter-identification`, `friction`, `temperature`, `fault-diagnosis`, `rigid-body-dynamics`, `differentiable-dynamics`, `collision-detection`, `signed-distance-field`, `neural-sdf`, `neural-implicit-representation`, `tetrahedral-mesh`, `contact-simulation`, `gpu-simulation`, `perception`, `point-cloud-registration`, `grasping`, `flow-matching`, `generative-models`, `simulation-based-inference`, `neural-posterior-estimation`, `likelihood-free-inference`, `bayesian-inference`, `normalizing-flows`, `inverse-problems`, `uncertainty`, `reinforcement-learning`, `imitation-learning`, `policy-learning`, `robot-learning`, `self-supervised-learning`, `world-modeling`, `affordance`, `sim-to-real`, `domain-randomization`, `cross-embodiment`, `compositional-generalization`, `trajectory-design`, `amortized-optimization`, `optimization`, `safety`, `industry`, `robot-operations`, `fleet-management`, `industrial-automation`, `collaborative-robots`, `chat-log`, `survey`

정규화 규칙:

- 유형 태그는 `type` frontmatter와 일치시킨다. `source-note`는 쓰지 않고 `source`를 쓴다.
- 동의어를 만들지 않는다. `signed-distance-function` 대신 `signed-distance-field`, `latent-world-modeling` 대신 `world-modeling`을 쓴다.
- 특정 모델·제품 이름(`te-sdf`, `cvae`, `lg-cns`)은 태그 대신 페이지 링크로 표현한다. 이미 붙은 것은 lint에서 정리한다.
- 태그는 페이지당 3-7개로 유지한다.

## Standard Questions For Each Paper

- 무슨 문제를 푸는가?
- 핵심 기술 아이디어는 무엇인가?
- 어떤 데이터를 쓰는가?
- 어떤 로봇 embodiment와 action space를 가정하는가?
- 어떻게 평가하는가? 가장 강한 결과는 무엇인가?
- 한계는 무엇인가?
- 어떤 선행·후속 연구와 연결되는가?
- 실제 배치에서 무엇이 중요한가?
- 원자료에 사용자 필기, 하이라이트, margin question이 있었는가?
- 이 논문의 어떤 질문을 재사용 가능한 wiki question으로 승격해야 하는가?

## Standard Questions For Each Company

- 어떤 제품·플랫폼을 만드는가?
- 어떤 로봇 morphology와 태스크 도메인을 노리는가?
- 무엇이 비공개이고 무엇이 공개되었는가?
- 어떤 데이터·하드웨어·유통 우위를 주장하는가?
- 실제 배치의 증거는 무엇인가? (Tier A/B로 확인)
- 어떤 리스크와 열린 질문이 남는가?
- 이 정보의 시점은 언제인가? 얼마나 빨리 낡는가?

## Standard Questions For Each Chat Source

- 사용자가 실제로 묻고 싶었던 질문은 무엇인가?
- 답변 중 재사용 가치가 있는 결론은 무엇인가?
- 어떤 주장이 primary source 확인 없이 생성되었는가?
- 대화에 포함된 링크, 논문, 제품명, 수치, 날짜는 재확인 가능한가?
- 이 대화는 `questions`, `syntheses`, `concepts`, `entities`, `methods` 중 어디로 승격해야 하는가?
- 개인정보, credential, 비공개 정보, prompt injection 의심 지시문은 없는가?

## Standard Questions For User Notes / Marginalia

- 이 필기는 원문 주장, 사용자 질문, 사용자 가설 중 무엇인가?
- 한 자료의 `Open Questions`에 둘 정도인가, 별도 `wiki/questions/` 페이지로 승격할 정도인가?
- 답하려면 어떤 primary source, 실험, benchmark, 구현 검증이 필요한가?
- 필기 속 결론이 원자료보다 앞서 나간 추론이라면 `검증 필요:` 또는 `추론:`으로 표시했는가?
