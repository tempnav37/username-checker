const form = document.querySelector("#checker-form");
const usernameInput = document.querySelector("#username-input");
const resultPanel = document.querySelector("#result");
const suggestionsPanel = document.querySelector("#suggestions");
const bucketGrid = document.querySelector("#bucket-grid");
let currentFilter = "all";
let highlightedBucket = null;
let tableSize = 151;

function makeElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Something went wrong.");
  return payload;
}

function showError(message) {
  resultPanel.replaceChildren();
  const card = makeElement("div", "result-card invalid");
  card.append(makeElement("span", "result-symbol", "!"));
  const copy = makeElement("div", "result-copy");
  copy.append(makeElement("strong", "result-title", "Check the username"));
  copy.append(makeElement("p", "", message));
  card.append(copy);
  resultPanel.append(card);
  suggestionsPanel.hidden = true;
  resetTrace();
}

function resetTrace() {
  document.querySelector("#trace-status").textContent = "READY";
  document.querySelector("#trace-normalized").textContent = "waiting for input";
  document.querySelector("#trace-hash").textContent = "—";
  document.querySelector("#trace-bucket").textContent = "—";
  document.querySelector("#trace-chain-content").textContent = "The selected bucket will appear here.";
  highlightedBucket = null;
}

function renderTrace(data) {
  document.querySelector("#trace-status").textContent = "TRACED";
  document.querySelector("#trace-normalized").textContent = data.username;
  document.querySelector("#trace-hash").textContent = data.hash_value.toLocaleString();
  document.querySelector("#trace-bucket").textContent = `${data.bucket_index} / ${tableSize - 1}`;
  const chain = document.querySelector("#trace-chain-content");
  chain.replaceChildren();
  if (data.bucket_contents.length) {
    data.bucket_contents.forEach((username) => chain.append(makeElement("span", "chain-token", username)));
  } else {
    chain.append(makeElement("span", "empty-chain", "Empty bucket"));
  }
  highlightedBucket = data.bucket_index;
}

function renderResult(data) {
  resultPanel.replaceChildren();
  const isAvailable = data.available;
  const card = makeElement("div", `result-card ${isAvailable ? "available" : "taken"}`);
  card.append(makeElement("span", "result-symbol", isAvailable ? "+" : "×"));
  const copy = makeElement("div", "result-copy");
  copy.append(makeElement("strong", "result-title", isAvailable ? "Username available" : "Already in the table"));
  copy.append(makeElement("p", "", isAvailable
    ? `@${data.username} can be registered.`
    : `@${data.username} is stored in bucket ${data.bucket_index}.`));
  card.append(copy);
  const action = makeElement("button", "result-action", isAvailable ? "Register" : "Delete");
  action.type = "button";
  action.addEventListener("click", () => isAvailable ? registerUsername(data.username) : deleteUsername(data.username));
  card.append(action);
  resultPanel.append(card);

  suggestionsPanel.replaceChildren();
  suggestionsPanel.hidden = isAvailable || data.suggestions.length === 0;
  if (!suggestionsPanel.hidden) {
    suggestionsPanel.append(makeElement("span", "suggestion-label", "AVAILABLE ALTERNATIVES"));
    const list = makeElement("div", "suggestion-list");
    data.suggestions.forEach((suggestion) => {
      const button = makeElement("button", "suggestion-chip", `@${suggestion} ↗`);
      button.type = "button";
      button.addEventListener("click", () => {
        usernameInput.value = suggestion;
        form.requestSubmit();
      });
      list.append(button);
    });
    suggestionsPanel.append(list);
  }
}

async function checkUsername(username) {
  try {
    const data = await api("/api/check", {
      method: "POST",
      body: JSON.stringify({ username }),
    });
    renderResult(data);
    renderTrace(data);
    await refreshTable();
  } catch (error) {
    showError(error.message);
  }
}

async function registerUsername(username) {
  try {
    const data = await api("/api/add", {
      method: "POST",
      body: JSON.stringify({ username }),
    });
    if (!data.added) return checkUsername(username);
    renderResult({ ...data, available: false, suggestions: [] });
    renderTrace(data);
    await refreshTable();
  } catch (error) {
    showError(error.message);
  }
}

async function deleteUsername(username) {
  try {
    const data = await api("/api/delete", {
      method: "DELETE",
      body: JSON.stringify({ username }),
    });
    if (data.deleted) {
      await checkUsername(username);
    } else {
      showError(data.message);
    }
  } catch (error) {
    showError(error.message);
  }
}

function renderStats(stats) {
  tableSize = stats.table_size;
  document.querySelector("#stat-total").textContent = stats.total_usernames;
  document.querySelector("#stat-size").textContent = stats.table_size;
  document.querySelector("#stat-collisions").textContent = stats.collisions;
  document.querySelector("#stat-load").textContent = stats.load_factor.toFixed(2);
  document.querySelector("#stat-occupied").textContent = stats.occupied_buckets;
}

function renderBuckets(buckets) {
  const visibleBuckets = currentFilter === "collisions"
    ? buckets.filter((bucket) => bucket.usernames.length > 1)
    : buckets;
  bucketGrid.replaceChildren();
  if (visibleBuckets.length === 0) {
    bucketGrid.append(makeElement("p", "empty-explorer", currentFilter === "collisions"
      ? "No collision chains yet. Add more usernames to the table."
      : "No occupied buckets. Load the sample dataset or register a username."));
  }
  visibleBuckets.forEach((bucket) => {
    const collision = bucket.usernames.length > 1;
    const card = makeElement("article", `bucket-card${collision ? " has-collision" : ""}${bucket.index === highlightedBucket ? " is-highlighted" : ""}`);
    const header = makeElement("div", "bucket-card-header");
    header.append(makeElement("span", "bucket-number", `BUCKET ${String(bucket.index).padStart(3, "0")}`));
    header.append(makeElement("span", collision ? "chain-count collision-count" : "chain-count", collision ? `${bucket.usernames.length} IN CHAIN` : "1 KEY"));
    card.append(header);
    const keys = makeElement("div", "bucket-keys");
    bucket.usernames.forEach((username) => keys.append(makeElement("span", "bucket-key", username)));
    card.append(keys);
    bucketGrid.append(card);
  });
  document.querySelector("#bucket-summary").textContent = `${visibleBuckets.length} ${currentFilter === "collisions" ? "collision chains" : "occupied buckets"} shown`;
}

async function refreshTable() {
  try {
    const [stats, bucketData] = await Promise.all([
      api("/api/stats"),
      api("/api/buckets"),
    ]);
    renderStats(stats);
    renderBuckets(bucketData.buckets);
  } catch (error) {
    document.querySelector("#bucket-summary").textContent = error.message;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  checkUsername(usernameInput.value);
});

document.querySelectorAll(".filter-button").forEach((button) => {
  button.addEventListener("click", () => {
    currentFilter = button.dataset.filter;
    document.querySelectorAll(".filter-button").forEach((item) => item.classList.toggle("active", item === button));
    refreshTable();
  });
});

document.querySelector("#sample-button").addEventListener("click", async () => {
  try {
    await api("/api/sample", { method: "POST" });
    await refreshTable();
  } catch (error) {
    showError(error.message);
  }
});

document.querySelector("#reset-button").addEventListener("click", async () => {
  try {
    await api("/api/reset", { method: "POST" });
    resetTrace();
    resultPanel.replaceChildren();
    resultPanel.append(makeElement("div", "result-placeholder", "Table cleared. Check or register a username to begin."));
    suggestionsPanel.hidden = true;
    await refreshTable();
  } catch (error) {
    showError(error.message);
  }
});

refreshTable();