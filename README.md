# Deutsche Bahn Accessibility MCP Server

An MCP (Model Context Protocol) server that provides accessibility information for German train stations using Deutsche Bahn's public APIs.

## Features

This server provides tools to:
- 🔍 Search for train stations across Germany
- ♿ Check accessibility features (step-free access, mobility services, etc.)
- 🚉 Get detailed station information including facilities
- 🛤️ Evaluate route accessibility between stations
- 📞 Get DB Mobility Service contact information

## No API Key Needed! 🎉

This MVP uses Deutsche Bahn's public StaDa (Station Data) API which **does not require authentication** for basic queries. Perfect for getting started quickly!

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

### Development Mode
```bash
python server.py
```

### Using with Claude Desktop

Add this to your Claude Desktop MCP settings file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "db-accessibility": {
      "command": "python",
      "args": ["/absolute/path/to/db-accessibility-mcp/server.py"]
    }
  }
}
```

## Available Tools

### 1. `search_stations`
Search for stations by name or city.

**Example**: "Search for stations in Berlin"

### 2. `get_station_details`
Get comprehensive accessibility information for a specific station.

**Example**: "Get details for Berlin Hauptbahnhof"

### 3. `check_accessibility_route`
Check if a route between two stations is accessible.

**Example**: "Is the route from München to Hamburg accessible?"

### 4. `get_mobility_service_info`
Get contact information for DB's free mobility assistance service.

## Example Queries

Once connected to Claude Desktop, you can ask:

- "Which stations in Hamburg have step-free access?"
- "Is Frankfurt Hauptbahnhof wheelchair accessible?"
- "Check if the route from Berlin to Cologne is accessible"
- "How can I book assistance for my train journey?"
- "What facilities are available at München Hauptbahnhof?"

## API Information

This server uses:
- **StaDa API v2** - Station Data (no authentication required)
- Base URL: `https://api.deutschebahn.com/stada/v2/`

### Want More Features?

If you need more advanced features like real-time timetables or journey planning, you can:

1. Register at: https://developers.deutschebahn.com/
2. Subscribe to additional APIs (many are free tier available)
3. Add your API key to the server code

For the MVP, the public endpoints provide plenty of useful accessibility data!

## Accessibility Features Tracked

- ♿ Step-free access (Stufenfreier Zugang)
- 🤝 Mobility service availability
- 🅿️ Parking facilities
- 🚲 Bicycle parking
- 🚌 Local public transport connections
- 🚻 Public facilities
- 🧳 Lockers
- 🚕 Taxi ranks
- 📶 WiFi availability
- 🎫 Travel center
- ☕ Travel necessities (shops, etc.)

## Data Freshness

Station data is maintained by Deutsche Bahn and updated regularly. Accessibility information is generally reliable, but for critical accessibility needs, it's recommended to:
1. Contact DB Mobility Service in advance (see `get_mobility_service_info` tool)
2. Book assistance at least one day before travel

## Contributing

This is an MVP! Some ideas for enhancement:
- Add real-time departure/arrival data
- Include platform information
- Add elevator status (requires additional API)
- Cache frequently accessed stations
- Add journey planning with accessibility filters

## License

MIT License - Feel free to modify and extend!

## Support

For DB Mobility Service:
- Phone: 030 65 21 28 88 (6:00-22:00 daily)
- International: +49 30 65 21 28 88
- Website: https://www.bahn.de/service/individuelle-reise/barrierefrei
