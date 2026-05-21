from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "tutorial-flutter-dasar-pemula.md"
WEB_DIR = ROOT / "web"


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "section"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def close_list(parts: list[str], state: dict[str, str | None]) -> None:
    if state["list"] == "ul":
        parts.append("</ul>")
    elif state["list"] == "ol":
        parts.append("</ol>")
    elif state["list"] == "check":
        parts.append("</div>")
    state["list"] = None


def flush_paragraph(parts: list[str], buffer: list[str]) -> None:
    if not buffer:
        return
    text = " ".join(line.strip() for line in buffer).strip()
    if text:
        parts.append(f"<p>{inline_markdown(text)}</p>")
    buffer.clear()


def convert_markdown(markdown: str) -> tuple[str, list[dict[str, str]]]:
    parts: list[str] = []
    toc: list[dict[str, str]] = []
    paragraph_buffer: list[str] = []
    code_buffer: list[str] = []
    state: dict[str, str | None] = {"list": None}
    in_code = False
    code_lang = ""
    first_h1 = True

    used_ids: set[str] = set()

    for raw in markdown.splitlines():
        line = raw.rstrip()

        fence = re.match(r"^```(\w+)?", line)
        if fence:
            if in_code:
                code_text = html.escape("\n".join(code_buffer).rstrip())
                label = html.escape(code_lang or "code")
                parts.append(
                    f'<div class="code-card"><div class="code-label">{label}</div><pre><code>{code_text}</code></pre></div>'
                )
                code_buffer.clear()
                code_lang = ""
                in_code = False
            else:
                flush_paragraph(parts, paragraph_buffer)
                close_list(parts, state)
                in_code = True
                code_lang = fence.group(1) or "code"
            continue

        if in_code:
            code_buffer.append(line)
            continue

        if not line.strip():
            flush_paragraph(parts, paragraph_buffer)
            close_list(parts, state)
            continue

        if line.strip() == "---":
            flush_paragraph(parts, paragraph_buffer)
            close_list(parts, state)
            parts.append('<hr class="section-rule">')
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_paragraph(parts, paragraph_buffer)
            close_list(parts, state)
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if first_h1 and level == 1:
                first_h1 = False
                continue
            first_h1 = False
            base_id = slugify(text)
            section_id = base_id
            n = 2
            while section_id in used_ids:
                section_id = f"{base_id}-{n}"
                n += 1
            used_ids.add(section_id)
            if level <= 2:
                toc.append({"id": section_id, "text": text})
                parts.append(f'<section class="lesson-section" id="{section_id}">')
                parts.append(f"<h2>{inline_markdown(text)}</h2>")
            elif level == 3:
                parts.append(f'<h3 id="{section_id}">{inline_markdown(text)}</h3>')
            else:
                parts.append(f'<h4 id="{section_id}">{inline_markdown(text)}</h4>')
            continue

        checklist = re.match(r"^\s*-\s+\[( |x|X)\]\s+(.+)$", line)
        bullet = re.match(r"^\s*-\s+(.+)$", line)
        numbered = re.match(r"^\s*\d+\.\s+(.+)$", line)

        if checklist:
            flush_paragraph(parts, paragraph_buffer)
            if state["list"] != "check":
                close_list(parts, state)
                parts.append('<div class="checklist">')
                state["list"] = "check"
            checked = " checked" if checklist.group(1).lower() == "x" else ""
            label = inline_markdown(checklist.group(2))
            parts.append(f'<label class="check-item"><input type="checkbox"{checked}> <span>{label}</span></label>')
            continue

        if bullet:
            flush_paragraph(parts, paragraph_buffer)
            if state["list"] != "ul":
                close_list(parts, state)
                parts.append("<ul>")
                state["list"] = "ul"
            parts.append(f"<li>{inline_markdown(bullet.group(1))}</li>")
            continue

        if numbered:
            flush_paragraph(parts, paragraph_buffer)
            if state["list"] != "ol":
                close_list(parts, state)
                parts.append("<ol>")
                state["list"] = "ol"
            parts.append(f"<li>{inline_markdown(numbered.group(1))}</li>")
            continue

        paragraph_buffer.append(line)

    flush_paragraph(parts, paragraph_buffer)
    close_list(parts, state)
    return "\n".join(parts).replace("</section>\n<section", "<section"), toc


