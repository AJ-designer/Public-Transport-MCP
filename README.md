# GoAccess — Berlin Transit Accessibility Intelligence Platform

> Making Berlin's public transit navigable for everyone — powered by a multi-model AI pipeline built on open standards.

GoAccess is a conversational accessibility assistant for Berlin's public transit network. Wheelchair users, parents with strollers, and travelers with mobility needs can instantly query elevator status, step-free routes, and platform accessibility across BVG stations through a natural language chat interface — no forms, no maps to parse, no PDFs to dig through.

---

## Demo

| Ask a question | Get structured accessibility data |
|---|---|
| "Is Alexanderplatz accessible?" | Elevator status + live notes per station |
| "Can I use Zoo with a wheelchair?" | Full platform accessibility breakdown |
| "What's the situation at Hauptbahnhof?" | Operational status + level-by-level notes |

---

## Architecture

GoAccess is a three-layer full-stack application:

```
┌─────────────────────────────────────────┐
│           React Frontend (Vite)         │
│    Chat UI  →  src/App.jsx              │
│    Station Cards  →  src/StationCard.jsx│
└──────────────────┬──────────────────────┘
                   │ POST /api/chat
                   ▼
┌─────────────────────────────────────────┐
│         Express Router (port 3001)      │
│    router.js  — LLM orchestration       │
│    server.js  — HuggingFace backend     │
└──────────────────┬──────────────────────┘
                   │ stdio (MCP protocol)
                   ▼
┌─────────────────────────────────────────┐
│         MCP Server (mcp-server.js)      │
│    Tool: get_station_accessibility      │
│    Transport: StdioServerTransport      │
└─────────────────────────────────────────┘
```

**Data flow:**
1. User types a question in the React chat interface
2. Frontend sends `POST /api/chat` to the Express router
3. Router calls the MCP server's `get_station_accessibility` tool via stdio transport
4. MCP server returns structured station JSON
5. Router returns `{ text, stations[] }` to the frontend
6. Frontend renders the response and station accessibility cards

---

## The MCP Layer

The transit data is served through an **MCP (Model Context Protocol) server** — an open standard for connecting AI models to external tools and data sources.

Rather than hardcoding transit lookups into a prompt or calling a REST endpoint directly, GoAccess exposes a typed, schema-validated tool called `get_station_accessibility` through the MCP protocol. When an LLM needs station data, it calls this tool like a function — passing structured arguments and receiving structured results — then reasons about those results before composing a response.

```js
// Any MCP-compatible client can call this tool
await client.callTool({
  name: "get_station_accessibility",
  arguments: { stationName: "Ostbahnhof" }
});
// Returns: { name, elevator, accessible, notes }
```

**Why this matters:**
- Any MCP-compatible AI client can connect to the GoAccess tool server — it is not tied to this frontend
- The data layer is independently upgradeable: swap mock data for a live BVG API feed without touching the AI layer
- The protocol is open: Claude, GPT-4, local Ollama models, and any future MCP-compatible system can consume GoAccess tools

The MCP server runs as a subprocess spawned by the Express router over stdio (`StdioClientTransport`). No separate daemon, no network overhead between the router and tool server.

---

## AI Provider Pipeline

GoAccess is **provider-agnostic** — the intelligence layer can run on any major LLM without changing application logic.

| Provider | Role | File |
|---|---|---|
| **Anthropic Claude** | Multi-turn reasoning, tool use, ambiguity resolution | `router.js` |
| **Groq (Llama 3)** | High-speed single-turn lookups, sub-second inference | `router.js` |
| **Google Gemini** | Multimodal queries (photograph a station, ask if accessible) | `router.js` |
| **HuggingFace (Llama 3.2)** | Alternative inference backend | `server.js` |

All providers share the same response contract: `{ text: string, stations: array }`. Swapping providers requires changing one line.

---

## Tech Stack

