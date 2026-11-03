---
type: log
status: active
created: 2026-06-14
updated: 2026-11-03
tags:
  - log
sources: []
---

# Wiki Log

append-only 운영 로그다. 최신 항목이 위에 온다. 형식은 `AGENTS.md`의 Logging Format을 따른다.

## [2026-09-01] ingest | GraspMF Lie group MeanFlow grasping

- Input: `raw/papers/2608.26076v1.pdf` (arXiv:2608.26076v1, 2026-08-26, "Fast Generative Grasping via Lie Group-Constrained MeanFlow", Purdue)
- Changed: source note [[2026-08-26 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]]와 paper 페이지 [[2026 - Fast Generative Grasping via Lie Group-Constrained MeanFlow]]를 추가했다. `wiki/methods/GraspMF Few-Step Grasp Generation.md`, `wiki/concepts/Flow Matching.md`, `wiki/concepts/MeanFlow.md`, `wiki/concepts/Generative Grasp Synthesis.md`, `wiki/benchmarks/ACRONYM.md`를 신설했다. `Ontology`의 태그 어휘에 `grasping`, `flow-matching`, `generative-models`를 추가했다. index를 갱신했다.
- Notes: PDF 전문(12쪽)을 pypdf로 추출해 표 수치를 원문에서 확인했다. Read 도구는 owner-password 때문에 열지 못했으나 열람 제한은 없었다. PDF annotation 없음. Grasp 생성 축이 이 ingest로 신설되었고, 기존 위키와의 연결점은 세 갈래다: pi0 계열의 flow matching action head (few-step화 이식 가능성), Amortized NeuralSDF의 amortization 패턴, 보조 SDF regression을 통한 Neural Implicit Surface Representation 축. 검증 필요 항목: concurrent work(Zhong et al. ICML 2026) 열위 주장은 저자 측 재현 기반, 코드 공개 여부 미언급, ACRONYM 전체 규모는 원 논문 미확보로 부분집합 수치만 기록. 원자료 파일명이 arXiv ID 그대로라 명명 규칙에 맞는 rename은 사용자 승인 대기.

## [2026-08-01] ingest | SDFReg point cloud registration

- Input: `raw/papers/2023 - SDFReg Learning Signed Distance Functions for Point Cloud Registration.pdf` (arXiv 2304.08929v2, 사용자가 링크 지정해 신규 수집)
- Changed: source note와 paper page를 추가했다. `wiki/methods/SDFReg Point Cloud Registration.md`, `wiki/concepts/Point Cloud Registration.md`, `wiki/concepts/Neural Implicit Surface Representation.md`를 신설했다. 비어 있던 `wiki/benchmarks/`에 첫 페이지로 [[ModelNet40]]과 [[3DMatch]]를 만들었다. 질문 [[2026-08-01 - Can One SDF Representation Serve Perception and Contact]]를 승격했다. 기존 [[Signed Distance Field Collision Detection]]과 [[NeuralSDF Collision Detection]]에 신규 개념 링크와 열린 질문을 연결하고, `signed-distance-function` 태그를 `signed-distance-field`로 정규화했다. `Ontology`의 태그 어휘에 `point-cloud-registration`, `neural-implicit-representation`, `perception`, `benchmark`를 추가했다. index를 갱신했다.
- Notes: PDF 본문과 supplementary를 직접 추출해 표 수치를 원문에서 확인했다. PDF annotation 없음. 이 논문은 위키에 있던 SDF 자료들과 응용 축이 다르다. 기존 세 편은 모두 접촉/충돌 계산이고 이 논문은 지각/정렬이라, 공통 표현을 묶는 개념 페이지를 새로 만들고 두 축을 연결하는 질문을 승격했다. 논문 자체의 공백도 기록했다. 계산 비용이 전혀 보고되지 않았고, limitation 절이 없으며, clean data에서는 IFR/DCP 대비 이점이 없다. 검증 필요: Table 3의 baseline 인용 번호가 참고문헌 목록과 어긋나 있고(`FMR [12]`, `DeepGMR [11]`), 본문과 supplementary가 SDF 학습을 각각 self-supervised와 semi-supervised로 다르게 부른다. venue 미표기라 게재 여부는 미확인이다.

