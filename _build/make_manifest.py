#!/usr/bin/env python3
"""从章节目录里的 Markdown 生成 manifest.json。

约定（章节文件必须遵守）：
  - 一级标题 "# 第 N 章：xxx" 作为章节标题；
  - "## 自测题（答案与解析）" 下每条以 "### Q1 【单选】" 开头，
    选项行 "- A. ..."；答案行 "**答案**：B"；解析行 "**解析**：..."；
  - flashcards.md 每条 "### 卡片：问题"，下面 "- **背面**：..."、"- **标签**：a, b"、"- **章节**：ch01"；
  - glossary.md 是四列表格：术语 | 白话定义 | 首次出现 | 章节；
  - concepts/*.md 第一行注释 "<!--chapters: ch03,ch07-->"
用法：python3 make_manifest.py <书目录> <config.json>
"""
import json, os, re, sys

TYPE_MAP = {"单选": "single", "多选": "multi", "填空": "blank", "判断": "single"}
LETTER = {"A": 0, "B": 1, "C": 2, "D": 3}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def parse_quizzes(md):
    m = re.search(r"^##\s*自测题.*$", md, re.M)
    if not m:
        return []
    body = md[m.end():]
    # 到下一个二级标题为止
    nxt = re.search(r"^##\s", body, re.M)
    if nxt:
        body = body[:nxt.start()]
    blocks = re.split(r"^###\s*Q", body, flags=re.M)[1:]
    out = []
    for b in blocks:
        head = b.split("\n", 1)[0]
        tm = re.search(r"【(单选|多选|填空|判断)】", head)
        qtype = TYPE_MAP[tm.group(1)] if tm else "single"
        stem = re.sub(r"^\d+\s*", "", head)
        stem = re.sub(r"【(单选|多选|填空|判断)】", "", stem).strip()
        rest = b.split("\n", 1)[1] if "\n" in b else ""
        opts = re.findall(r"^\s*-\s*([A-D])\.\s*(.*)$", rest, re.M)
        ans = re.search(r"\*\*答案\*\*[：:]\s*(.+)$", rest, re.M)
        exp = re.search(r"\*\*解析\*\*[：:]\s*(.+)$", rest, re.M)
        if not ans:
            continue
        av = ans.group(1).strip()
        if qtype == "multi":
            answer = [LETTER[c] for c in re.findall(r"[A-D]", av)]
        elif qtype == "blank":
            answer = av
        else:
            answer = LETTER.get(av[0], 0) if av[:1] in LETTER else 0
        out.append({
            "id": "", "chapterId": "",
            "type": qtype,
            "question": stem,
            "options": [o[1].strip() for o in opts],
            "answer": answer,
            "explain": exp.group(1).strip() if exp else "",
        })
    return out


def parse_cards(md):
    out = []
    for blk in re.split(r"^###\s*卡片[：:]\s*", md, flags=re.M)[1:]:
        front = blk.split("\n", 1)[0].strip()
        rest = blk.split("\n", 1)[1] if "\n" in blk else ""
        back = re.search(r"\*\*背面\*\*[：:]\s*(.+)", rest)
        tags = re.search(r"\*\*标签\*\*[：:]\s*(.+)", rest)
        ch = re.search(r"\*\*章节\*\*[：:]\s*(.+)", rest)
        if not back:
            continue
        out.append({
            "id": "", "chapterId": ch.group(1).strip() if ch else "",
            "front": front, "back": back.group(1).strip(),
            "tags": [t.strip() for t in tags.group(1).split(",") if t.strip()] if tags else [],
        })
    return out


def parse_glossary(md):
    out = []
    for line in md.split("\n"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("术语", "") or set(cells[0]) <= set("-: "):
            continue
        ch = re.search(r"ch\d{2}", cells[3]) if len(cells) > 3 else None
        out.append({"term": cells[0], "def": cells[1],
                    "chapterId": ch.group(0) if ch else ""})
    return out


def main():
    root, cfgp = sys.argv[1], sys.argv[2]
    cfg = json.loads(read(cfgp))
    man = {k: cfg[k] for k in ("slug", "title", "subtitle", "book", "audience", "goal")}

    chapters, quizzes, cards = [], [], []
    for i, ch in enumerate(cfg["chapters"], 1):
        fp = os.path.join(root, ch["file"])
        md = read(fp)
        title = re.match(r"#\s*(.+)", md).group(1).strip()
        chapters.append({"id": ch["id"], "title": title, "file": ch["file"],
                         "difficulty": ch.get("difficulty", 1)})
        for q in parse_quizzes(md):
            q["chapterId"] = ch["id"]
            # 不能以 chNN- 开头：build_handbook 会给 data-qid 无条件加章节前缀，
            # 而 manifest 里的 id 只在「未带该前缀」时才加，两者会分叉成 ch01-ch01-q1。
            n_ch = len([x for x in quizzes if x["chapterId"] == ch["id"]]) + 1
            q["id"] = f"q{i:02d}{n_ch:02d}"
            quizzes.append(q)

    cp = os.path.join(root, "flashcards.md")
    if os.path.exists(cp):
        for c in parse_cards(read(cp)):
            c["id"] = f"f{len(cards) + 1:02d}"
            cards.append(c)

    man["learningPath"] = cfg["learningPath"]
    man["chapters"] = chapters
    man["concepts"] = []
    cdir = os.path.join(root, "concepts")
    if os.path.isdir(cdir):
        for i, fn in enumerate(sorted(os.listdir(cdir)), 1):
            if not fn.endswith(".md"):
                continue
            md = read(os.path.join(cdir, fn))
            m = re.search(r"<!--chapters:\s*([\w,\s]+)-->", md)
            title = re.match(r"#\s*(.+)", md).group(1).strip()
            man["concepts"].append({"id": f"c{i:02d}", "title": title,
                                    "file": f"concepts/{fn}",
                                    "chapterIds": [x.strip() for x in m.group(1).split(",")] if m else []})
    for k in ("patterns", "cheatsheet"):
        man[k] = {"file": f"{k}.md"}
    man["glossary"] = parse_glossary(read(os.path.join(root, "glossary.md")) if os.path.exists(os.path.join(root, "glossary.md")) else "")
    man["quizzes"] = quizzes
    man["flashcards"] = cards
    man["companion"] = f"{cfg['slug']}学习伴侣.html"

    out = os.path.join(root, "manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
    print(f"{cfg['slug']}: 章 {len(chapters)} · 题 {len(quizzes)} · 卡 {len(cards)} · 术语 {len(man['glossary'])} · 概念 {len(man['concepts'])}")


if __name__ == "__main__":
    main()
