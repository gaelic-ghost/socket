#!/usr/bin/env node

import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptPath = fileURLToPath(import.meta.url);
const hookRoot = path.resolve(path.dirname(scriptPath), "..");

process.env.CODEX_HOOK_TTS_DATA_DIR ??= hookRoot;

await import("../../hooks/stop-tts.mjs");
