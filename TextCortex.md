# GoAccess — Berlin Transit Accessibility Intelligence Platform
## Built with Claude Code

## Why I built this

Berlin's public transport accessibility data exists but it's completely 
inaccessible to AI assistants. Wheelchair users, parents with strollers, 
anyone with mobility needs — they can't just ask an AI "is Alexanderplatz 
accessible right now?" and get a real answer. I wanted to fix that.

Nobody asked me to build it. I just thought it should exist.

It got selected as a standout project at the MCP Hackathon by ActionSpace 
AI and ProjectTogether.

## What I actually built

GoAccess is a three-layer full-stack application:

- React 19 frontend with a high-contrast, accessibility-first chat UI
- Express 5 router handling LLM orchestration
- MCP server exposing a typed `get_station_accessibility` tool via stdio transport

The LLM layer is provider-agnostic — Claude, Groq (Llama 3), Gemini, 
and HuggingFace all share the same response contract. Swapping providers 
is one line. The MCP server runs as a subprocess spawned by the router 
over stdio — no separate daemon, no network overhead.

## How I build with AI coding tools

The architecture, decisions, and code were built hands-on by the team. 
AI tooling made the process faster and cleaner — not a replacement for 
thinking, but an accelerant for it.

**The workflow that actually works:**
- Use Perplexity first for research — understanding the MCP protocol, 
  the SDK, existing patterns — then bring that context into Claude for 
  implementation decisions
- Treat every AI output like a junior developer's PR: read it, question 
  it, rewrite what isn't right before it touches the codebase
- When stuck, prompt Claude to act as a hostile client trying to break 
  whatever you just built — it surfaces failure modes faster than testing
- The real engineering judgment — architecture choices, what to build 
  next, what to throw away — that stays human

**What most people get wrong:**
They use AI to skip thinking. I use it to think faster. The moment you 
stop reading the output critically is the moment your codebase becomes 
unownable.

## The five questions

**Agency — last thing nobody asked me to do:**
Built an n8n workflow that scans business cards, extracts contact data 
into Airtable, uses an AI agent to compose and send a personalised email, 
then marks the contact as reached to prevent duplicates. Fully autonomous 
end-to-end. Built it because the manual process was inefficient and left 
too much room for human error.

**See Problems — how I act:**
I quantify first. At Global Goals for Berlin I didn't just notice the 
outreach process was slow — I measured it (2.5 hours/day), built the 
replacement, then measured again (zero hours/day). If you can't measure 
the problem you haven't understood it yet.

**First customer — how I test:**
I used GoAccess myself for a week before the hackathon. Every query I'd 
realistically ask, every edge case I could think of. The fallback logic 
in App.jsx — the getMockResponse function — exists because I tested what 
happened when the MCP server wasn't running and decided graceful 
degradation was better than a broken UI.

**Eye for good products — what inspires me:**
n8n. Not because of what it does but because of how it thinks about the 
user — giving technical people the speed of no-code without removing the 
power of code. I've built production workflows with it. That's the most 
honest endorsement I can give any product.

## What makes me different
I'm a final-year Software Engineering student who builds AI-native systems 
in production — not in tutorials. I think about AI tools as infrastructure, 
not features. And I've been using TextCortex's category of product long 
enough to have opinions about what it gets right and what it doesn't.