## [2026-08-01] schema | AGENTS.md 및 운영 스키마 업그레이드

- Input: 사용자가 `AGENTS.md` 가이드 개선 가능성과 최신 LLM wiki 운영 방식 조사를 요청. 조사 대상은 Karpathy LLM Wiki 원본 gist, LLM Wiki v2 확장 논의, AGENTS.md 스펙 관련 2026년 가이드, Claude Code의 AGENTS.md/CLAUDE.md 동작.
- Changed: `AGENTS.md`를 계약 중심으로 재작성했다. Non-Negotiables, Frontmatter Contract, Evidence Tiers(A/B/C), Lifecycle and Supersession, Scaling Rules, Tool Notes를 신설하고 상세 절차는 `wiki/_meta/`로 위임했다. 에이전트 명칭을 Codex 고정에서 도구 중립으로 바꿨다. `CLAUDE.md`를 추가해 `@AGENTS.md`를 import하도록 했다. `wiki/_meta/Workflow.md`를 ingest triage/read/write/link/record 5단계로 재구성하고 query에 evidence tier·freshness 규칙을 추가했다. `wiki/_meta/Maintenance.md`와 실행 가능한 `wiki/_meta/lint.py`를 신설했다. `wiki/_meta/Ontology.md`에 Relations, Evidence Tiers, Tag Vocabulary를 추가했다. `wiki/_meta/Templates.md`에 frontmatter 표와 Source/Method/Benchmark/Log/Superseded 템플릿을 추가했다. `raw/README.md`, `Home.md`, `wiki/index.md`를 갱신하고 `raw/lectures/`를 만들었다. lint 결과 발견된 항목을 수정했다. synthesis 페이지의 BOM 제거, `log.md` frontmatter 추가, `Embodied AI` status `seed` -> `stub`, small-motion source note status `processed` -> `ingested`, Raviola 페이지에 `superseded_by` 추가.
- Notes: 조사에서 확인한 핵심은 세 가지다. (1) Claude Code는 `AGENTS.md`를 직접 읽지 않으므로 `CLAUDE.md`의 `@AGENTS.md` import가 필요하다. 이 vault에는 `CLAUDE.md`가 없어 기존 규칙이 Claude Code 세션에 로드되지 않고 있었다. (2) 스키마 파일은 길이보다 밀도가 중요하며, 상세 절차 중복은 드리프트를 만든다. `AGENTS.md`와 `Workflow.md`에 중복되어 있던 ingest/chat 절차를 한 곳으로 정리했다. (3) LLM Wiki v2 논의에서 유효한 것은 supersession과 evidence chain이고, 수치 confidence score는 비판이 많아 채택하지 않았다. 대신 Tier A/B/C와 `superseded_by`를 도입했다. 검증 필요: `raw/lecutre_note/`는 오타로 보이는 빈 디렉터리이고 `raw/lectures/`로 대체 예정이나 사용자 확인 전까지 삭제하지 않았다.

## [2026-06-22] query | pi0.6 and pi0.7 comparison

- Input: User asked for the difference between $\pi^*_{0.6}$ and $\pi_{0.7}$, then requested the answer be ingested.
- Changed: Added `wiki/questions/2026-06-22 - What Is the Difference Between pi0.6 and pi0.7.md` and linked it from `wiki/index.md`.
- Notes: The answer frames $\pi^*_{0.6}$ as VLA + RL/task-specific deployment improvement, and $\pi_{0.7}$ as steerable generalist VLA/RFM with rich context conditioning.

## [2026-06-22] query | VLA and reinforcement learning relationship

