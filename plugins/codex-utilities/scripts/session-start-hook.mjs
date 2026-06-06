import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const pluginRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function handleThreadTitle(payload, config) {
  const eventName =
    typeof payload.hook_event_name === "string" && payload.hook_event_name.trim()
      ? payload.hook_event_name.trim()
      : "unknown";
  if (!["SessionStart", "Stop"].includes(eventName)) {
    return {
      at: new Date().toISOString(),
      eventName,
      mode: config.mode,
      action: "ignored",
      reason: "Thread title prefixing only handles SessionStart and Stop hook events.",
    };
  }

  const threadId = threadIdFromPayload(payload);
  const base = {
    at: new Date().toISOString(),
    eventName,
    mode: config.mode,
    source: payload.source ?? null,
    sessionId: threadId,
    turnId: typeof payload.turn_id === "string" ? payload.turn_id : null,
    cwd: typeof payload.cwd === "string" ? payload.cwd : null,
  };

  if (config.mode === "capture") {
    return { ...base, action: "capture-only" };
  }

  if (!threadId) {
    return {
      ...base,
      action: "skipped",
      reason: "Codex hook payload did not include session_id or thread_id.",
    };
  }

  const prefixPlan = titlePrefixPlanFromPayload(payload, config);
  if (!prefixPlan.prefix) {
    return {
      ...base,
      action: "skipped",
      reason: prefixPlan.reason,
    };
  }

  if (eventName !== "Stop") {
    return {
      ...base,
      action: "skipped",
      prefix: prefixPlan.prefix,
      reason: "Generated title prefixing waits for the Stop hook because SessionStart runs before Codex creates a thread title.",
    };
  }

  const state = readState(config.statePath);
  if (state.threads[threadId]?.applied === true) {
    return {
      ...base,
      action: "skipped",
      prefix: prefixPlan.prefix,
      reason: "Thread title prefix was already handled for this thread.",
    };
  }

  const stopCount = stopCountForThread(state, threadId) + 1;
  if (stopCount < config.minStopCountBeforeRename) {
    writeThreadState(config.statePath, state, threadId, {
      ...state.threads[threadId],
      applied: false,
      lastStopAt: new Date().toISOString(),
      stopCount,
    });
    return {
      ...base,
      action: "skipped",
      prefix: prefixPlan.prefix,
      reason: `Waiting for Stop hook ${config.minStopCountBeforeRename} before prefixing the generated thread title.`,
      stopCount,
    };
  }

  const threadRead = await readThreadWithGeneratedTitle(threadId, config);
  if (!threadRead.thread) {
    return {
      ...base,
      action: "failed",
      prefix: prefixPlan.prefix,
      reason: threadRead.reason,
      stopCount,
    };
  }

  const currentName = currentThreadName(threadRead.thread);
  if (!currentName) {
    return {
      ...base,
      action: "skipped",
      prefix: prefixPlan.prefix,
      reason: "Codex App Server did not return a generated thread title before the Stop hook timeout.",
      stopCount,
    };
  }

  const proposedName = prefixedThreadName(prefixPlan.prefix, currentName);
  const planned = {
    ...base,
    action: "planned",
    currentName,
    prefix: prefixPlan.prefix,
    proposedName,
    threadId,
  };

  if (proposedName === currentName) {
    writeThreadState(config.statePath, state, threadId, {
      ...state.threads[threadId],
      applied: true,
      at: new Date().toISOString(),
      currentName,
      proposedName,
      reason: "already-prefixed",
      stopCount,
    });
    return { ...planned, action: "already-prefixed", stopCount };
  }

  if (config.mode === "dry-run") {
    return { ...planned, stopCount };
  }

  try {
    await withAppServerClient(config, async (client) => {
      await client.request("thread/name/set", { threadId, name: proposedName });
    });
    writeThreadState(config.statePath, state, threadId, {
      ...state.threads[threadId],
      applied: true,
      at: new Date().toISOString(),
      currentName,
      proposedName,
      reason: "renamed",
      stopCount,
    });
    return { ...planned, action: "renamed", stopCount };
  } catch (error) {
    return {
      ...planned,
      action: "failed",
      reason: error instanceof Error ? error.message : String(error),
      stopCount,
    };
  }
}