def build_index(content: str, toc: list[dict[str, str]]) -> str:
    toc_links = "\n".join(
        f'<a href="#{item["id"]}" data-section="{item["id"]}">{html.escape(item["text"])}</a>' for item in toc
    )
    return f"""<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tutorial Flutter Dasar untuk Pemula</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="top-progress" id="topProgress"></div>
  <button class="menu-toggle" id="menuToggle" aria-label="Buka daftar isi">☰</button>
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <span class="brand-mark">F</span>
      <div>
        <strong>Flutter Dasar</strong>
        <small>Modul belajar pemula</small>
      </div>
    </div>
    <label class="search-box">
      <span>Cari materi</span>
      <input id="searchInput" type="search" placeholder="widget, state, API...">
    </label>
    <nav class="toc" id="toc">
      {toc_links}
    </nav>
  </aside>
  <main class="page">
    <header class="hero">
      <p class="eyebrow">Web pembelajaran interaktif</p>
      <h1>Tutorial Flutter Dasar untuk Pemula</h1>
      <p class="lead">Belajar Flutter dari setup sampai mini project dengan alur yang mudah diikuti: pahami konsep, jalankan contoh, lalu modifikasi sendiri.</p>
      <div class="hero-actions">
        <a class="primary-action" href="#apa-itu-flutter">Mulai belajar</a>
        <button class="secondary-action" id="resetChecklist" type="button">Reset checklist</button>
      </div>
      <div class="stats">
        <div><strong>{len(toc)}</strong><span>bagian materi</span></div>
        <div><strong>1</strong><span>mini project</span></div>
        <div><strong>0</strong><span>dependency web</span></div>
      </div>
    </header>
    <article class="content" id="content">
      {content}
    </article>
  </main>
  <button class="back-top" id="backTop" type="button" aria-label="Kembali ke atas">↑</button>
  <script src="script.js"></script>
</body>
</html>
"""


CSS = r"""
:root {
  --bg: #f6f3ec;
  --surface: #fffdf8;
  --ink: #102027;
  --muted: #607076;
  --line: #ded7c9;
  --flutter: #00a6b4;
  --green: #78c257;
  --amber: #f6b945;
  --coral: #ef6f61;
  --violet: #6b5dd3;
  --code-bg: #102f35;
  --code-ink: #d8fffb;
  --shadow: 0 24px 60px rgba(16, 32, 39, .10);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.65;
}

.top-progress {
  position: fixed;
  inset: 0 auto auto 0;
  height: 4px;
  width: 0;
  background: linear-gradient(90deg, var(--flutter), var(--green), var(--amber));
  z-index: 20;
}

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: 320px;
  padding: 28px 22px;
  background: #123238;
  color: white;
  overflow: auto;
  z-index: 10;
}

.brand {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 28px;
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  background: var(--flutter);
  color: white;
  font-weight: 800;
}

.brand strong, .brand small { display: block; }
.brand small { color: #b7ced1; }

.search-box span {
  display: block;
  color: #cbe0e2;
  font-size: 13px;
  margin-bottom: 8px;
}

.search-box input {
  width: 100%;
  border: 1px solid #31575e;
  background: #0c272d;
  color: white;
  padding: 12px 14px;
  outline: none;
}

.search-box input:focus { border-color: var(--flutter); }

.toc {
  display: grid;
  gap: 4px;
  margin-top: 22px;
}

.toc a {
  color: #d8eeee;
  text-decoration: none;
  padding: 9px 10px;
  border-left: 3px solid transparent;
  font-size: 14px;
}

.toc a:hover, .toc a.active {
  background: rgba(255, 255, 255, .08);
  border-left-color: var(--flutter);
}

.page {
  margin-left: 320px;
  min-height: 100vh;
}

.hero {
  padding: 72px 8vw 54px;
  background:
    linear-gradient(135deg, rgba(0,166,180,.14), transparent 34%),
    linear-gradient(155deg, transparent 58%, rgba(246,185,69,.22)),
    var(--surface);
  border-bottom: 1px solid var(--line);
}

.eyebrow {
  margin: 0 0 14px;
  color: var(--flutter);
  font-weight: 800;
  text-transform: uppercase;
  font-size: 13px;
  letter-spacing: .08em;
}

h1 {
  max-width: 900px;
  margin: 0;
  font-size: 56px;
  line-height: 1.04;
}

.lead {
  max-width: 760px;
  margin: 24px 0 0;
  font-size: 21px;
  color: var(--muted);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 30px;
}

.primary-action, .secondary-action {
  border: 0;
  padding: 12px 18px;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
  text-decoration: none;
}

.primary-action {
  background: var(--flutter);
  color: white;
}

.secondary-action {
  background: #e9e3d6;
  color: var(--ink);
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(120px, 1fr));
  max-width: 720px;
  gap: 1px;
  margin-top: 36px;
  background: var(--line);
  border: 1px solid var(--line);
}

.stats div {
  background: var(--surface);
  padding: 18px;
}

.stats strong, .stats span { display: block; }
.stats strong { font-size: 28px; }
.stats span { color: var(--muted); font-size: 14px; }

.content {
  max-width: 960px;
  padding: 40px 8vw 96px;
}

.lesson-section {
  padding: 42px 0;
  border-bottom: 1px solid var(--line);
}

.lesson-section:target h2 {
  color: #007986;
}

h2 {
  margin: 0 0 20px;
  font-size: 34px;
  line-height: 1.15;
}

h3 {
  margin: 30px 0 10px;
  font-size: 23px;
  color: #1d5f8f;
}

h4 {
  margin: 24px 0 8px;
  font-size: 18px;
}

p { margin: 0 0 16px; }
ul, ol { margin: 0 0 18px; padding-left: 25px; }
li { margin: 6px 0; }
code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  background: #e9f3f3;
  color: #005d67;
  padding: 2px 5px;
  font-size: .92em;
}

.code-card {
  margin: 20px 0 24px;
  background: var(--code-bg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.code-label {
  padding: 10px 16px;
  color: #9ee7e2;
  font-size: 12px;
  text-transform: uppercase;
  font-weight: 800;
  border-bottom: 1px solid rgba(255,255,255,.12);
}

pre {
  margin: 0;
  padding: 20px;
  overflow-x: auto;
}

pre code {
  background: transparent;
  color: var(--code-ink);
  padding: 0;
  font-size: 14px;
}

.checklist {
  display: grid;
  gap: 8px;
  margin: 18px 0;
}

.check-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 12px 14px;
  background: var(--surface);
  border: 1px solid var(--line);
}

.check-item input {
  margin-top: 5px;
  accent-color: var(--flutter);
}

.section-rule {
  border: 0;
  border-top: 1px solid var(--line);
  margin: 28px 0;
}

.back-top, .menu-toggle {
  position: fixed;
  border: 0;
  background: var(--ink);
  color: white;
  width: 44px;
  height: 44px;
  cursor: pointer;
  z-index: 30;
}

.back-top {
  right: 22px;
  bottom: 22px;
  opacity: 0;
  pointer-events: none;
  transition: opacity .2s ease;
}

.back-top.visible {
  opacity: 1;
  pointer-events: auto;
}

.menu-toggle {
  display: none;
  left: 16px;
  top: 16px;
}

.hidden-by-search { display: none; }

@media (max-width: 960px) {
  .menu-toggle { display: block; }
  .sidebar {
    transform: translateX(-100%);
    transition: transform .2s ease;
    width: min(86vw, 340px);
  }
  .sidebar.open { transform: translateX(0); }
  .page { margin-left: 0; }
  .hero { padding-top: 86px; }
  h1 { font-size: 42px; }
  .stats { grid-template-columns: 1fr; }
}

@media (max-width: 560px) {
  .content, .hero { padding-left: 24px; padding-right: 24px; }
  h1 { font-size: 34px; }
  h2 { font-size: 28px; }
  .lead { font-size: 18px; }
}
"""


