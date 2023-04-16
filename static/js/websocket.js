let websocket;

function setupWebSocket() {
  websocket = new WebSocket("ws://localhost:8000/ws");

  websocket.addEventListener("open", (event) => {
    console.log("WebSocket connection opened:", event);
  });

  websocket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    const newMessage = document.createElement("div");
    newMessage.classList.add(
      "message",
      "d-flex",
      "flex-column",
      "align-items-start",
      "mb-3"
    );

    const newIcon = document.createElement("div");
    newIcon.classList.add("icon", "ms-3");
    newIcon.textContent = data.emoji;

    const newText = document.createElement("div");
    newText.classList.add("text", "ms-3");
    newText.textContent = data.ai_chat;

    const newDetailsButton = document.createElement("button");
    newDetailsButton.classList.add(
      "btn",
      "btn-link",
      "text-decoration-none",
      "text-start"
    );
    newDetailsButton.type = "button";
    newDetailsButton.textContent = "詳細を表示";
    newDetailsButton.setAttribute("data-bs-toggle", "collapse");
    const detailsId = "message-" + Math.floor(Math.random() * 10000); // Generate a random unique ID
    newDetailsButton.setAttribute("data-bs-target", "#" + detailsId);
    newDetailsButton.setAttribute("aria-expanded", "false");
    newDetailsButton.setAttribute("aria-controls", detailsId);

    const newCollapse = document.createElement("div");
    newCollapse.classList.add("collapse");
    newCollapse.id = detailsId;
    newCollapse.style.width = "100%";

    const newHR = document.createElement("hr");
    newHR.style.width = "100%";

    newCollapse.appendChild(newHR);

    if (data.human_chat) {
      const newDetails = document.createElement("div");
      newDetails.classList.add("details", "ms-3");
      const newStrong = document.createElement("strong");
      newStrong.textContent = "Human: ";
      const newHumanChat = document.createTextNode(data.human_chat);
      newDetails.appendChild(newStrong);
      newDetails.appendChild(newHumanChat);

      newCollapse.appendChild(newDetails);
    }

    newMessage.appendChild(newIcon);
    newMessage.appendChild(newText);
    newMessage.appendChild(newDetailsButton);
    newMessage.appendChild(newCollapse);

    const messagesContainer = document.querySelector(".messages");
    messagesContainer.insertBefore(newMessage, messagesContainer.firstChild);
  });

  websocket.addEventListener("close", (event) => {
    console.log("WebSocket connection closed:", event);
  });

  websocket.addEventListener("error", (event) => {
    console.error("WebSocket error:", event);
  });
}

function sendMessage(message) {
  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send(message);
  } else {
    console.error("WebSocket is not connected.");
  }
}

// ページが読み込まれたときにWebSocketの接続を確立
window.addEventListener("DOMContentLoaded", setupWebSocket);