function toolUseSummaryFromPayload(payload, config) {
  const eventName =
    typeof payload.hook_event_name === "string" && payload.hook_event_name.trim()
      ? payload.hook_event_name.trim()
      : "unknown";
  if (eventName !== "PostToolUse") {
    return null;
  }

  return {
    at: new Date().toISOString(),
    eventName,
    sessionId: threadIdFromPayload(payload),
    turnId: typeof payload.turn_id === "string" ? payload.turn_id : null,
    cwd: typeof payload.cwd === "string" ? payload.cwd : null,
    toolName: firstStringField(payload, [
      "tool_name",
      "toolName",
      "name",
      "tool",
      "function_name",
      "functionName",
    ]),
    toolId: firstStringField(payload, ["tool_id", "toolId", "call_id", "callId", "id"]),
    status: firstStringField(payload, ["status", "result", "outcome"]),
    payloadKeys: Object.keys(payload).sort(),
    payloadPath: config.payloadLogPath,
  };
}

function readConfig() {
  const dataDir =
    process.env.CODEX_UTILITIES_DATA_DIR ??
    path.join(os.homedir(), ".codex", "codex-utilities", "hooks");
  const mode = modeFromEnv(process.env.CODEX_UTILITIES_THREAD_TITLE_MODE);
  const maxPrefixLength = positiveIntegerFromEnv(
    process.env.CODEX_UTILITIES_THREAD_TITLE_MAX_PREFIX_LENGTH,
    48,
  );
  const projectlessRoot =
    process.env.CODEX_UTILITIES_PROJECTLESS_ROOT ??
    path.join(os.homedir(), "Documents", "Codex");
  const projectlessThreadPrefix = optionalTrimmedStringFromEnv(
    process.env.CODEX_UTILITIES_PROJECTLESS_THREAD_PREFIX,
  );
  const timeoutMs = positiveIntegerFromEnv(
    process.env.CODEX_UTILITIES_APP_SERVER_TIMEOUT_MS,
    2500,
  );
  const titlePollAttempts = positiveIntegerFromEnv(
    process.env.CODEX_UTILITIES_THREAD_TITLE_POLL_ATTEMPTS,
    4,
  );
  const titlePollDelayMs = positiveIntegerFromEnv(
    process.env.CODEX_UTILITIES_THREAD_TITLE_POLL_DELAY_MS,
    500,
  );
  const minStopCountBeforeRename = positiveIntegerFromEnv(
    process.env.CODEX_UTILITIES_THREAD_TITLE_MIN_STOP_COUNT,
    2,
  );

  return {
    appServerCommand: process.env.CODEX_UTILITIES_APP_SERVER_COMMAND ?? "codex",
    appServerArgs: ["app-server"],
    dataDir,
    decisionLogPath: path.join(dataDir, "thread-title-decisions.jsonl"),
    maxPrefixLength,
    minStopCountBeforeRename,
    mode,
    payloadLogPath: path.join(dataDir, "thread-title-payloads.jsonl"),
    pluginVersion: readPluginVersion(pluginRoot),
    projectlessRoot,
    projectlessThreadPrefix,
    statePath: path.join(dataDir, "thread-title-state.json"),
    timeoutMs,
    titlePollAttempts,
    titlePollDelayMs,
    toolUseLogPath: path.join(dataDir, "tool-use-events.jsonl"),
  };
}

function readPluginVersion(pluginRoot) {
  const manifestPath = path.join(pluginRoot, ".codex-plugin", "plugin.json");
  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    if (typeof manifest.version === "string" && manifest.version.trim()) {
      return manifest.version.trim();
    }
  } catch {
    return "unknown";
  }
  return "unknown";
}

function modeFromEnv(rawMode) {
  const mode = (rawMode ?? "rename").trim().toLowerCase();
  if (["capture", "dry-run", "rename"].includes(mode)) {
    return mode;
  }
  return "rename";
}

