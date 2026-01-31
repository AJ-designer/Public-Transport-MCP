"""
Deutsche Bahn Accessibility MCP Server - Mock Data Version
With built-in chatbot for accessibility advice
"""

from mcp.server.fastmcp import FastMCP
import logging
from typing import Optional
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP("DB Accessibility Server")

# Mock station database (realistic data)
MOCK_STATIONS = {
    "berlin": [
        {
            "name": "Berlin Hauptbahnhof",
            "eva_number": "8011160",
            "has_step_free_access": "yes",
            "has_mobility_service": "yes",
            "has_parking": True,
            "has_bicycle_parking": True,
            "has_wifi": True,
            "has_elevators": 8,
            "location": {"latitude": 52.525589, "longitude": 13.369548},
            "notes": "Fully accessible. All platforms have elevators."
        },
        {
            "name": "Berlin Alexanderplatz",
            "eva_number": "8010159",
            "has_step_free_access": "yes",
            "has_mobility_service": "no",
            "has_parking": False,
            "has_bicycle_parking": True,
            "has_wifi": True,
            "has_elevators": 4,
            "location": {"latitude": 52.521918, "longitude": 13.413215},
            "notes": "Accessible but crowded. Elevators can be slow during rush hour."
        },
        {
            "name": "Berlin Ostbahnhof",
            "eva_number": "8010255",
            "has_step_free_access": "partial",
            "has_mobility_service": "no",
            "has_parking": True,
            "has_bicycle_parking": True,
            "has_wifi": False,
            "has_elevators": 2,
            "location": {"latitude": 52.510972, "longitude": 13.434567},
            "notes": "Some platforms require stairs. Contact station staff for assistance."
        }
    ],
    "münchen": [
        {
            "name": "München Hauptbahnhof",
            "eva_number": "8000261",
            "has_step_free_access": "yes",
            "has_mobility_service": "yes",
            "has_parking": True,
            "has_bicycle_parking": True,
            "has_wifi": True,
            "has_elevators": 6,
            "location": {"latitude": 48.140232, "longitude": 11.558335},
            "notes": "Fully accessible. Modern facilities."
        },
        {
            "name": "München Ostbahnhof",
            "eva_number": "8004158",
            "has_step_free_access": "yes",
            "has_mobility_service": "no",
            "has_parking": True,
            "has_bicycle_parking": True,
            "has_wifi": True,
            "has_elevators": 4,
            "location": {"latitude": 48.127434, "longitude": 11.604246},
            "notes": "Accessible with elevators to all platforms."
        }
    ],
    "hamburg": [
        {
            "name": "Hamburg Hauptbahnhof",
            "eva_number": "8002549",
            "has_step_free_access": "yes",
            "has_mobility_service": "yes",
            "has_parking": True,
            "has_bicycle_parking": True,
            "has_wifi": True,
            "has_elevators": 5,
            "location": {"latitude": 53.552776, "longitude": 10.006683},
            "notes": "Fully accessible. Some platforms under renovation."
        }
    ],
    "frankfurt": [
        {
            "name": "Frankfurt (Main) Hauptbahnhof",
            "eva_number": "8000105",
            "has_step_free_access": "yes",
            "has_mobility_service": "yes",
            "has_parking": True,
            "has_bicycle_parking": True,
            "has_wifi": True,
            "has_elevators": 7,
            "location": {"latitude": 50.107149, "longitude": 8.663789},
            "notes": "Fully accessible major hub."
        }
    ],
    "köln": [
        {
            "name": "Köln Hauptbahnhof",
            "eva_number": "8000207",
            "has_step_free_access": "yes",
            "has_mobility_service": "yes",
            "has_parking": True,
            "has_bicycle_parking": True,
            "has_wifi": True,
            "has_elevators": 6,
            "location": {"latitude": 50.943073, "longitude": 6.958729},
            "notes": "Accessible. Located next to cathedral."
        }
    ]
}