JS = r"""
const sidebar = document.getElementById("sidebar");
const menuToggle = document.getElementById("menuToggle");
const searchInput = document.getElementById("searchInput");
const topProgress = document.getElementById("topProgress");
const backTop = document.getElementById("backTop");
const resetChecklist = document.getElementById("resetChecklist");
const sections = [...document.querySelectorAll(".lesson-section")];
const tocLinks = [...document.querySelectorAll(".toc a")];
const checklistInputs = [...document.querySelectorAll(".check-item input")];

menuToggle.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

tocLinks.forEach((link) => {
  link.addEventListener("click", () => {
    sidebar.classList.remove("open");
  });
});

function updateProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const progress = max > 0 ? (window.scrollY / max) * 100 : 0;
  topProgress.style.width = `${progress}%`;
  backTop.classList.toggle("visible", window.scrollY > 500);

  let current = sections[0]?.id;
  for (const section of sections) {
    if (section.getBoundingClientRect().top < 160) {
      current = section.id;
    }
  }
  tocLinks.forEach((link) => {
    link.classList.toggle("active", link.dataset.section === current);
  });
}

window.addEventListener("scroll", updateProgress, { passive: true });
updateProgress();

backTop.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

searchInput.addEventListener("input", () => {
  const term = searchInput.value.trim().toLowerCase();
  sections.forEach((section) => {
    const match = !term || section.textContent.toLowerCase().includes(term);
    section.classList.toggle("hidden-by-search", !match);
  });
});

checklistInputs.forEach((input, index) => {
  const key = `flutter-basic-check-${index}`;
  input.checked = localStorage.getItem(key) === "true" || input.checked;
  input.addEventListener("change", () => {
    localStorage.setItem(key, String(input.checked));
  });
});

resetChecklist.addEventListener("click", () => {
  checklistInputs.forEach((input, index) => {
    input.checked = false;
    localStorage.removeItem(`flutter-basic-check-${index}`);
  });
});
"""


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    content, toc = convert_markdown(markdown)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    (WEB_DIR / "index.html").write_text(build_index(content, toc), encoding="utf-8")
    (WEB_DIR / "styles.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (WEB_DIR / "script.js").write_text(JS.strip() + "\n", encoding="utf-8")
    print(WEB_DIR / "index.html")


if __name__ == "__main__":
    main()
