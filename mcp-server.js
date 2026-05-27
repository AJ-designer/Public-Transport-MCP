import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "berlin-transit", version: "1.0.0" }, { capabilities: { tools: {} } });

const STATIONS = [
  { name: "Berlin Hauptbahnhof", elevatorStatus: "Operational", accessible: true,  notes: "Clear access to all levels" },
  { name: "Alexanderplatz",      elevatorStatus: "Limited",     accessible: false, notes: "U8 elevator out until 4 PM — use U5 entrance for lift" },
  { name: "Friedrichstraße",     elevatorStatus: "Operational", accessible: true,  notes: "Step-free S-Bahn and Regional transition available" },
  { name: "Zoologischer Garten", elevatorStatus: "Operational", accessible: true,  notes: "Large elevators for U2, U9, and all S-Bahn lines" },
  { name: "Ostbahnhof",          elevatorStatus: "Operational", accessible: true,  notes: "Main hall ramp open" },
];

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_station_accessibility",
    description: "Check if a Berlin BVG station is wheelchair accessible and get elevator status",
    inputSchema: {
      type: "object",
      properties: { stationName: { type: "string", description: "Name or partial name of the Berlin station" } },
      required: ["stationName"]
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { stationName } = request.params.arguments;
  const station = STATIONS.find(s => s.name.toLowerCase().includes(stationName.toLowerCase()));
  return {
    content: [{ type: "text", text: JSON.stringify(station ?? { error: "Station not found" }) }]
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