@mcp.tool() 
async def search_stations(query: str, limit: int = 10) -> dict:
    """
    Search for train stations in Germany by name or location.
    
    Args:
        query: Station name or city to search for (e.g., "Berlin", "München")
        limit: Maximum number of results (default 10)
    
    Returns:
        List of matching stations with accessibility info
    """
    query_lower = query.lower()
    results = []
    
    # Search through mock database
    for city, stations in MOCK_STATIONS.items():
        if query_lower in city or any(query_lower in s["name"].lower() for s in stations):
            results.extend(stations)
    
    # Limit results
    results = results[:limit]
    
    return {
        "success": True,
        "count": len(results),
        "stations": results,
        "note": "Using curated accessibility database"
    }


@mcp.tool()
async def get_station_details(station_name: str) -> dict:
    """
    Get detailed accessibility information for a specific station.
    
    Args:
        station_name: Station name (e.g., "Berlin Hauptbahnhof", "München Hbf")
    
    Returns:
        Detailed station information including all accessibility features
    """
    station_lower = station_name.lower()
    
    # Remove common abbreviations
    station_lower = station_lower.replace("hbf", "hauptbahnhof")
    station_lower = station_lower.replace("hb", "hauptbahnhof")
    
    # Search for station
    for city, stations in MOCK_STATIONS.items():
        for station in stations:
            station_name_lower = station["name"].lower()
            
            # Match if query is in station name OR station name is in query OR city matches
            if (station_lower in station_name_lower or 
                station_name_lower in station_lower or
                city in station_lower):
                return {
                    "success": True,
                    "station": {
                        "name": station["name"],
                        "eva_number": station["eva_number"],
                        "step_free_access": station["has_step_free_access"],
                        "mobility_service": station["has_mobility_service"],
                        "elevators": station.get("has_elevators", "Unknown"),
                        "parking": station["has_parking"],
                        "bicycle_parking": station["has_bicycle_parking"],
                        "wifi": station["has_wifi"],
                        "location": station["location"],
                        "accessibility_notes": station.get("notes", "No additional notes"),
                        "recommendation": _get_accessibility_recommendation(station)
                    }
                }
    
    return {
        "success": False,
        "error": f"Station '{station_name}' not found in database"
    }


@mcp.tool()
async def check_accessibility_route(from_station: str, to_station: str) -> dict:
    """
    Check accessibility information for a route between two stations.
    
    Args:
        from_station: Departure station name (e.g., "Berlin Hbf")
        to_station: Arrival station name (e.g., "München Hbf")
    
    Returns:
        Accessibility information for both stations on the route
    """
    # Get details for both stations
    from_details = await get_station_details(from_station)
    to_details = await get_station_details(to_station)
    
    if not from_details["success"] or not to_details["success"]:
        return {
            "success": False,
            "error": "Could not find one or both stations",
            "tip": "Try searching for the station first to see available options"
        }
    
    # Analyze accessibility
    from_accessible = from_details["station"]["step_free_access"] == "yes"
    to_accessible = to_details["station"]["step_free_access"] == "yes"
    
    both_have_service = (
        from_details["station"]["mobility_service"] == "yes" and 
        to_details["station"]["mobility_service"] == "yes"
    )
    
    return {
        "success": True,
        "route_fully_accessible": from_accessible and to_accessible,
        "departure": {
            "name": from_details["station"]["name"],
            "step_free": from_accessible,
            "mobility_service": from_details["station"]["mobility_service"],
            "elevators": from_details["station"]["elevators"],
            "notes": from_details["station"]["accessibility_notes"]
        },
        "arrival": {
            "name": to_details["station"]["name"],
            "step_free": to_accessible,
            "mobility_service": to_details["station"]["mobility_service"],
            "elevators": to_details["station"]["elevators"],
            "notes": to_details["station"]["accessibility_notes"]
        },
        "recommendation": _get_route_recommendation(from_accessible, to_accessible, both_have_service)
    }