function positiveIntegerFromEnv(rawValue, fallback) {
  const parsed = Number.parseInt(rawValue ?? "", 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function optionalTrimmedStringFromEnv(rawValue) {
  if (typeof rawValue !== "string") {
    return null;
  }
  const trimmed = rawValue.trim();
  return trimmed ? trimmed : null;
}

function firstStringField(payload, keys) {
  for (const key of keys) {
    if (typeof payload[key] === "string" && payload[key].trim()) {
      return payload[key].trim();
    }
  }
  return null;
}

function threadIdFromPayload(payload) {
  for (const key of ["thread_id", "threadId", "session_id", "sessionId"]) {
    if (typeof payload[key] === "string" && payload[key].trim()) {
      return payload[key].trim();
    }
  }
  return null;
}

function titlePrefixPlanFromPayload(payload, config) {
  if (typeof payload.cwd !== "string") {
    return {
      prefix: null,
      reason: "Codex hook payload did not include a usable cwd for title prefixing.",
    };
  }
  if (isProjectlessCodexChatCwd(payload.cwd, config.projectlessRoot)) {
    if (config.projectlessThreadPrefix) {
      return {
        prefix: truncateTitlePrefix(config.projectlessThreadPrefix, config.maxPrefixLength),
        reason: null,
      };
    }
    return {
      prefix: null,
      reason:
        "Hook cwd looks like a projectless Codex chat directory, and no projectless title prefix is configured.",
    };
  }
  const prefix = path.basename(payload.cwd).replace(/\s+/g, " ").trim();
  if (!prefix) {
    return {
      prefix: null,
      reason: "Hook payload cwd did not include a usable final path component.",
    };
  }
  return {
    prefix: truncateTitlePrefix(prefix, config.maxPrefixLength),
    reason: null,
  };
}

function isProjectlessCodexChatCwd(cwd, projectlessRoot) {
  const relativePath = path.relative(path.resolve(projectlessRoot), path.resolve(cwd));
  if (!relativePath || relativePath.startsWith("..") || path.isAbsolute(relativePath)) {
    return false;
  }
  const [datePart] = relativePath.split(path.sep);
  return /^\d{4}-\d{2}-\d{2}$/.test(datePart);
}

function truncateTitlePrefix(prefix, maxPrefixLength) {
  return prefix.length > maxPrefixLength ? prefix.slice(0, maxPrefixLength).trim() : prefix;
}

function prefixedThreadName(prefix, currentName) {
  return currentName.startsWith(`${prefix}: `) ? currentName : `${prefix}: ${currentName}`;
}

function currentThreadName(thread) {
  if (typeof thread.name === "string" && thread.name.trim()) {
    return thread.name.trim();
  }
  if (typeof thread.title === "string" && thread.title.trim()) {
    return thread.title.trim();
  }
  return null;
}

async function readThreadWithGeneratedTitle(threadId, config) {
  let lastReason = "Codex App Server did not return thread data.";
  for (let attempt = 1; attempt <= config.titlePollAttempts; attempt += 1) {
    try {
      const response = await withAppServerClient(config, (client) =>
        client.request("thread/read", { threadId, includeTurns: false }),
      );
      if (response?.thread) {
        const name = currentThreadName(response.thread);
        if (name || attempt === config.titlePollAttempts) {
          return { thread: response.thread };
        }
        lastReason = "Codex App Server returned the thread before a generated title was available.";
      }
    } catch (error) {
      lastReason = error instanceof Error ? error.message : String(error);
      break;
    }
    await delay(config.titlePollDelayMs);
  }
  return { thread: null, reason: lastReason };
}

async function withAppServerClient(config, callback) {
  const client = new JsonRpcStdioClient(config);
  try {
    await client.start();
    await client.request("initialize", {
      clientInfo: {
        name: "codex_utilities_hook",
        title: "Codex Utilities Hook",
        version: config.pluginVersion,
      },
      capabilities: {
        experimentalApi: true,
        optOutNotificationMethods: ["thread/name/updated"],
      },
    });
    client.notify("initialized", {});
    return await callback(client);
  } finally {
    client.close();
  }
}

class JsonRpcStdioClient {
  constructor(config) {
    this.config = config;
    this.nextId = 1;
    this.outputBuffer = "";
    this.pending = new Map();
    this.process = null;
  }

  async start() {
    this.process = spawn(this.config.appServerCommand, this.config.appServerArgs, {
      stdio: ["pipe", "pipe", "pipe"],
    });
    this.process.stdout.setEncoding("utf8");
    this.process.stdout.on("data", (chunk) => this.receive(chunk));
    this.process.stderr.on("data", () => {
      return;
    });
    this.process.on("error", (error) => this.fail(error));
    this.process.on("exit", (code, signal) => {
      if (this.pending.size === 0) {
        return;
      }
      const detail = signal ? `signal ${signal}` : `exit code ${code}`;
      this.fail(new Error(`Codex App Server exited before responding (${detail}).`));
    });
  }

  request(method, params) {
    const id = this.nextId++;
    this.send({ id, method, params });
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Timed out waiting for ${method} response from Codex App Server.`));
      }, this.config.timeoutMs);
      this.pending.set(id, { method, resolve, reject, timer });
    });
  }

  notify(method, params) {
    this.send({ method, params });
  }

  send(message) {
    this.process.stdin.write(`${JSON.stringify(message)}\n`);
  }

  receive(chunk) {
    this.outputBuffer += chunk;
    const lines = this.outputBuffer.split("\n");
    this.outputBuffer = lines.pop() ?? "";
    for (const line of lines) {
      if (!line.trim()) {
        continue;
      }
      this.routeMessage(line);
    }
  }

  routeMessage(line) {
    let message;
    try {
      message = JSON.parse(line);
    } catch {
      return;
    }
    if (!Object.hasOwn(message, "id")) {
      return;
    }
    const pending = this.pending.get(message.id);
    if (!pending) {
      return;
    }
    clearTimeout(pending.timer);
    this.pending.delete(message.id);
    if (message.error) {
      pending.reject(
        new Error(
          `${pending.method} failed: ${message.error.message ?? "unknown JSON-RPC error"}`,
        ),
      );
      return;
    }
    pending.resolve(message.result ?? {});
  }

  fail(error) {
    for (const pending of this.pending.values()) {
      clearTimeout(pending.timer);
      pending.reject(error);
    }
    this.pending.clear();
  }

  close() {
    if (!this.process) {
      return;
    }
    try {
      this.process.stdin.end();
    } catch {
      return;
    }
    if (!this.process.killed) {
      this.process.kill();
    }
  }
}

function readState(statePath) {
  try {
    const parsed = JSON.parse(fs.readFileSync(statePath, "utf8"));
    if (
      parsed &&
      typeof parsed === "object" &&
      parsed.threads &&
      typeof parsed.threads === "object" &&
      !Array.isArray(parsed.threads)
    ) {
      return parsed;
    }
  } catch {
    return { threads: {} };
  }
  return { threads: {} };
}

function stopCountForThread(state, threadId) {
  const rawStopCount = state.threads[threadId]?.stopCount;
  return Number.isInteger(rawStopCount) && rawStopCount > 0 ? rawStopCount : 0;
}

function writeThreadState(statePath, state, threadId, entry) {
  const nextState = {
    ...state,
    threads: {
      ...state.threads,
      [threadId]: entry,
    },
  };
  fs.writeFileSync(statePath, `${JSON.stringify(nextState, null, 2)}\n`);
}

function parsePayload(payloadText) {
  if (!payloadText.trim()) {
    return {};
  }
  try {
    const parsed = JSON.parse(payloadText);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
  } catch {
    return {};
  }
}

function appendJsonl(filePath, line) {
  fs.appendFileSync(filePath, `${line}\n`);
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function readStdin() {
  let buffer = "";
  process.stdin.setEncoding("utf8");

  for await (const chunk of process.stdin) {
    buffer += chunk;
  }

  return buffer;
}

const payloadText = await readStdin();
const payload = parsePayload(payloadText);
const config = readConfig();

fs.mkdirSync(config.dataDir, { recursive: true });
appendJsonl(config.payloadLogPath, payloadText.trimEnd() || "{}");

const toolUseSummary = toolUseSummaryFromPayload(payload, config);
if (toolUseSummary) {
  appendJsonl(config.toolUseLogPath, JSON.stringify(toolUseSummary));
}

const decision = await handleThreadTitle(payload, config);
appendJsonl(config.decisionLogPath, JSON.stringify(decision));
