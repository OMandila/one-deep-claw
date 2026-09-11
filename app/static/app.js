const form = document.querySelector("#chat-form");
const message = document.querySelector("#message");
const messages = document.querySelector("#messages");
const sendButton = document.querySelector("#send-button");
const characterCount = document.querySelector("#character-count");

function appendBrief(question, content, isError = false) {
  const brief = document.createElement("article");
  brief.className = `brief${isError ? " error-brief" : ""}`;

  const questionLabel = document.createElement("p");
  questionLabel.className = "user-question";
  questionLabel.textContent = `Research question: ${question}`;

  const label = document.createElement("p");
  label.className = "brief-label";
  label.textContent = isError ? "SERVICE NOTICE" : "ONE DEEP CLAW / RESEARCH BRIEF";

  const answer = document.createElement("p");
  answer.className = "answer";
  answer.textContent = content;

  brief.append(questionLabel, label, answer);
  messages.replaceChildren(brief);
}

function setSending(isSending) {
  sendButton.disabled = isSending;
  sendButton.textContent = isSending ? "Generating..." : "Generate brief ->";
}

message.addEventListener("input", () => {
  characterCount.textContent = `${message.value.length} / 4000`;
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    message.value = button.dataset.prompt;
    message.dispatchEvent(new Event("input"));
    message.focus();
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = message.value.trim();
  if (!question) return;

  setSending(true);
  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: question }),
    });
    const data = await response.json();

    if (!response.ok) throw new Error(data.detail || "The research request could not be completed.");
    appendBrief(question, data.response);
    message.value = "";
    message.dispatchEvent(new Event("input"));
  } catch (error) {
    appendBrief(question, error.message || "The research request could not be completed.", true);
  } finally {
    setSending(false);
  }
});