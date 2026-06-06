import crypto from "node:crypto";
import fs from "node:fs";
import net from "node:net";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const pluginRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const payloadText = await readStdin();
const payload = parsePayload(payloadText);
const config = readConfig();

fs.mkdirSync(config.dataDir, { recursive: true });
appendJsonl(config.payloadLogPath, payloadText.trimEnd() || "{}");

const decision = await handleThreadTitle(payload, config);
appendJsonl(config.decisionLogPath, JSON.stringify(decision));

async function handleThreadTitle(payload, config) {
  const base = {
    at: new Date().toISOString(),
    mode: config.mode,
    source: payload.source ?? null,
    sessionId: threadIdFromPayload(payload),
    cwd: typeof payload.cwd === "string" ? payload.cwd : null,
  };

  if (config.mode === "capture") {
    return { ...base, action: "capture-only" };
  }

  const threadId = threadIdFromPayload(payload);
  if (!threadId) {
    return {
      ...base,
      action: "skipped",
      reason: "SessionStart payload did not include session_id or thread_id.",
    };
  }

  const prefix = titlePrefixFromPayload(payload, config);
  if (!prefix) {
    return {
      ...base,
      action: "skipped",
      reason: "SessionStart payload did not include a usable cwd for title prefixing.",
    };
  }

  const proposedName = prefix;
  const planned = { ...base, action: "planned", threadId, proposedName };
  if (config.mode === "dry-run") {
    return planned;
  }

  try {
    await setThreadName({
      socketPath: config.socketPath,
      threadId,
      name: proposedName,
      timeoutMs: config.timeoutMs,
    });
    return { ...planned, action: "renamed" };
  } catch (error) {
    return {
      ...planned,
      action: "failed",
      reason: error instanceof Error ? error.message : String(error),
    };
  }
}

