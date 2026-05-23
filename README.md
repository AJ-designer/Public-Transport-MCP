# GoAccess — Berlin Transit Accessibility Intelligence Platform

> **Making Berlin's public transit navigable for everyone — powered by a multi-model AI pipeline built on open standards.**

GoAccess is an open-source conversational accessibility assistant for Berlin's public transit network. It lets any user — wheelchair users, parents with strollers, travelers with mobility needs — instantly query real-time elevator status, step-free routes, and platform accessibility across the entire BVG network through a natural language interface. No forms. No maps to parse. Just ask.

The frontend branch is the active, production-ready branch of this repository.

---

## The Problem

Berlin's transit accessibility data exists — but it's buried. The BVG publishes elevator outage notices, but finding the relevant info for *your* station, *your* line, *your* platform requires navigating fragmented websites, PDFs, and apps that were never designed for people who need that information most. GoAccess collapses that friction into a single conversation.

---

## How It Works: A Multi-Model AI Pipeline

GoAccess is not a wrapper around a single API. It is a **provider-agnostic AI pipeline** — meaning the intelligence layer can run on any major LLM provider without changing application logic. This is the core architectural decision that makes the project genuinely extensible and future-proof.

Under the hood, three separate AI providers are integrated in parallel:

**Anthropic Claude** sits at the center of the reasoning layer. Claude is responsible for understanding the user's natural language query, deciding which tool to invoke, interpreting the structured result returned by the MCP server, and composing a human-readable response. Claude's tool-use capability — its ability to call external functions mid-conversation and reason about the results — is what makes the whole pipeline coherent rather than just a string of API calls stitched together. The model doesn't just retrieve data; it understands context, handles ambiguity ("the one near Alexanderplatz"), and produces responses that are genuinely useful rather than raw JSON.

**Groq** (running Llama 3) provides a high-speed inference alternative for latency-sensitive queries. Where Claude handles nuanced multi-turn reasoning, Groq handles fast, single-turn lookups with sub-second response times. Both are live in the codebase under the same interface contract — swapping between them requires changing one line.

**Google Gemini** is integrated as a third provider, enabling multimodal inputs in future iterations — for example, letting a user photograph a station entrance and ask whether it's accessible.

All three providers are abstracted behind a shared Express router (`router.js`), meaning the frontend never knows or cares which model is responding. This is intentional: the goal is resilience. If one provider's API goes down or raises prices, the system keeps running.

---

## The MCP Layer: Why This Matters

The transit data itself is served through an **MCP (Model Context Protocol) server** — an open standard for connecting AI models to external tools and data sources. This is the architectural detail that separates GoAccess from a toy project.

Rather than hardcoding transit lookups into the LLM prompt or calling a REST endpoint directly, GoAccess exposes a typed, schema-validated tool called `get_station_accessibility` through the MCP protocol. When Claude (or any connected model) needs station data, it *calls this tool the same way a function call works in code* — passing structured arguments, receiving structured results, and reasoning about those results before responding.

This means:

- **Any MCP-compatible AI client** can connect to the GoAccess tool server and gain transit awareness. The server is not tied to this frontend.
- **The data layer is independently upgradeable.** Swap mock data for a live BVG API feed, a database, or a third-party accessibility service — the AI layer doesn't need to change.
- **The protocol is open.** MCP is not a proprietary integration. Any model or agent that speaks MCP — Claude, GPT-4, local Ollama models, future systems we haven't seen yet — can consume GoAccess's tools.

The MCP server runs as a subprocess spawned by the Express router, communicating over stdio via `StdioClientTransport`. This keeps it lightweight and portable — no separate daemon to manage, no network overhead between the router and the tool server.

---

## Why It's Open Source (and What That Actually Means Here)

GoAccess is open source not as a legal formality but as a structural commitment. Every layer of the stack is built on open standards and permissively licensed dependencies:

- **MCP** is an open protocol. The tool definitions in this repo can be consumed by any conforming client.
- **The AI provider abstraction** means no vendor lock-in. The project does not depend on any single company's continued goodwill or pricing.
- **The frontend** is plain React with no proprietary component libraries.
- **The data model** is schema-first (zod-validated) and fully documented — anyone can extend the station database or replace it with a live data feed.

Anyone can fork this, point it at a different city's transit API, swap in a different LLM, and have a working accessibility assistant in hours. That is the point.

---

## Getting Started

```bash
npm install
```

Run the Vite frontend:

```bash
npm run dev
```

Run the Express + MCP backend (port 3001):

```bash
node router.js
```

The MCP server is spawned automatically as a subprocess — no separate startup needed.

---

## Currently Supported Stations

| Station | Elevator Status | Notes |
|---|---|---|
| Berlin Hauptbahnhof |  Operational | Clear access to all levels |
| Alexanderplatz |  Limited | U8 elevator out until 4 PM |
| Friedrichstraße |  Operational | Step-free S-Bahn/Regional transition |
| Zoologischer Garten |  Operational | Large elevators, all lines |

Live BVG data integration is on the roadmap.

---

## Available Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start Vite dev server with HMR |
| `npm run build` | Production build |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

---

## Contributing

The active branch is `frontend`. PRs welcome — especially for live data integrations, additional cities, and accessibility improvements to the UI itself.

---

*Built for the people Berlin's transit system was not designed with in mind.*
