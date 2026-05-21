import fs from "node:fs/promises";
import path from "node:path";

const root = process.cwd();

const docs = [
  {
    source: "tutorial-flutter-dasar-pemula.md",
    target: "src/content/docs/flutter/dasar.md",
    frontmatter: {
      title: "Tutorial Flutter Dasar untuk Pemula",
      description: "Materi fondasi Flutter: setup, Dart dasar, widget, layout, state, navigasi, form, API, storage, dan mini project catatan belajar.",
      category: "Flutter",
      level: "Beginner",
      order: 10,
      tags: ["flutter", "dart", "widget", "state", "pemula"],
      updated: "2026-05-20",
    },
  },
  {
    source: "tutorial-flutter-lanjutan.md",
    target: "src/content/docs/flutter/lanjutan.md",
    frontmatter: {
      title: "Tutorial Flutter Lanjutan",
      description: "Materi lanjutan Flutter: struktur folder, repository, state management, CRUD, local storage, testing, build, dan publish.",
      category: "Flutter",
      level: "Intermediate",
      order: 20,
      tags: ["flutter", "architecture", "repository", "crud", "testing"],
      updated: "2026-05-20",
    },
  },
];

function yamlValue(value) {
  if (Array.isArray(value)) {
    return `[${value.map((item) => JSON.stringify(item)).join(", ")}]`;
  }
  if (typeof value === "number") return String(value);
  return JSON.stringify(value);
}

function frontmatterBlock(data) {
  const lines = Object.entries(data).map(([key, value]) => `${key}: ${yamlValue(value)}`);
  return `---\n${lines.join("\n")}\n---\n\n`;
}

for (const doc of docs) {
  const sourcePath = path.join(root, doc.source);
  const targetPath = path.join(root, doc.target);
  const content = await fs.readFile(sourcePath, "utf8");
  await fs.mkdir(path.dirname(targetPath), { recursive: true });
  await fs.writeFile(targetPath, frontmatterBlock(doc.frontmatter) + content, "utf8");
  console.log(targetPath);
}
