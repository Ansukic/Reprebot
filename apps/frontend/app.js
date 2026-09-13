"use strict";

const $ = (sel) => document.querySelector(sel);

const chatLog = $("#chat-log");
const chatForm = $("#chat-form");
const chatInput = $("#chat-question");
const chatSend = $("#chat-send");
const docList = $("#doc-list");
const dropzone = $("#dropzone");
const fileInput = $("#file-input");
const uploadStatus = $("#upload-status");
const healthDot = $("#health-dot");
const healthText = $("#health-text");

let busy = false;
let docCount = 0;

/* ---------- util ---------- */

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
}

function now() {
  return new Date().toLocaleTimeString("es-CO", { hour: "2-digit", minute: "2-digit" });
}

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (res.status === 204) return null;
  let body = null;
  try {
    body = await res.json();
  } catch (_) {
    body = null;
  }
  if (!res.ok) {
    const detail = body && body.detail ? body.detail : `error ${res.status}`;
    throw new Error(detail);
  }
  return body;
}

/* ---------- tabs ---------- */

function switchTab(name) {
  document.querySelectorAll(".tab").forEach((t) => {
    const active = t.id === `tab-${name}`;
    t.classList.toggle("active", active);
    t.setAttribute("aria-selected", active);
  });
  document.querySelectorAll(".view").forEach((v) => {
    v.classList.toggle("active", v.id === `view-${name}`);
  });
}

$("#tab-chat").addEventListener("click", () => switchTab("chat"));
$("#tab-docs").addEventListener("click", () => switchTab("docs"));

/* ---------- chat ---------- */

function addMsg(role, text) {
  const msg = el("div", `msg ${role}`);
  const meta = el("div", "meta", role === "user" ? "tú" : "reprebot");
  meta.textContent = `${role === "user" ? "tú" : "reprebot"} · ${now()}`;
  msg.append(meta, el("div", "body", text));
  chatLog.append(msg);
  chatLog.scrollTop = chatLog.scrollHeight;
  return msg;
}

function addTyping() {
  const msg = el("div", "msg bot");
  const typing = el("div", "typing");
  typing.append(el("span"), el("span"), el("span"));
  msg.append(typing);
  chatLog.append(msg);
  chatLog.scrollTop = chatLog.scrollHeight;
  return msg;
}

function renderSources(msg, sources) {
  if (!sources || sources.length === 0) return;
  const wrap = el("details", "sources");
  wrap.append(el("summary", null, `fuentes (${sources.length})`));
  for (const s of sources) {
    const chip = el("div", "source-chip");
    chip.append(el("span", "src-name", s.doc_name));
    chip.append(el("div", "src-text", s.text));
    chip.append(el("div", "src-score", `relevancia ${s.score.toFixed(3)}`));
    wrap.append(chip);
  }
  msg.append(wrap);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendQuestion(question) {
  busy = true;
  chatSend.disabled = true;
  chatInput.disabled = true;

  addMsg("user", question);
  const typing = addTyping();

  try {
    const data = await api("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    typing.remove();
    const answer = addMsg("bot", data.answer);
    renderSources(answer, data.sources);
  } catch (err) {
    typing.remove();
    addMsg("error", err.message);
  } finally {
    busy = false;
    chatSend.disabled = false;
    chatInput.disabled = false;
    chatInput.focus();
  }
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = chatInput.value.trim();
  if (!question || busy) return;
  chatInput.value = "";
  sendQuestion(question);
});

/* ---------- documentos ---------- */

function renderDocs(docs) {
  docCount = docs.length;
  docList.replaceChildren();
  if (docs.length === 0) {
    docList.append(el("div", "doc-empty", "no hay conocimiento cargado — el bot no sabe nada todavía"));
    return;
  }
  for (const d of docs) {
    const item = el("div", "doc-item");
    item.append(el("div", "doc-name", d.name));
    const date = new Date(d.added_at).toLocaleString("es-CO", { dateStyle: "short", timeStyle: "short" });
    item.append(el("div", "doc-meta", `${d.chunks} chunks · ${date}`));
    const del = el("button", "doc-del", "borrar");
    del.addEventListener("click", async () => {
      if (!confirm(`¿borrar "${d.name}"?`)) return;
      del.disabled = true;
      try {
        await api(`/api/documents/${d.id}`, { method: "DELETE" });
        loadDocs();
      } catch (err) {
        del.disabled = false;
        showUploadStatus(err.message, "err");
      }
    });
    item.append(del);
    docList.append(item);
  }
}

async function loadDocs() {
  try {
    const data = await api("/api/documents");
    renderDocs(data.documents);
  } catch (err) {
    docList.replaceChildren(el("div", "doc-empty", err.message));
  }
}

function showUploadStatus(text, cls) {
  uploadStatus.hidden = false;
  uploadStatus.className = `drop-status ${cls || ""}`;
  uploadStatus.textContent = text;
}

async function uploadFile(file) {
  showUploadStatus(`ingiriendo "${file.name}"… (la primera vez descarga el modelo de embeddings, puede tardar un par de minutos)`, "");
  try {
    const fd = new FormData();
    fd.append("file", file);
    const data = await api("/api/documents", { method: "POST", body: fd });
    showUploadStatus(`ok: ${data.name} → ${data.chunks} chunks`, "ok");
    loadDocs();
  } catch (err) {
    showUploadStatus(err.message, "err");
  }
}

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) uploadFile(fileInput.files[0]);
  fileInput.value = "";
});

["dragover", "dragenter"].forEach((ev) =>
  dropzone.addEventListener(ev, (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  })
);
["dragleave", "drop"].forEach((ev) =>
  dropzone.addEventListener(ev, (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  })
);
dropzone.addEventListener("drop", (e) => {
  if (e.dataTransfer.files.length > 0) uploadFile(e.dataTransfer.files[0]);
});

/* ---------- health ---------- */

async function checkHealth() {
  try {
    const h = await api("/api/health");
    healthDot.className = "health-dot up";
    healthText.textContent = `${h.documents} docs · ${h.chunks} chunks`;
    docCount = h.documents;
  } catch (_) {
    healthDot.className = "health-dot down";
    healthText.textContent = "sin conexión";
  }
}

/* ---------- init ---------- */

async function init() {
  checkHealth();
  setInterval(checkHealth, 30000);
  loadDocs();
  try {
    const h = await api("/api/health");
    if (h.documents === 0) {
      addMsg("bot", "hola. soy reprebot. todavía no tengo documentos cargados — ve a la pestaña documentos y súbele las leyes y reglamentos de la unal.");
    }
  } catch (_) {
    addMsg("error", "no pude conectar con el backend. ¿está corriendo el servidor?");
  }
}

init();