function readConfig() {
  const dataDir =
    process.env.CODEX_UTILITIES_DATA_DIR ??
    path.join(os.homedir(), ".codex", "codex-utilities", "hooks");
  const codexHome = process.env.CODEX_HOME ?? path.join(os.homedir(), ".codex");
  const socketPath =
    process.env.CODEX_UTILITIES_APP_SERVER_SOCKET ??
    path.join(codexHome, "app-server-control", "app-server-control.sock");
  const mode = modeFromEnv(process.env.CODEX_UTILITIES_THREAD_TITLE_MODE);
  const maxPrefixLength = positiveIntegerFromEnv(
    process.env.CODEX_UTILITIES_THREAD_TITLE_MAX_PREFIX_LENGTH,
    48,
  );
  const timeoutMs = positiveIntegerFromEnv(
    process.env.CODEX_UTILITIES_APP_SERVER_TIMEOUT_MS,
    1500,
  );

  return {
    dataDir,
    decisionLogPath: path.join(dataDir, "thread-title-decisions.jsonl"),
    maxPrefixLength,
    mode,
    payloadLogPath: path.join(dataDir, "session-start.jsonl"),
    pluginVersion: readPluginVersion(pluginRoot),
    socketPath,
    timeoutMs,
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
  const mode = (rawMode ?? "capture").trim().toLowerCase();
  if (["capture", "dry-run", "rename"].includes(mode)) {
    return mode;
  }
  return "capture";
}

function positiveIntegerFromEnv(rawValue, fallback) {
  const parsed = Number.parseInt(rawValue ?? "", 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function threadIdFromPayload(payload) {
  for (const key of ["thread_id", "threadId", "session_id", "sessionId"]) {
    if (typeof payload[key] === "string" && payload[key].trim()) {
      return payload[key].trim();
    }
  }
  return null;
}

function titlePrefixFromPayload(payload, config) {
  if (typeof payload.cwd !== "string") {
    return null;
  }
  const prefix = path.basename(payload.cwd).replace(/\s+/g, " ").trim();
  if (!prefix) {
    return null;
  }
  return prefix.length > config.maxPrefixLength
    ? prefix.slice(0, config.maxPrefixLength).trim()
    : prefix;
}

async function setThreadName({ socketPath, threadId, name, timeoutMs }) {
  const socket = await connectWebSocket(socketPath, timeoutMs);
  try {
    await socket.request("initialize", {
      clientInfo: {
        name: "codex_utilities_hook",
        title: "Codex Utilities Hook",
        version: config.pluginVersion,
      },
      capabilities: {
        experimentalApi: false,
        optOutNotificationMethods: ["thread/name/updated"],
      },
    });
    socket.notify("initialized");
    await socket.request("thread/name/set", { threadId, name });
  } finally {
    socket.close();
  }
}

async function connectWebSocket(socketPath, timeoutMs) {
  if (!fs.existsSync(socketPath)) {
    throw new Error(`Codex App Server control socket was not found at ${socketPath}.`);
  }

  const rawSocket = net.createConnection(socketPath);
  rawSocket.setTimeout(timeoutMs);
  rawSocket.setNoDelay(true);

  await new Promise((resolve, reject) => {
    const onConnect = () => {
      cleanup();
      resolve();
    };
    const onError = (error) => {
      cleanup();
      reject(error);
    };
    const onTimeout = () => {
      cleanup();
      reject(new Error(`Timed out connecting to Codex App Server socket at ${socketPath}.`));
    };

    function cleanup() {
      rawSocket.off("connect", onConnect);
      rawSocket.off("error", onError);
      rawSocket.off("timeout", onTimeout);
    }

    rawSocket.once("connect", onConnect);
    rawSocket.once("error", onError);
    rawSocket.once("timeout", onTimeout);
  });

  await performWebSocketHandshake(rawSocket, timeoutMs);

  const client = new JsonRpcWebSocketClient(rawSocket, timeoutMs);
  rawSocket.on("data", (chunk) => client.receive(chunk));
  rawSocket.on("error", (error) => client.fail(error));
  rawSocket.on("close", () => client.closeFromServer());
  return client;
}

async function performWebSocketHandshake(rawSocket, timeoutMs) {
  const key = crypto.randomBytes(16).toString("base64");
  const expectedAccept = crypto
    .createHash("sha1")
    .update(`${key}258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)
    .digest("base64");
  const request = [
    "GET / HTTP/1.1",
    "Host: localhost",
    "Connection: Upgrade",
    "Upgrade: websocket",
    "Sec-WebSocket-Version: 13",
    `Sec-WebSocket-Key: ${key}`,
    "",
    "",
  ].join("\r\n");

  rawSocket.write(request);
  const response = await readHttpHeaders(rawSocket, timeoutMs);
  if (!/^HTTP\/1\.1 101\b/i.test(response)) {
    throw new Error("Codex App Server socket did not accept the WebSocket upgrade.");
  }
  const acceptHeader = response
    .split("\r\n")
    .find((line) => line.toLowerCase().startsWith("sec-websocket-accept:"));
  const actualAccept = acceptHeader?.split(":").slice(1).join(":").trim();
  if (actualAccept !== expectedAccept) {
    throw new Error("Codex App Server WebSocket upgrade returned an unexpected accept key.");
  }
}

async function readHttpHeaders(rawSocket, timeoutMs) {
  let buffer = Buffer.alloc(0);
  return await new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      cleanup();
      reject(new Error("Timed out waiting for Codex App Server WebSocket upgrade."));
    }, timeoutMs);

    const onData = (chunk) => {
      buffer = Buffer.concat([buffer, chunk]);
      const end = buffer.indexOf("\r\n\r\n");
      if (end === -1) {
        return;
      }
      cleanup();
      const extra = buffer.subarray(end + 4);
      if (extra.length > 0) {
        rawSocket.unshift(extra);
      }
      resolve(buffer.subarray(0, end + 4).toString("utf8"));
    };
    const onError = (error) => {
      cleanup();
      reject(error);
    };

    function cleanup() {
      clearTimeout(timer);
      rawSocket.off("data", onData);
      rawSocket.off("error", onError);
    }

    rawSocket.on("data", onData);
    rawSocket.once("error", onError);
  });
}

class JsonRpcWebSocketClient {
  constructor(rawSocket, timeoutMs) {
    this.nextId = 1;
    this.pending = new Map();
    this.rawSocket = rawSocket;
    this.timeoutMs = timeoutMs;
    this.readBuffer = Buffer.alloc(0);
  }

  request(method, params) {
    const id = this.nextId++;
    this.send({ id, method, params });
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Timed out waiting for ${method} response from Codex App Server.`));
      }, this.timeoutMs);
      this.pending.set(id, { method, resolve, reject, timer });
    });
  }

  notify(method, params) {
    const message = params === undefined ? { method } : { method, params };
    this.send(message);
  }

  send(message) {
    this.rawSocket.write(encodeTextFrame(JSON.stringify(message)));
  }

  receive(chunk) {
    try {
      this.readBuffer = Buffer.concat([this.readBuffer, chunk]);
      while (true) {
        const parsed = decodeFrame(this.readBuffer);
        if (!parsed) {
          return;
        }
        this.readBuffer = this.readBuffer.subarray(parsed.frameLength);
        if (parsed.opcode === 0x8) {
          this.closeFromServer();
          return;
        }
        if (parsed.opcode !== 0x1) {
          continue;
        }
        this.routeMessage(parsed.payload.toString("utf8"));
      }
    } catch (error) {
      this.fail(error);
      try {
        this.rawSocket.destroy();
      } catch {
        return;
      }
    }
  }

  routeMessage(text) {
    let message;
    try {
      message = JSON.parse(text);
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

  closeFromServer() {
    this.fail(new Error("Codex App Server closed the control socket connection."));
  }

  close() {
    try {
      this.rawSocket.end(encodeCloseFrame());
    } catch {
      this.rawSocket.destroy();
    }
  }
}

function encodeTextFrame(text) {
  const payload = Buffer.from(text, "utf8");
  return encodeClientFrame(0x1, payload);
}

function encodeCloseFrame() {
  return encodeClientFrame(0x8, Buffer.alloc(0));
}

function encodeClientFrame(opcode, payload) {
  const mask = crypto.randomBytes(4);
  const header = [];
  header.push(0x80 | opcode);

  if (payload.length < 126) {
    header.push(0x80 | payload.length);
  } else if (payload.length <= 0xffff) {
    header.push(0x80 | 126, (payload.length >> 8) & 0xff, payload.length & 0xff);
  } else {
    const lengthBuffer = Buffer.alloc(8);
    lengthBuffer.writeBigUInt64BE(BigInt(payload.length));
    header.push(0x80 | 127, ...lengthBuffer);
  }

  const masked = Buffer.alloc(payload.length);
  for (let index = 0; index < payload.length; index += 1) {
    masked[index] = payload[index] ^ mask[index % 4];
  }
  return Buffer.concat([Buffer.from(header), mask, masked]);
}

function decodeFrame(buffer) {
  if (buffer.length < 2) {
    return null;
  }

  const opcode = buffer[0] & 0x0f;
  const masked = (buffer[1] & 0x80) !== 0;
  let payloadLength = buffer[1] & 0x7f;
  let offset = 2;

  if (payloadLength === 126) {
    if (buffer.length < offset + 2) {
      return null;
    }
    payloadLength = buffer.readUInt16BE(offset);
    offset += 2;
  } else if (payloadLength === 127) {
    if (buffer.length < offset + 8) {
      return null;
    }
    const length = buffer.readBigUInt64BE(offset);
    if (length > BigInt(Number.MAX_SAFE_INTEGER)) {
      throw new Error("Codex App Server returned an oversized WebSocket frame.");
    }
    payloadLength = Number(length);
    offset += 8;
  }

  let mask;
  if (masked) {
    if (buffer.length < offset + 4) {
      return null;
    }
    mask = buffer.subarray(offset, offset + 4);
    offset += 4;
  }

  const frameLength = offset + payloadLength;
  if (buffer.length < frameLength) {
    return null;
  }

  const payload = Buffer.from(buffer.subarray(offset, frameLength));
  if (masked) {
    for (let index = 0; index < payload.length; index += 1) {
      payload[index] ^= mask[index % 4];
    }
  }
  return { frameLength, opcode, payload };
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

async function readStdin() {
  let buffer = "";
  process.stdin.setEncoding("utf8");

  for await (const chunk of process.stdin) {
    buffer += chunk;
  }

  return buffer;
}