- Input: User asked about the conceptual relationship and different level of abstraction between VLA and Reinforcement Learning.
- Changed: Added `wiki/questions/2026-06-22 - What Is the Relationship Between VLA and Reinforcement Learning.md` and linked it from `wiki/index.md`.
- Notes: The answer frames VLA as a policy/model class and RL as a training or policy-improvement framework, using the Physical Intelligence $\pi^*_{0.6}$, $\pi_{0.7}$, and RECAP pages as local wiki context.

## [2026-06-22] ingest | AI-based robot fault diagnosis chat

- Input: `raw/chats/AI 기반 로봇 고장진단.pdf`
- Changed: Added chat source note with Important Questions. Promoted three question pages about AI diagnosis under small motions, CVAE vs NPE, and diagnostic trajectory distribution matching. Added theory/method pages for physics-informed NPE, slow-fast parameter separation, and safe diagnostic trajectory design. Updated `wiki/index.md`.
- Notes: The chat is a secondary source and includes unverified external literature suggestions. Claims about FIGAROH, safe online system identification, RMA, HiP-RSSM, and hybrid inverse dynamics should be checked against primary sources before being treated as settled knowledge.

## [2026-06-22] query | TE-SDF distance computation

- Input: User asked how TE-SDF computes distance based on the wiki and requested the answer be saved as a new `.md` file.
- Changed: Added `wiki/questions/2026-06-22 - How Does TE-SDF Compute Distance.md` and linked it from `wiki/index.md`.
- Notes: The answer summarizes TE-SDF's tetrahedron-local encoded face set distance query, gap function, preprocessing acceleration, and truncation caveats using the TE-SDF paper note and learning material source.

## [2026-06-21] ingest | Physical Intelligence VLA papers and TE-SDF learning notes

- Input: `raw/papers/2511.14759v2.pdf`, `raw/papers/2604.15483v2.pdf`, `raw/notes/논문 학습 자료 요청.pdf`, `raw/chats/내용 파악 요약.pdf`
- Changed: Renamed the two new raw paper PDFs to `raw/papers/2025 - pi0.6 a VLA That Learns From Experience.pdf` and `raw/papers/2026 - pi0.7 Steerable Generalist Robotic Foundation Model.pdf`. Added source notes and paper pages for Physical Intelligence $\pi^*_{0.6}$ / RECAP and $\pi_{0.7}$. Added pages for [[RECAP RL with Experience and Corrections]], [[Context-Conditioned Robot Foundation Models]], [[Physical Intelligence]], the TE-SDF learning material, the Amortized NeuralSDF KKT chat source, and the promoted KKT question. Updated the index and connected TE-SDF/Amortized NeuralSDF method pages to the secondary notes.
- Notes: The two paper PDFs expose arXiv identifiers `2511.14759v2` and `2604.15483v2`. PDF annotation checks found link annotations but no user highlight/text/ink markers. The TE-SDF learning material and KKT chat are secondary/LLM-generated sources; primary claims should be checked against the corresponding paper PDFs.

## [2026-06-16] ingest | TE-SDF collision detection

- Input: `raw/papers/0c0760_c634df9134e4476c93b0a40a5a49c203.pdf`
- Changed: Renamed the raw PDF to `raw/papers/2026 - TE-SDF Tetra-Encoded Signed Distance Field.pdf`. Added source note and paper page for "TE-SDF: Tetra-Encoded Signed Distance Field for Memory-Efficient and Accurate Collision Detection". Added concept pages for signed distance field collision detection and Tetra-Encoded Signed Distance Field, plus a method page for TE-SDF collision detection. Updated the wiki index and linked TE-SDF from the NeuralSDF collision page.
- Notes: PDF metadata date is 2026-05-07. The PDF lists TES SDK and encoder GitHub URLs. Venue/arXiv/DOI were not visible in the PDF and remain marked for verification. Annotation marker search found annotations but no user highlight/text/ink markers.

## [2026-06-16] maintenance | Raw paper filename alignment

