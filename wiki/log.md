# Wiki Log

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
