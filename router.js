import express from 'express';
import cors from 'cors';
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const app = express();
app.use(cors());
app.use(express.json());

const transport = new StdioClientTransport({ command: "node", args: ["mcp-server.js"] });
const client = new Client({ name: "transit-client", version: "1.0.0" }, { capabilities: {} });
await client.connect(transport);

function extractStation(message) {
  const q = message.toLowerCase();
  if (q.includes("hauptbahnhof"))                          return "Berlin Hauptbahnhof";
  if (q.includes("alexanderplatz"))                        return "Alexanderplatz";
  if (q.includes("friedrichstrasse") || q.includes("friedrichstraße")) return "Friedrichstraße";
  if (q.includes("zoo") || q.includes("zoologischer"))    return "Zoologischer Garten";
  if (q.includes("ostbahnhof"))                           return "Ostbahnhof";
  return null;
}

app.post('/api/chat', async (req, res) => {
  const userMessage = req.body.message;
  const stationName = extractStation(userMessage);

  if (!stationName) {
    return res.json({
      text: "I'm not sure which station you mean. Try asking about Hauptbahnhof, Alexanderplatz, Friedrichstraße, Zoologischer Garten, or Ostbahnhof.",
      stations: []
    });
  }

  try {
    const result = await client.callTool({
      name: "get_station_accessibility",
      arguments: { stationName }
    });

    const station = JSON.parse(result.content[0].text);

    if (station.error) {
      return res.json({ text: `Couldn't find data for ${stationName}.`, stations: [] });
    }

    const statusLine = station.accessible
      ? `${station.name} is fully accessible. ${station.notes}.`
      : `${station.name} has limited accessibility — ${station.notes}.`;

    res.json({ text: statusLine, stations: [station] });
  } catch (err) {
    console.error("MCP error:", err);
    res.status(500).json({ text: "Internal error querying station data.", stations: [] });
  }
});

app.listen(3001, () => console.log("GoAccess MCP router running on port 3001"));
