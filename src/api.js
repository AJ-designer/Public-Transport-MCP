export const sendMessageToRouter = async (msg) => {
  await new Promise(r => setTimeout(r, 1000)); // Simulate delay
  return {
    text: "Here is the closest accessible station found via MCP:",
    stations: [{ name: "Central Station", distance: "0.2", elevatorStatus: "Working" }]
  };
};