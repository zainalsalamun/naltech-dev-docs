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
