const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const submitButton = document.querySelector("#submit-button");
const charCount = document.querySelector("#char-count");
const statusLine = document.querySelector("#status");
const answerPanel = document.querySelector("#answer-panel");

questionInput.addEventListener("input", () => {
  charCount.textContent = `${questionInput.value.length} / 1000`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;

  submitButton.disabled = true;
  statusLine.className = "status";
  statusLine.textContent = "Searching the policy corpus and preparing an answer…";
  answerPanel.hidden = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The request could not be completed.");

    document.querySelector("#answer").textContent = data.answer;
    const citationList = document.querySelector("#citations");
    citationList.replaceChildren();
    for (const citation of data.citations || []) {
      const item = document.createElement("li");
      item.textContent = `${citation.policy_id} — ${citation.title} — ${citation.section} (${citation.chunk_id})`;
      citationList.append(item);
    }
    document.querySelector("#citations-wrap").hidden = !(data.citations || []).length;

    const snippets = document.querySelector("#snippets");
    snippets.replaceChildren();
    for (const snippet of data.snippets || []) {
      const card = document.createElement("article");
      card.className = "snippet";
      const meta = document.createElement("div");
      meta.className = "snippet-meta";
      meta.textContent = `${snippet.policy_id} — ${snippet.title} — ${snippet.section} — ${snippet.chunk_id}`;
      const text = document.createElement("p");
      text.textContent = snippet.text;
      card.append(meta, text);
      snippets.append(card);
    }
    document.querySelector("#snippets-wrap").hidden = !(data.snippets || []).length;
    answerPanel.hidden = false;
    statusLine.textContent = "Answer ready.";
  } catch (error) {
    statusLine.className = "status error";
    statusLine.textContent = error.message;
  } finally {
    submitButton.disabled = false;
  }
});
