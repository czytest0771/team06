const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const dist = path.join(root, "dist");
const sourceIndex = path.join(root, "src", "frontend", "index.html");
const sourceAssets = path.join(root, "src", "public", "assets");
const targetAssets = path.join(dist, "public", "assets");

fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(targetAssets, { recursive: true });

let html = fs.readFileSync(sourceIndex, "utf8");
html = html.replaceAll("../public/assets/", "public/assets/");

fs.writeFileSync(path.join(dist, "index.html"), html);
fs.cpSync(sourceAssets, targetAssets, { recursive: true });

console.log("Cloudflare Pages build complete: dist/");
