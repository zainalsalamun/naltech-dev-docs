from pathlib import Path

from build_tutorial_web import convert_markdown


ROOT = Path(__file__).resolve().parent
BASIC_SOURCE = ROOT / "tutorial-flutter-dasar-pemula.md"
ADVANCED_SOURCE = ROOT / "tutorial-flutter-lanjutan.md"
COMBINED_SOURCE = ROOT / "tutorial-flutter-lengkap.md"
WEB_DIR = ROOT / "web"


def build_combined_markdown() -> str:
    basic = BASIC_SOURCE.read_text(encoding="utf-8").strip()
    advanced = ADVANCED_SOURCE.read_text(encoding="utf-8").strip()
    return basic + "\n\n---\n\n# Bagian 2: Materi Flutter Lanjutan\n\n" + advanced + "\n"


def build_index(content: str, toc: list[dict[str, str]]) -> str:
    toc_links = "\n".join(
        f'<a href="#{item["id"]}" data-section="{item["id"]}">{item["text"]}</a>' for item in toc
    )
    return f"""<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tutorial Flutter Lengkap: Dasar sampai Lanjutan</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="top-progress" id="topProgress"></div>
  <button class="menu-toggle" id="menuToggle" aria-label="Buka daftar isi">☰</button>
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <span class="brand-mark">F</span>
      <div>
        <strong>Flutter Lengkap</strong>
        <small>Dasar sampai lanjutan</small>
      </div>
    </div>
    <label class="search-box">
      <span>Cari materi</span>
      <input id="searchInput" type="search" placeholder="widget, state, repository...">
    </label>
    <nav class="toc" id="toc">
      {toc_links}
    </nav>
  </aside>
  <main class="page">
    <header class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Complete Flutter learning workspace</p>
        <h1>Tutorial Flutter Lengkap</h1>
        <p class="lead">Satu halaman belajar dari Flutter dasar sampai lanjutan: widget, layout, state, API, local storage, repository, CRUD, testing, dan persiapan publish.</p>
        <div class="hero-actions">
          <a class="primary-action" href="#daftar-isi">Mulai dari dasar</a>
          <a class="secondary-action" href="#bagian-2-materi-flutter-lanjutan">Lompat ke lanjutan</a>
          <button class="secondary-action" id="resetChecklist" type="button">Reset checklist</button>
        </div>
        <div class="stats">
          <div><strong>{len(toc)}</strong><span>bagian materi</span></div>
          <div><strong>2</strong><span>mini project</span></div>
          <div><strong>CRUD</strong><span>target akhir</span></div>
        </div>
      </div>
      <div class="hero-visual" aria-hidden="true">
        <div class="workspace-card">
          <div class="window-bar">
            <span></span><span></span><span></span>
            <em>flutter_complete_path.dart</em>
          </div>
          <div class="code-grid">
            <div class="code-pane">
              <b>class FlutterPath</b>
              <i>widgets.compose()</i>
              <i>state.manage()</i>
              <i>repository.fetch()</i>
              <i>tests.verify()</i>
            </div>
            <div class="ai-pane">
              <span>AI mentor</span>
              <strong>Full path</strong>
              <p>From first widget to scalable task manager.</p>
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
    combined = build_combined_markdown()
    COMBINED_SOURCE.write_text(combined, encoding="utf-8")
    content, toc = convert_markdown(combined)
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    (WEB_DIR / "index.html").write_text(build_index(content, toc), encoding="utf-8")
    print(WEB_DIR / "index.html")
    print(COMBINED_SOURCE)


if __name__ == "__main__":
    main()
