// src/api.js
export const sendMessageToRouter = async (userMessage) => {
  try {
    const response = await fetch("http://localhost:3001/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage }),
    });

    return await response.json();
  } catch (error) {
    return { text: "Error: Is your server.js running?", stations: [] };
  }
};