- Input: User requested `raw/papers/` filenames match `wiki/papers/` paper note names.
- Changed: Renamed five PDF files under `raw/papers/` to the corresponding `wiki/papers/` basenames and updated wiki source references outside the append-only historical log.
- Notes: Historical `wiki/log.md` entries still preserve the original input filenames. Current source links now point to the renamed raw PDF files.

## [2026-06-15] schema | Chat important questions

- Input: User requested important questions from `raw/chats/` conversations be recorded carefully.
- Changed: Updated `AGENTS.md`, `wiki/_meta/Workflow.md`, `wiki/_meta/Chat Source Workflow.md`, and `wiki/_meta/Templates.md` to require an `Important Questions` section for chat source notes, with question status labels and promotion rules.
- Notes: Chat questions are now preserved separately from answer summaries, even when the answer is incomplete or requires primary-source verification.

## [2026-06-15] ingest | Amortized NeuralSDF-mesh collision detection

- Input: `raw/papers/0c0760_a300ee12f6054b399ed0e4b4af409ca6.pdf`
- Changed: Added source note and paper page for "Amortized NeuralSDF-Mesh Collision Detection for Robotic Contact Simulation". Added concept page for NeuralSDF collision detection and method page for amortized NeuralSDF-mesh collision detection. Updated `wiki/index.md`.
- Notes: PDF metadata date is 2026-03-06. Venue/arXiv/DOI were not visible in the PDF and remain marked for verification. Annotation marker search found no user highlight/text/ink notes.

## [2026-06-15] ingest | DIAL VLA and robotic cloth manipulation review

- Input: `raw/papers/260329844v1 1_260615_004135.pdf`, `raw/papers/frobt-13-1752914.pdf`
- Changed: Added source notes and paper pages for DIAL and the Frontiers robotic cloth manipulation systematic review. Added concept/method pages for latent world modeling, robotic cloth manipulation, and cloth manipulation learning paradigms. Promoted reusable research questions to `wiki/questions/`. Updated VLA and Physical AI concept pages, index, workflow, ontology, templates, and AGENTS.md.
- Notes: PDF annotation extraction found only link annotations and no user highlight/text/ink notes. Important questions were selected from explicit paper research questions and future-work/discussion sections. The ingest policy now requires notes/marginalia checks and question promotion during paper ingest.

## [2026-06-15] schema | Chat source workflow

- Input: User requested an operating plan for storing LLM conversation records under `raw/chats/`.
- Changed: Added chat-specific ingest, lint, trust, naming, source note, promotion, privacy, and security rules to `AGENTS.md`, `wiki/_meta/Workflow.md`, `wiki/_meta/Ontology.md`, and `wiki/_meta/Templates.md`. Added `wiki/_meta/Chat Source Workflow.md`, updated `wiki/index.md`, and clarified `raw/README.md`.
- Notes: Chat logs are treated as untrusted secondary source records. Claims from LLM answers require primary-source verification before being promoted as settled wiki knowledge.

## [2026-06-15] maintenance | Inline math format

- Input: User requested inline formulas in sentences use Obsidian `$...$` math instead of inline code/backtick style.
- Changed: Converted inline mathematical variables and expressions in wiki pages from backticks to `$...$`, including $\pi_E$, $\phi_f^{eff}$, $\beta_R^0$, $g^{real}(T)$, $q$, $\dot q$, $\tau$, $Y^T Y$, and related SBI notation. Updated `AGENTS.md` to distinguish inline math from code/path backticks.
- Notes: Backticks remain for file paths, metadata fields, product/model names, action labels, and log literals where they are not mathematical notation.

## [2026-06-15] maintenance | Obsidian math block format

- Input: User requested applying the new AGENTS.md math rule across the wiki.
- Changed: Converted wiki math code fences from fenced `math` blocks to Obsidian-renderable `$$ ... $$` block math.
- Notes: Raw source files were not modified because `raw/` is the immutable source layer.

