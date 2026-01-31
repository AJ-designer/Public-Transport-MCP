"""
Quick test script to verify the DB Accessibility MCP server works
Run this to test without needing Claude Desktop setup
"""

import asyncio
import sys
import logging
sys.path.insert(0, '/home/claude/db-accessibility-mcp')

from server import search_stations, get_station_details, check_accessibility_route, get_mobility_service_info


async def test_server():
    print("=" * 60)
    print("Testing DB Accessibility MCP Server")
    print("=" * 60)
    
    logger = logging.getLogger()
    # Test 1: Search for stations
    print("\n1️⃣  Testing station search for 'Berlin'...")
    result = await search_stations("Berlin", limit=3)
    if result["success"]:
        print(f"✅ Found {result['count']} stations")
        for station in result["stations"][:2]:
            print(f"   - {station['name']}")
            print(f"     Step-free: {station['has_step_free_access']}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Test 2: Get station details
    print("\n2️⃣  Testing detailed station info for 'München Hbf'...")
    result = await get_station_details("München Hbf")
    if result["success"]: 
        station = result["station"]
        print(f"✅ Station: {station['name']}")
        print(f"   EVA Number: {station['eva_number']}")
        print(f"   Step-free access: {station['step_free_access']}")
        print(f"   Mobility service: {station['mobility_service']}")
        print(f"   WiFi: {station['wifi']}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Test 3: Check route accessibility
    print("\n3️⃣  Testing route accessibility Berlin → Hamburg...")
    result = await check_accessibility_route("Berlin Hbf", "Hamburg Hbf")
    if result["success"]:
        print(f"✅ Route accessible: {result['route_fully_accessible']}")
        print(f"   Departure: {result['departure']['name']} - {result['departure']['step_free']}")
        print(f"   Arrival: {result['arrival']['name']} - {result['arrival']['step_free']}")
        print(f"   💡 {result['recommendation']}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Test 4: Get mobility service info
    print("\n4️⃣  Testing mobility service information...")
    result = await get_mobility_service_info()
    if result["success"]:
        print(f"✅ Service: {result['service']}")
        print(f"   Phone: {result['phone']['national']}")
        print(f"   Hours: {result['phone']['hours']}")
        print(f"   Free: {result['free_of_charge']}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print("\n" + "=" * 60)
    print("✨ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_server())
