# 🚀 Quick Start Guide - DB Accessibility MCP Server

## What You Have

A complete MCP server for Deutsche Bahn accessibility information that:
- ✅ **No API key needed!** Uses public DB APIs
- ♿ Checks station accessibility features
- 🔍 Searches stations across Germany
- 🛤️ Evaluates route accessibility

## Setup Steps

### 1. Install Dependencies

Open your terminal and navigate to the project folder, then run:

```bash
pip install fastmcp httpx
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Test the Server (Optional but Recommended)

Run the test script to make sure everything works:

```bash
python test_server.py
```

You should see output testing all 4 tools.

### 3. Connect to Claude Desktop

#### Find Your Config File:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Edit the Config:

Open the file and add (replace `/path/to/` with your actual path):

```json
{
  "mcpServers": {
    "db-accessibility": {
      "command": "python",
      "args": ["/path/to/db-accessibility-mcp/server.py"]
    }
  }
}
```

**Important**: Use the **full absolute path** to server.py!

#### Example (macOS/Linux):
```json
{
  "mcpServers": {
    "db-accessibility": {
      "command": "python",
      "args": ["/home/yourname/projects/db-accessibility-mcp/server.py"]
    }
  }
}
```

#### Example (Windows):
```json
{
  "mcpServers": {
    "db-accessibility": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\projects\\db-accessibility-mcp\\server.py"]
    }
  }
}
```

### 4. Restart Claude Desktop

Close and reopen Claude Desktop completely.

### 5. Test It!

In Claude Desktop, try asking:
- "Search for accessible stations in Berlin"
- "Is München Hauptbahnhof wheelchair accessible?"
- "Check accessibility from Frankfurt to Hamburg"

You should see Claude using the MCP tools! 🎉

## Troubleshooting

### "Module not found" Error
Make sure you installed fastmcp and httpx:
```bash
pip install fastmcp httpx
```

### Server Not Showing Up in Claude Desktop
- Double-check the full path to server.py is correct
- Make sure you restarted Claude Desktop completely
- Check the Claude Desktop logs for errors

### API Returning Errors
The StaDa API is public but might have rate limits. If you get errors:
- Wait a few seconds between requests
- For production use, consider registering for a free API key at https://developers.deutschebahn.com/

## About the DB API (No Key Needed!)

This MVP uses Deutsche Bahn's **StaDa v2 API** which is:
- ✅ **Free to use** without registration
- ✅ **No API key required** for basic station data
- ✅ **Publicly accessible** for everyone
- 📊 Updated regularly by Deutsche Bahn

### What Data Is Available?

Without an API key, you get:
- Station names and locations
- Accessibility features (step-free access, mobility services)
- Station facilities (parking, WiFi, lockers, etc.)
- Contact information for assistance services

### Want More Features?

If you want real-time timetables, journey planning, or disruption alerts, you can:

1. **Register** at https://developers.deutschebahn.com/
2. **Subscribe** to additional APIs (many have free tiers!)
3. **Get an API key** (usually instant)
4. **Add the key** to the server code

But for basic accessibility checking, **the current setup works perfectly without any key!**

## Example Use Cases

✅ **Trip Planning**: "I'm traveling from Berlin to München - are both stations accessible?"

✅ **Station Facilities**: "Does Frankfurt Hbf have mobility assistance available?"

✅ **Route Evaluation**: "Which stations between Hamburg and Köln are wheelchair accessible?"

✅ **Contact Info**: "How do I book assistance for my journey?"

## Next Steps

Some ideas to extend this MVP:
- Add real-time train departure/arrival data
- Include platform accessibility information
- Add elevator status monitoring
- Cache frequently accessed stations
- Add support for multiple languages

Enjoy your DB Accessibility MCP Server! 🚂♿
