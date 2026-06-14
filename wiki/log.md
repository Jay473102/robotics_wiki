# Wiki Log

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
