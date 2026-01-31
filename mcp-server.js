// mcp-server.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "berlin-transit", version: "1.0.0" }, { capabilities: { tools: {} } });

// MOCK DATA
const STATIONS = [
  { name: "Ostbahnhof", elevator: "Working", accessible: true, notes: "Main hall ramp open" },
  { name: "Alexanderplatz", elevator: "Under Repair", accessible: false, notes: "Use U5 entrance for lift" }
];

// 1. Tell the LLM what tools are available
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_station_accessibility",
    description: "Check if a Berlin station is wheelchair accessible",
    inputSchema: {
      type: "object",
      properties: { stationName: { type: "string" } },
      required: ["stationName"]
    }
  }]
}));

// 2. Handle the logic when the LLM calls the tool
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { stationName } = request.params.arguments;
  const station = STATIONS.find(s => s.name.toLowerCase().includes(stationName.toLowerCase()));
  
  return {
    content: [{ type: "text", text: JSON.stringify(station || { error: "Station not found" }) }]
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);