## [2026-06-15] ingest | Bin picking, robot dynamics identification, and LG CNS PhysicalWorks

- Input: `raw/papers/2302.08152v2.pdf`, `raw/papers/robotics-10-00083-v3.pdf`, `raw/notes/deep-research-report.md`
- Changed: Added source notes and paper pages for Zhang et al. 2023 tangled-prone bin picking and Raviola et al. 2021 dynamic parameter identification. Added method/concept pages for tangled-prone bin picking, object singulation, action affordance learning, robot foundation models, and robot fleet orchestration. Added entity and synthesis pages for LG CNS PhysicalWorks. Updated index and related concepts. Marked the previous unverified Raviola reference as superseded.
- Notes: PhysicalWorks raw report contains chat-internal citation markers rather than durable URLs, so its claims are preserved as a secondary report with explicit verification caveats.

## [2026-06-15] ingest | Small-motion end-effector inertia and friction fault diagnosis note

- Input: `raw/notes/충분 가진이 어려운 산업용 로봇의 End-effector 관성 및 마찰 파라미터 추정 기반 고장진단 방법론.md`
- Changed: Added source note, synthesis page, method page, concept pages for SBI/NPE/differentiable dynamics/temperature-friction baseline/robot dynamics identification, and paper pages for Cranmer et al. 2020, Greenberg et al. 2019, Muratore et al. 2022, Lutter et al. 2021. Added an unverified Raviola reference page.
- Notes: The raw note appears mojibake in the command-line environment, so extraction relied on readable equations, English terms, section structure, and URLs. Raviola et al. could not be uniquely verified and remains marked `status: unverified`.

## [2026-06-14] schema | Initial robotics wiki scaffold

- Input: User requested a personal knowledge/know-how wiki for robotics and Physical AI, inspired by Karpathy's LLM Wiki idea.
- Changed: Created raw source directories, wiki directories, index, metadata workflows, templates, ontology, and initial concept stubs.
- Notes: The vault is configured as an Obsidian-friendly LLM-maintained wiki. Raw sources are immutable; `wiki/` is the maintained knowledge layer.

## [2026-11-02] ingest | GraspGraphNet multi-embodiment dexterous grasp generation

- Input: `raw/papers/2026 - GraspGraphNet Graph-Structured Multi-Embodiment Dexterous Grasp Generation.pdf` (사용자 제공 `2607.11031v1.pdf`).
- Changed: GraspGraphNet source note·논문 페이지·방법 페이지와 Cross-Embodiment Dexterous Grasping 개념 페이지를 추가했다. Flow Matching, Generative Grasp Synthesis, MeanFlow, GraspMF 방법 페이지와 `wiki/index.md`를 갱신했다.
- Notes: 원본 PDF를 변경 없이 보존했다. 논문 표와 평가 조건을 대조하고, 시뮬레이션·손가락 제거 zero-shot·Leap Hand 미세조정 후 실물 결과를 구분했다. PDF 주석·하이라이트 확인 결과는 source note에 기록했다. Flow Matching의 추론 스텝 수에 관한 기존 설명은 GraspGraphNet의 3스텝 결과를 반영해 적용 범위와 변경 근거를 명시했다.

## [2026-11-02] lint | GraspGraphNet ingest validation

- Input: GraspGraphNet 관련 신규·갱신 문서와 원본 PDF.
- Changed: Ingest 운영 로그를 보완했다.
- Notes: `python3 wiki/_meta/lint.py` 기계 점검을 통과했다. 새 문서의 주요 수치·평가 범위·출처 연결을 원문과 대조했다.

## [2026-11-03] ingest | Quadruped open stair learning papers and RBQ10

