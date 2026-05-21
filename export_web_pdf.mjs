import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/macbookpro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

const root = "/Users/macbookpro/Documents/Codex/2026-05-19/buatkan-tutorial-flutter-dasar-untuk-pemula";
const input = path.join(root, "web", "index.html");
const output = path.join(root, "web", "tutorial-flutter-dasar-pemula-web.pdf");
const chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const browser = await chromium.launch({
  executablePath: chrome,
  headless: true,
});

const page = await browser.newPage({
  viewport: { width: 1440, height: 1200 },
});

await page.goto(pathToFileURL(input).href, { waitUntil: "networkidle" });
await page.emulateMedia({ media: "print" });
await page.pdf({
  path: output,
  format: "A4",
  printBackground: true,
  preferCSSPageSize: true,
  displayHeaderFooter: false,
});

await browser.close();
console.log(output);
