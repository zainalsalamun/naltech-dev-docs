from pathlib import Path

from build_tutorial_web import convert_markdown


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "tutorial-flutter-lanjutan.md"
WEB_DIR = ROOT / "web"


def build_index(content: str, toc: list[dict[str, str]]) -> str:
    toc_links = "\n".join(
        f'<a href="#{item["id"]}" data-section="{item["id"]}">{item["text"]}</a>' for item in toc
    )
    return f"""<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tutorial Flutter Lanjutan</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="top-progress" id="topProgress"></div>
  <button class="menu-toggle" id="menuToggle" aria-label="Buka daftar isi">☰</button>
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <span class="brand-mark">F</span>
      <div>
        <strong>Flutter Lanjutan</strong>
        <small>Modul naik level</small>
      </div>
    </div>
    <label class="search-box">
      <span>Cari materi</span>
      <input id="searchInput" type="search" placeholder="repository, state, testing...">
    </label>
    <nav class="toc" id="toc">
      <a href="index.html">← Materi Dasar</a>
      {toc_links}
    </nav>
  </aside>
  <main class="page">
    <header class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Next level Flutter engineering</p>
        <h1>Tutorial Flutter Lanjutan</h1>
        <p class="lead">Lanjutkan dari widget dan state sederhana menuju project yang lebih rapi: arsitektur folder, repository, state management, CRUD, local storage, testing, dan persiapan publish.</p>
        <div class="hero-actions">
          <a class="primary-action" href="#1-kapan-harus-naik-dari-dasar-ke-lanjutan">Mulai materi lanjutan</a>
          <a class="secondary-action" href="index.html">Kembali ke dasar</a>
        </div>
        <div class="stats">
          <div><strong>{len(toc)}</strong><span>bagian lanjutan</span></div>
          <div><strong>1</strong><span>mini project baru</span></div>
          <div><strong>CRUD</strong><span>target praktik</span></div>
        </div>
      </div>
      <div class="hero-visual" aria-hidden="true">
        <div class="workspace-card">
          <div class="window-bar">
            <span></span><span></span><span></span>
            <em>task_manager_architecture.dart</em>
          </div>
          <div class="code-grid">
            <div class="code-pane">
              <b>feature/tasks</b>
              <i>models/task.dart</i>
              <i>data/repository.dart</i>
              <i>pages/task_list.dart</i>
              <i>widgets/task_card.dart</i>
            </div>
            <div class="ai-pane">
              <span>AI mentor</span>
              <strong>Upgrade</strong>
              <p>Move from screens to scalable app structure.</p>
            </div>
          </div>
          <div class="signal-row">
            <span></span><span></span><span></span><span></span>
          </div>
        </div>
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


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    content, toc = convert_markdown(markdown)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    (WEB_DIR / "lanjutan.html").write_text(build_index(content, toc), encoding="utf-8")
    print(WEB_DIR / "lanjutan.html")


if __name__ == "__main__":
    main()
