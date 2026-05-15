const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");

assert.match(
  html,
  /const bookingApiUrl = "https:\/\/api\.lifebee\.tech\/api\/v3\/gateway\/booking";/,
  "booking form should post directly to the Gateway booking API"
);

assert.doesNotMatch(
  html,
  /\/api\/booking/,
  "frontend should not post through a same-origin backend proxy"
);

assert.match(
  html,
  /"Content-Type": "application\/x-www-form-urlencoded;charset=UTF-8"/,
  "booking request should use form-urlencoded content type"
);

for (const field of ["name", "phone", "email"]) {
  assert.match(html, new RegExp(`name="${field}"`), `booking form should include ${field}`);
}

console.log("frontend booking integration test passed");