**Frontend**
- React 19.2 — UI library
- Vite 7.2 — dev server and bundler (HMR enabled)
- Tailwind CSS — utility classes for styling
- Lucide React — icon library

**Backend**
- Express 5.2 — Node.js web framework
- CORS — cross-origin request handling
- `@modelcontextprotocol/sdk` 1.25 — official MCP SDK

**AI/LLM SDKs**
- `@google/generative-ai` — Google Gemini
- `groq-sdk` — Groq
- `openai` — OpenAI-compatible endpoints

**Dev Tools**
- ESLint 9 (flat config) with React hooks/refresh plugins
- dotenv — environment variable management

---

## Currently Supported Stations

| Station | Elevator | Accessible | Notes |
|---|---|---|---|
| Berlin Hauptbahnhof | Operational | Yes | Clear access to all levels |
| Alexanderplatz | Limited | No | U8 elevator out until 4 PM; use U5 entrance |
| Friedrichstraße | Operational | Yes | Step-free S-Bahn/Regional transition |
| Zoologischer Garten | Operational | Yes | Large elevators for U2, U9, all S-Bahn lines |
| Ostbahnhof | Working | Yes | Main hall ramp open |

> Live BVG API integration is on the roadmap. Current data is mocked for demonstration.

---

## Project Structure

```
Public-Transport-MCP/
├── mcp-server.js          # MCP server — defines get_station_accessibility tool
├── router.js              # Express router — LLM orchestration + MCP client
├── server.js              # Alternative backend — HuggingFace Inference API
├── main.jsx               # React DOM entry point
├── index.html             # Vite HTML entry point
├── vite.config.js         # Vite config (React plugin)
├── eslint.config.js       # ESLint flat config
├── package.json           # Dependencies and scripts
└── src/
    ├── App.jsx            # Main chat interface component
    ├── StationCard.jsx    # Station accessibility card component
    ├── api.js             # HTTP client (sendMessageToRouter)
    ├── main.jsx           # React root renderer
    ├── App.css            # App-level styles
    └── index.css          # Global styles and resets
```

---

## Getting Started

### Prerequisites

- Node.js 18+
- npm 9+

### Installation

```bash
git clone https://github.com/AJ-designer/Public-Transport-MCP.git
cd Public-Transport-MCP
npm install
```

### Environment Variables

Create a `.env` file in the project root:

```env
# Required for HuggingFace backend (server.js)
HF_TOKEN=your_huggingface_token

# Optional — for other providers
GROQ_API_KEY=your_groq_key
GOOGLE_AI_KEY=your_google_ai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Running the App

**Terminal 1 — Frontend (Vite dev server):**
```bash
npm run dev
```
Opens at `http://localhost:5173`

**Terminal 2 — Backend (Express + MCP server):**
```bash
node router.js
```
API available at `http://localhost:3001`

The MCP server spawns automatically as a subprocess of the router — no separate startup needed.

---

## Available Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start Vite dev server with HMR |
| `npm run build` | Production build to `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint across the codebase |

---

## UI Design

The interface is intentionally bold and high-contrast — accessibility-first design for the tool's target users:

- **Large 24–48px font sizes** across chat messages
- **Thick 4–8px borders** with high-contrast blue/purple palette
- **25vh input area** with large touch target for the SEND button
- **Rounded 32px corners** throughout for a friendly, legible layout

---

## Roadmap

- [ ] Live BVG API integration (real-time elevator outage data)
- [ ] Multi-turn reasoning with Claude tool use
- [ ] Multimodal inputs via Gemini (photograph a station, ask if accessible)
- [ ] Additional cities beyond Berlin
- [ ] Keyboard navigation and screen reader support
- [ ] Station search autocomplete

---

## Contributing

The active branch is `frontend`. PRs are welcome — especially for:

- Live BVG/transit API integrations
- Additional city support
- Accessibility improvements to the UI itself
- New LLM provider integrations

```bash
git checkout -b feature/your-feature
# make your changes
git push origin feature/your-feature
# open a PR against frontend
```
