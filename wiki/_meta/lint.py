#!/usr/bin/env python3
"""Robotics wiki lint.

vault 루트에서 실행한다:  python "wiki/_meta/lint.py"

기계적으로 확인 가능한 항목만 검사한다. 내용 판단(중복 개념, 오래된 주장,
출처 없는 강한 주장)은 에이전트가 wiki/_meta/Maintenance.md 체크리스트로 수행한다.
"""

import os
import re
import sys
from collections import Counter, defaultdict

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKIP_DIRS = {".git", ".obsidian", ".claude", "__pycache__"}

REQUIRED_FIELDS = ["type", "status", "created", "updated", "tags", "sources"]
VALID_TYPES = {
    "source", "paper", "concept", "method", "entity", "benchmark",
    "synthesis", "question", "meta", "index", "home", "log",
}
VALID_STATUS = {
    "stub", "draft", "active", "verified", "superseded",
    "ingested", "partial", "unverified",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"\[\[([^\]|#]+)")
FENCE_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
# 템플릿 자리표시자는 실제 페이지가 아니다.
PLACEHOLDERS = {"New Page", "Wiki Link", "Concept", "Method", "Topic", "Question"}


def walk_md(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def rel(path):
    return os.path.relpath(path, VAULT).replace("\\", "/")


def parse_frontmatter(text):
    text = text.lstrip("﻿")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    fields = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif line.lstrip().startswith("-") and key:
            fields[key] = (fields.get(key) or "") + " " + line.strip()
    return fields


def main():
    problems = defaultdict(list)

    wiki_files = []
    all_files = []
    names = set()
    for path in walk_md(VAULT):
        all_files.append(path)
        names.add(os.path.basename(path)[:-3])
        if os.path.relpath(path, VAULT).replace("\\", "/").startswith("wiki/"):
            wiki_files.append(path)

    inbound = Counter()
    broken = defaultdict(list)

    for path in all_files:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        in_wiki = path in wiki_files

        # 코드 펜스 안의 링크는 템플릿 예시다.
        for target in LINK_RE.findall(FENCE_RE.sub("", text)):
            target = target.strip()
            if not target or target in PLACEHOLDERS:
                continue
            if target in names:
                inbound[target] += 1
            elif in_wiki and not target.lower().endswith((".pdf", ".png", ".jpg")):
                broken[target].append(rel(path))

        if not in_wiki:
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            problems["frontmatter 없음"].append(rel(path))
            continue
        for field in REQUIRED_FIELDS:
            if field not in fm:
                problems["필수 필드 누락"].append(f"{rel(path)}  ({field})")
        if fm.get("type") and fm["type"] not in VALID_TYPES:
            problems["알 수 없는 type"].append(f"{rel(path)}  ({fm['type']})")
        if fm.get("status") and fm["status"] not in VALID_STATUS:
            problems["알 수 없는 status"].append(f"{rel(path)}  ({fm['status']})")
        for field in ("created", "updated"):
            value = fm.get(field, "")
            if value and not DATE_RE.match(value):
                problems["날짜 형식 오류"].append(f"{rel(path)}  ({field}: {value})")
        if fm.get("created") and fm.get("updated"):
            if DATE_RE.match(fm["created"]) and DATE_RE.match(fm["updated"]):
                if fm["updated"] < fm["created"]:
                    problems["updated < created"].append(rel(path))
        if fm.get("status") == "superseded" and "superseded_by" not in fm:
            problems["superseded인데 superseded_by 없음"].append(rel(path))

        # raw 경로는 공백을 포함할 수 있다. frontmatter 리스트 항목과 backtick 안만 검사한다.
        # log.md는 append-only 이력이라 이름이 바뀐 옛 경로를 그대로 보존한다. 검사 대상에서 뺀다.
        raw_refs = set()
        if os.path.basename(path) != "log.md":
            raw_refs |= set(re.findall(r"^\s*-\s+(raw/.+?)\s*$", text, re.MULTILINE))
            raw_refs |= set(re.findall(r"`(raw/[^`]+)`", text))
        for raw_ref in raw_refs:
            if "YYYY" in raw_ref or "path/to" in raw_ref:
                continue
            if not os.path.exists(os.path.join(VAULT, raw_ref)):
                problems["존재하지 않는 raw 경로 참조"].append(f"{rel(path)}  -> {raw_ref}")

    for target, refs in sorted(broken.items()):
        problems["깨진 링크"].append(f"[[{target}]]  <- {', '.join(sorted(set(refs))[:3])}")

    for path in sorted(wiki_files):
        base = os.path.basename(path)[:-3]
        if base in ("index", "log"):
            continue
        if inbound[base] == 0:
            problems["고아 페이지 (inbound 링크 없음)"].append(rel(path))

    index_path = os.path.join(VAULT, "wiki", "index.md")
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8", errors="replace") as fh:
            index_text = fh.read()
        indexed = {t.strip() for t in LINK_RE.findall(index_text)}
        for path in sorted(wiki_files):
            base = os.path.basename(path)[:-3]
            if base in ("index", "log") or "/_meta/" in rel(path):
                continue
            if base not in indexed:
                problems["index.md에 없는 페이지"].append(rel(path))

    source_frontmatter = " ".join(
        open(p, encoding="utf-8", errors="replace").read()
        for p in wiki_files
        if "/sources/" in rel(p)
    )
    raw_root = os.path.join(VAULT, "raw")
    for dirpath, dirnames, filenames in os.walk(raw_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name in (".gitkeep", "README.md"):
                continue
            if name not in source_frontmatter:
                problems["source note가 없는 원자료"].append(
                    rel(os.path.join(dirpath, name))
                )

    if not problems:
        print("clean: 기계 점검 항목에서 문제를 찾지 못했다.")
        return 0

    total = 0
    for label in sorted(problems):
        items = problems[label]
        total += len(items)
        print(f"\n## {label} ({len(items)})")
        for item in items:
            print(f"  - {item}")
    print(f"\n총 {total}건. 내용 판단 항목은 Maintenance.md 체크리스트로 이어서 확인한다.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
