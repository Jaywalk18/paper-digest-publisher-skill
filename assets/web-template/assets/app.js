const state = {
  data: null,
  priority: "all",
  topic: "all",
  query: "",
};

const fallbackData = {
  title: "Research Digest",
  date: "YYYY-MM-DD",
  summary: "Curated papers for a user-defined research topic.",
  stats: { new: 0, updated: 0, filtered: 0, images: 0 },
  trends: ["Replace this with the digest's trend observations."],
  archiveNote: "Link generated catalog and previous issues here.",
  papers: [
    {
      priority: "P0",
      title: "Example high-priority paper",
      authors: "Author One, Author Two",
      topic: "Core Method",
      type: "arXiv",
      reason: "Shows how a card summarizes why the paper matters.",
      method: "Short method description.",
      limitation: "Known limitation or reason to read critically.",
      image: "assets/placeholder-figure.svg",
      imageAlt: "Placeholder figure",
      links: [{ label: "Paper", url: "#" }],
    },
  ],
};

const $ = (selector) => document.querySelector(selector);

async function loadData() {
  try {
    const response = await fetch("data/papers.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch {
    return fallbackData;
  }
}

function setText(selector, text) {
  const element = $(selector);
  if (element) element.textContent = text || "";
}

function uniqueValues(items, key) {
  return [...new Set(items.map((item) => item[key]).filter(Boolean))].sort();
}

function fillSelect(selector, values, allLabel) {
  const select = $(selector);
  select.innerHTML = `<option value="all">${allLabel}</option>`;
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  }
}

function renderHeader(data) {
  document.title = data.title || "Research Digest";
  setText("#digest-title", data.title);
  setText("#digest-summary", data.summary);
  setText("#issue-date", data.date ? `Issue ${data.date}` : "Latest issue");
  setText("#stat-new", String(data.stats?.new ?? 0));
  setText("#stat-updated", String(data.stats?.updated ?? 0));
  setText("#stat-filtered", String(data.stats?.filtered ?? 0));
  setText("#stat-images", String(data.stats?.images ?? 0));
  setText("#archive-note", data.archiveNote);

  const hero = data.papers?.[0];
  if (hero) {
    setText("#hero-priority", hero.priority);
    setText("#hero-title", hero.title);
    setText("#hero-reason", hero.reason);
    setText("#hero-caption", hero.caption || hero.method || "Extracted figure");
    $("#hero-image").src = hero.image || "assets/placeholder-figure.svg";
    $("#hero-image").alt = hero.imageAlt || hero.title;
    $("#hero-link").href = "#papers";
  }
}

function renderTrends(data) {
  const list = $("#trend-list");
  list.innerHTML = "";
  for (const trend of data.trends || []) {
    const item = document.createElement("li");
    item.textContent = trend;
    list.appendChild(item);
  }
}

function filteredPapers() {
  const query = state.query.trim().toLowerCase();
  return state.data.papers.filter((paper) => {
    const matchesPriority = state.priority === "all" || paper.priority === state.priority;
    const matchesTopic = state.topic === "all" || paper.topic === state.topic;
    const searchable = `${paper.title} ${paper.authors} ${paper.reason} ${paper.method}`.toLowerCase();
    return matchesPriority && matchesTopic && (!query || searchable.includes(query));
  });
}

function appendText(parent, tag, text, className) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.textContent = text || "";
  parent.appendChild(element);
  return element;
}

function paperCard(paper) {
  const article = document.createElement("article");
  article.className = "paper-card";

  const figure = document.createElement("figure");
  const image = document.createElement("img");
  image.src = paper.image || "assets/placeholder-figure.svg";
  image.alt = paper.imageAlt || paper.title || "Paper figure";
  figure.appendChild(image);
  article.appendChild(figure);

  const content = document.createElement("div");
  content.className = "paper-card-content";
  const meta = document.createElement("div");
  meta.className = "meta-row";
  appendText(meta, "span", paper.priority || "scan", "pill priority");
  appendText(meta, "span", paper.type || "paper", "pill");
  appendText(meta, "span", paper.topic || "topic", "pill");
  content.appendChild(meta);

  appendText(content, "h3", paper.title || "Untitled paper");
  const authors = document.createElement("p");
  const strong = document.createElement("strong");
  strong.textContent = paper.authors || "Authors unavailable";
  authors.appendChild(strong);
  content.appendChild(authors);
  appendText(content, "p", paper.reason);
  appendText(content, "p", paper.method);
  if (paper.limitation) appendText(content, "p", `Limitation: ${paper.limitation}`);

  const links = document.createElement("div");
  links.className = "links";
  for (const link of paper.links || []) {
    const anchor = document.createElement("a");
    anchor.href = link.url || "#";
    anchor.rel = "noreferrer";
    anchor.textContent = link.label || "Source";
    links.appendChild(anchor);
  }
  content.appendChild(links);
  article.appendChild(content);
  return article;
}

function renderPapers() {
  const grid = $("#papers");
  const papers = filteredPapers();
  grid.innerHTML = "";
  if (!papers.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No papers match the current filters.";
    grid.appendChild(empty);
    return;
  }
  papers.forEach((paper) => grid.appendChild(paperCard(paper)));
}

function bindFilters(data) {
  fillSelect("#priority-filter", uniqueValues(data.papers, "priority"), "All priorities");
  fillSelect("#topic-filter", uniqueValues(data.papers, "topic"), "All topics");

  $("#priority-filter").addEventListener("change", (event) => {
    state.priority = event.target.value;
    renderPapers();
  });
  $("#topic-filter").addEventListener("change", (event) => {
    state.topic = event.target.value;
    renderPapers();
  });
  $("#search-input").addEventListener("input", (event) => {
    state.query = event.target.value;
    renderPapers();
  });
}

loadData().then((data) => {
  state.data = { ...fallbackData, ...data, papers: data.papers || fallbackData.papers };
  renderHeader(state.data);
  renderTrends(state.data);
  bindFilters(state.data);
  renderPapers();
});
