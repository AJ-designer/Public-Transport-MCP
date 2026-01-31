// router.js
import express from 'express';
import cors from 'cors';
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const app = express();
app.use(cors());
app.use(express.json());

// Connect to the MCP Server we just made
const transport = new StdioClientTransport({ command: "node", args: ["mcp-server.js"] });
const client = new Client({ name: "transit-client", version: "1.0.0" }, { capabilities: {} });
await client.connect(transport);

app.post('/api/chat', async (req, res) => {
  const userMessage = req.body.message;

  // 1. Send message to LLM (using Groq/OpenAI)
  // 2. If LLM asks for 'get_station_accessibility', call the MCP client:
  const result = await client.callTool({
    name: "get_station_accessibility",
    arguments: { stationName: "Ostbahnhof" } // LLM would extract this dynamically
  });

  // 3. Send final answer back to Frontend
  res.json({
    text: "According to the Berlin MCP server, Ostbahnhof is accessible.",
    stations: [JSON.parse(result.content[0].text)]
  });
});

app.listen(3001, () => console.log("System connected on port 3001"));