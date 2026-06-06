import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const payload = await readStdin();
const dataDir =
  process.env.CODEX_UTILITIES_DATA_DIR ??
  path.join(os.homedir(), ".codex", "codex-utilities", "hooks");
const logPath = path.join(dataDir, "session-start.jsonl");

fs.mkdirSync(dataDir, { recursive: true });
fs.appendFileSync(logPath, `${payload.trimEnd()}\n`);

async function readStdin() {
  let buffer = "";
  process.stdin.setEncoding("utf8");

  for await (const chunk of process.stdin) {
    buffer += chunk;
  }

  return buffer;
}