- Input: 현재 대화의 위키 정리 요청, RBQ10 `reports/literature-stairs-20261026-01/implementation.json`의 핵심 6편, `training/lf2wb/README.md`의 관련 2편, 버전을 고정한 arXiv 본문·서지 및 저자 프로젝트.
- Changed: 논문 8편과 source note 8개, partial chat source 1개, 개념 2개, 보상 설계·평가 방법 1개, 질문 2개, 종합 1개를 추가했다. `wiki/index.md`, Embodied AI, Physical AI를 연결했다. 시작 문서는 [[2026-11-03 - Quadruped Open Stair Learning and RBQ10]]이다.
- Notes: 논문 원문은 Tier A, 대화의 진단 가설은 Tier C로 구분했다. Humanoid 문헌 2편과 4족 문헌, 엣지 여유와 스윙 높이, 특권 학습 정보와 배포 actor 입력을 구분했다. 2026-10-27의 RBQ10 관측과 신규 보상 검증은 논문 결과와 분리했다. 원대화 export 미확보와 사용자 PDF annotation 미확인을 source note에 기록했다. 기존 raw 자료와 `.obsidian/`을 수정하지 않았으며 commit은 수행하지 않았다.

## [2026-11-03] lint | Quadruped open stair literature validation

- Input: 신규 문서 23개와 연결을 추가한 기존 문서 4개.
- Changed: 문헌 정리 후 검증 결과를 운영 로그에 추가했다.
- Notes: `python3 wiki/_meta/lint.py`와 `git diff --check`를 통과했다. 신규 문서의 출처·내부 링크·길이 및 목차의 섹션당 30항목 제한을 확인했다. 기존 raw 파일 22개의 SHA-256이 동일하며 기존 문서 본문에서 삭제·변경된 줄이 없음을 확인했다. 서지·보상 설명은 원문과, RBQ10 수치는 해당 실험 기록과 대조했다. 사용자 PDF 주석과 학습 후 성능은 이번 검증 범위에 포함하지 않았다.

## [2026-11-03] ingest | AlphaNIST binary-reward assembly

- Input: 사용자가 지정한 `https://alpha-nist.github.io/` 및 arXiv:2610.13354v1 (2026-10-09), `raw/papers/2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards.pdf`.
- Changed: 원본 PDF를 보존하고 [[2026-10-09 - AlphaNIST Source]], [[2026 - AlphaNIST Emergent Assembly Skills from Binary Task Rewards]], [[AlphaNIST Binary-Reward Assembly]], [[Reset-State Curricula for Sparse-Reward RL]], [[NIST Assembly Task Board 1]], [[2026-11-03 - When Can Binary Rewards Replace Dense Shaping]]를 추가했다. Physical AI, Object Singulation, RECAP, Open Stair Reward Design and Evaluation에 관련 내용을 연결하고 index를 갱신했다.
- Notes: 공식 v1 PDF 8쪽을 읽고 주요 수식·결과를 검토했다. 압축 PDF 객체를 포함한 annotation 확인에서 Link 81개, 필기·하이라이트 subtype 없음으로 확인했다. 98.2% 학습 성공, frozen mixed-reset 평가, 별도 10-pair 정책의 84%를 구분했다. 완료 task reward 외 제어 비용, simulation-only 범위, 실물·전체 20-pair 조립의 미검증 상태를 명시했다. 보행으로의 적용은 추론과 실험 질문으로 표시했다. PDF는 바이너리 파일로 Git에 포함하며 원본 checksum을 source note에 남겼다.

## [2026-11-03] lint | AlphaNIST ingest validation

- Input: AlphaNIST 관련 신규·갱신 문서 및 원본 PDF.
- Changed: Frontmatter·날짜·출처·상호 링크·index 등재와 평가 조건을 점검했다.
- Notes: `python3 wiki/_meta/lint.py`와 `git diff --check`를 통과했다. 별도 내용 검토에서 주요 수치와 평가 범위의 중요한 오류를 발견하지 못했다. Source note의 파일 크기·SHA-256을 저장된 PDF와 대조했다. Obsidian 설정은 이번 작업 범위에 포함하지 않는다.
