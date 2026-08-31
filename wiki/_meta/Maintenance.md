---
type: meta
status: active
created: 2026-08-01
updated: 2026-08-01
tags:
  - workflow
  - lint
  - llm-wiki
sources: []
---

# Maintenance

위키 점검(lint) 체크리스트다. 트리거: "위키 점검", "lint", "정리 상태 봐줘".

점검은 두 단계다. **기계 점검**은 스크립트가 하고, **내용 점검**은 에이전트가 판단한다.

## 1. 기계 점검

vault 루트에서 실행한다.

```bash
python "wiki/_meta/lint.py"
```

검사 항목:

- frontmatter 존재 여부와 필수 필드(`type`, `status`, `created`, `updated`, `tags`, `sources`)
- `type`, `status` 어휘 위반
- `created` / `updated` 날짜 형식과 순서
- `status: superseded`인데 `superseded_by`가 없는 페이지
- 깨진 Obsidian 위키 링크
- 고아 페이지 (inbound 링크 없음)
- `wiki/index.md`에 등재되지 않은 페이지
- `sources:`에 적혔지만 실제로 없는 `raw/` 경로
- source note가 없는 `raw/` 원자료

스크립트가 잡는 것은 형식뿐이다. 통과했다고 내용이 정확한 것은 아니다.

## 2. 내용 점검

에이전트가 직접 읽고 판단한다.

### 지식 품질

- [ ] 출처 없는 강한 주장이 있는가. 있으면 근거를 붙이거나 `검증 필요:`로 낮춘다.
- [ ] Tier C(LLM 답변, 필기 추론)만 근거인 문장이 확정 서술로 쓰이지 않았는가.
- [ ] 에이전트 추론이 원자료 주장처럼 쓰이지 않았는가. `추론:` 표시를 확인한다.
- [ ] 수치, 벤치마크, 날짜가 원자료와 일치하는가.

### 구조

- [ ] 같은 개념이 다른 이름으로 중복 생성되지 않았는가. 있으면 하나로 합치고 나머지는 `superseded` 처리한다.
- [ ] 자주 등장하지만 아직 페이지가 없는 개념이 있는가.
- [ ] 페이지가 400줄을 넘어 분할이 필요한가.
- [ ] `wiki/index.md`의 한 섹션이 30개를 넘어 MOC가 필요한가.
- [ ] `status: stub`인 채로 오래 방치된 페이지가 있는가.

### 시간

- [ ] 업체·제품·시장 정보 중 `updated`가 6개월 이상 지난 페이지가 있는가.
- [ ] 후속 논문에 의해 약화된 주장이 `Contradictions / Updates` 없이 남아 있는가.
- [ ] `status: draft`로 오래 머문 페이지가 있는가.

### 원자료 커버리지

- [ ] `raw/`에 있는데 source note가 없는 자료가 있는가.
- [ ] source note는 있는데 개념·방법·논문 페이지로 이어지지 않은 자료가 있는가.
- [ ] 필기·하이라이트가 있는데 질문으로 승격되지 않은 중요한 쟁점이 있는가.

### Chat source 전용

- [ ] `raw/chats/`에는 있는데 source note가 없는 대화 기록.
- [ ] chat 답변만 근거로 확정된 강한 주장.
- [ ] `turn...`, `search result` 같은 재현 불가능한 내부 citation.
- [ ] 개인정보, credential, 비공개 정보가 wiki 본문에 복사된 흔적.
- [ ] 같은 질문을 여러 LLM에 물은 중복 대화. 더 나은 synthesis로 합칠 수 있는지 본다.

## 3. 조치

- 작은 수정(링크, frontmatter, 날짜, index 등재)은 바로 한다.
- 큰 재구성(페이지 병합·분할, 디렉터리 이동, 대규모 이름 변경)은 먼저 제안하고 승인 후 진행한다.
- 삭제는 하지 않는다. `status: superseded` + `superseded_by`로 처리하고, 실제 삭제는 사용자 승인 후에만 한다.
- 결과를 `wiki/log.md`에 `lint`로 기록한다. 무엇을 고쳤고 무엇을 남겨뒀는지 모두 적는다.

## 4. 권장 주기

- 매 ingest 후: 기계 점검.
- 자료 5-10개마다: 내용 점검 전체.
- 분기별: 오래된 업체·제품 정보 재확인, 중복 개념 통합, index 구조 재검토.
