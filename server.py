"""
Deutsche Bahn Accessibility MCP Server
Provides tools to check accessibility features for German train stations and connections
"""

from mcp.server.fastmcp import FastMCP
import httpx
from typing import Optional

# Initialize FastMCP server
mcp = FastMCP("DB Accessibility Server")

# DB API Base URLs (no auth required for these endpoints!)
STATION_API = "https://apis.deutschebahn.com/db-api-marketplace/apis/station-data/v2"
TIMETABLE_API = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"

@mcp.tool()
async def search_stations(query: str, limit: int = 10) -> dict:
    """
    Search for train stations in Germany by name or location.
    
    Args:
        query: Station name or city to search for
        limit: Maximum number of results (default 10)
    
    Returns:
        List of matching stations with accessibility info
    """
    try:
        async with httpx.AsyncClient() as client:
            # Using the StaDa Station API (free, no auth)
            url = f"https://api.deutschebahn.com/stada/v2/stations"
            params = {
                "searchstring": query,
                "limit": limit
            }
            
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # Extract accessibility information
            stations = []
            for station in data.get("result", []):
                accessibility_info = {
                    "name": station.get("name"),
                    "eva_number": station.get("evaNumbers", [{}])[0].get("number"),
                    "has_parking": station.get("hasParking", False),
                    "has_bicycle_parking": station.get("hasBicycleParking", False),
                    "has_local_public_transport": station.get("hasLocalPublicTransport", False),
                    "has_public_facilities": station.get("hasPublicFacilities", False),
                    "has_lockers": station.get("hasLockers", False),
                    "has_taxi_rank": station.get("hasTaxiRank", False),
                    "has_travel_necessities": station.get("hasTravelNecessities", False),
                    "has_step_free_access": station.get("hasSteplessAccess"),
                    "has_mobility_service": station.get("hasMobilityService"),
                    "location": {
                        "latitude": station.get("evaNumbers", [{}])[0].get("geographicCoordinates", {}).get("coordinates", [None, None])[1],
                        "longitude": station.get("evaNumbers", [{}])[0].get("geographicCoordinates", {}).get("coordinates", [None, None])[0]
                    }
                }
                stations.append(accessibility_info)
            
            return {
                "success": True,
                "count": len(stations),
                "stations": stations
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to fetch station data. Using StaDa API which is free."
        }


@mcp.tool()
async def get_station_details(station_id: str) -> dict:
    """
    Get detailed accessibility information for a specific station.
    
    Args:
        station_id: Station number (EVA number) or station name
    
    Returns:
        Detailed station information including all accessibility features
    """
    try:
        async with httpx.AsyncClient() as client:
            # First search for the station if name is provided
            if not station_id.isdigit():
                search_result = await search_stations(station_id, limit=1)
                if not search_result["success"] or not search_result["stations"]:
                    return {"success": False, "error": "Station not found"}
                station_id = search_result["stations"][0]["eva_number"]
            
            # Get station details
            url = f"https://api.deutschebahn.com/stada/v2/stations/{station_id}"
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            station = response.json()
            
            return {
                "success": True,
                "station": {
                    "name": station.get("name"),
                    "category": station.get("category"),
                    "has_step_free_access": station.get("hasSteplessAccess"),
                    "step_free_access_description": station.get("steplessAccess"),
                    "has_mobility_service": station.get("hasMobilityService"),
                    "mobility_service_info": station.get("mobilityService"),
                    "has_parking": station.get("hasParking"),
                    "has_bicycle_parking": station.get("hasBicycleParking"),
                    "has_local_public_transport": station.get("hasLocalPublicTransport"),
                    "has_public_facilities": station.get("hasPublicFacilities"),
                    "has_lockers": station.get("hasLockers"),
                    "has_taxi_rank": station.get("hasTaxiRank"),
                    "has_travel_center": station.get("hasTravelCenter"),
                    "has_railway_mission": station.get("hasRailwayMission"),
                    "has_db_lounge": station.get("hasDBLounge"),
                    "has_wifi": station.get("hasWiFi"),
                    "has_travel_necessities": station.get("hasTravelNecessities"),
                    "address": station.get("mailingAddress"),
                    "location": station.get("evaNumbers", [{}])[0].get("geographicCoordinates")
                }
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def check_accessibility_route(from_station: str, to_station: str) -> dict:
    """
    Check accessibility information for a route between two stations.
    
    Args:
        from_station: Departure station name
        to_station: Arrival station name
    
    Returns:
        Accessibility information for both stations on the route
    """
    try:
        # Get details for both stations
        from_details = await get_station_details(from_station)
        to_details = await get_station_details(to_station)
        
        if not from_details["success"] or not to_details["success"]:
            return {
                "success": False,
                "error": "Could not find one or both stations"
            }
        
        # Summarize accessibility
        from_accessible = from_details["station"]["has_step_free_access"] == "yes"
        to_accessible = to_details["station"]["has_step_free_access"] == "yes"
        
        return {
            "success": True,
            "route_accessible": from_accessible and to_accessible,
            "departure": {
                "name": from_details["station"]["name"],
                "step_free_access": from_details["station"]["has_step_free_access"],
                "mobility_service": from_details["station"]["has_mobility_service"]
            },
            "arrival": {
                "name": to_details["station"]["name"],
                "step_free_access": to_details["station"]["has_step_free_access"],
                "mobility_service": to_details["station"]["has_mobility_service"]
            },
            "recommendation": "Route is fully accessible" if from_accessible and to_accessible 
                          else "Some stations may require assistance. Contact DB Mobility Service in advance."
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
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
            "Help with boarding and alighting",
            "Assistance with luggage",
            "Guidance through stations",
            "Reserved seating arrangements",
            "Information about accessible routes"
        ],
        "free_of_charge": True
    }


if __name__ == "__main__":
    # Run the server
    mcp.run()