@mcp.tool()
async def get_mobility_service_info() -> dict:
    """
    Get information about DB's Mobility Service Center for travelers with disabilities.
    
    Returns:
        Contact information and service details for DB Mobility Service
    """
    return {
        "success": True,
        "service": "DB Mobility Service Center",
        "description": "Free assistance service for passengers with reduced mobility",
        "phone": {
            "national": "030 65 21 28 88",
            "international": "+49 30 65 21 28 88",
            "hours": "Daily 6:00 - 22:00"
        },
        "online": "https://www.bahn.de/service/individuelle-reise/barrierefrei",
        "booking": "Book assistance at least one day in advance (ideally earlier)",
        "services": [
            "Help with boarding and alighting trains",
            "Assistance with luggage",
            "Guidance through stations",
            "Reserved seating arrangements",
            "Information about accessible routes",
            "Wheelchair provision if needed"
        ],
        "free_of_charge": True,
        "tip": "Always mention your specific needs when booking"
    }


@mcp.tool()
async def accessibility_chatbot(user_question: str) -> dict:
    """
    AI chatbot for answering accessibility questions about German train travel.
    
    Args:
        user_question: User's question about accessibility
    
    Returns:
        Helpful advice and recommendations
    """
    question_lower = user_question.lower()
    
    if "wheelchair" in question_lower:
        return {
            "success": True,
            "answer": """For wheelchair users traveling with Deutsche Bahn:

✅ **Before Your Trip:**
- Book DB Mobility Service 1-2 days in advance (030 65 21 28 88)
- Request a wheelchair-accessible seat when booking
- Specify if you need boarding assistance

✅ **At The Station:**
- Major stations (Hauptbahnhof) have elevators to all platforms
- Look for the wheelchair symbol on station maps
- Staff can provide ramps for boarding

✅ **On The Train:**
- ICE and IC trains have dedicated wheelchair spaces
- Accessible toilets available
- Priority seating in designated areas

💡 **Pro Tip:** Arrive 20 minutes early to allow time for assistance setup."""
        }
    
    elif "elevator" in question_lower or "lift" in question_lower:
        return {
            "success": True,
            "answer": """Elevator Information:

🏢 **Major Stations:**
- Berlin Hbf: 8 elevators
- München Hbf: 6 elevators
- Hamburg Hbf: 5 elevators
- Frankfurt Hbf: 7 elevators

⚠️ **What If Elevator Breaks?**
1. Contact station staff immediately
2. They can arrange alternative routes
3. Call DB Mobility Service: 030 65 21 28 88
4. Platform lifts may be available as backup"""
        }
    
    else:
        return {
            "success": True,
            "answer": f"""I can help with accessibility questions!

🔍 **Ask me about:**
- Wheelchair accessibility
- Elevator locations
- Visual/hearing impairments
- Booking assistance
- Luggage help
- Costs and discounts

Your question was: "{user_question}"

Try asking something more specific!"""
        }


# Helper functions
def _get_accessibility_recommendation(station: dict) -> str:
    """Generate recommendation based on station accessibility"""
    if station["has_step_free_access"] == "yes" and station["has_mobility_service"] == "yes":
        return "✅ Fully accessible station. Recommended for all mobility needs."
    elif station["has_step_free_access"] == "yes":
        return "✅ Step-free access available. Contact DB Mobility Service for assistance: 030 65 21 28 88"
    else:
        return "⚠️ Partial accessibility. Advance booking with DB Mobility Service strongly recommended."


def _get_route_recommendation(from_accessible: bool, to_accessible: bool, both_have_service: bool) -> str:
    """Generate route recommendation"""
    if from_accessible and to_accessible:
        if both_have_service:
            return "✅ Excellent! Both stations are fully accessible with mobility service available."
        else:
            return "✅ Both stations are step-free accessible. Consider booking DB Mobility Service for smoother boarding."
    else:
        return "⚠️ One or both stations have accessibility challenges. Book DB Mobility Service in advance: 030 65 21 28 88"


if __name__ == "__main__":
    mcp.run()