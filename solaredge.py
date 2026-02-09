from typing import Any
import os
from urllib.parse import urlencode, quote
import json
import logging

import httpx
from mcp.server.fastmcp import FastMCP
from helpers.client import Client

# Initialize FastMCP server
mcp = FastMCP("solaredge")

# Constants
API_BASE_URL = "https://monitoringapi.solaredge.com"
DEFAULT_HEADERS = dict(Accept="application/json")

client = Client(API_BASE_URL)

@mcp.tool()
# Test function to get access token
# async def test_get_access_token():
#     """Test function to authenticate and get an access token."""
#     try:
#         logging.info(client.api_key)
#         logging.info(client.api_key_secret)
#         # This will trigger the authentication flow
#         auth_header = await client.auth_header()
#         logging.info("✅ Authentication successful!")
#         logging.info(f"Auth header: {auth_header}")
#         return auth_header
#     except Exception as e:
#         logging.error(f"❌ Authentication failed: {e}")
#         return None

@mcp.tool()
async def get_sites(state: str) -> str:
    """Get SolarEdge sites."""
    path = "/sites/list"
    data = await client.request("GET", path)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

@mcp.tool()
async def get_site_details(site_id: int) -> str:
    """Get SolarEdge site details."""
    path = f"/site/{site_id}/details"
    data = await client.request("GET", path)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

@mcp.tool()
async def get_site_energy(site_id: int, timeUnit: str = "Day", startTime: str = None, endTime: str = None) -> str:
    """Get SolarEdge site energy data.
    
    Args:
        site_id: The ID of the SolarEdge site
        timeUnit: Time unit for energy data (Day, Week, Month, Year, Quarter)
        startTime: Start date in YYYY-MM-DD format (defaults to today)
        endTime: End date in YYYY-MM-DD format (defaults to today)
    """
    from datetime import datetime, timedelta
    
    # Set default dates to today if not provided
    if not startTime:
        startTime = datetime.now().strftime("%Y-%m-%d")
    if not endTime:
        endTime = datetime.now().strftime("%Y-%m-%d")
    
    path = f"/site/{site_id}/energy"
    query_params = {
        "timeUnit": timeUnit,
        "startDate": startTime,
        "endDate": endTime
    }
    data = await client.request("GET", path, query=query_params)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

@mcp.tool()
async def get_current_power_flow(site_id: int) -> str:
    """Get SolarEdge site current power flow data."""
    path = f"/site/{site_id}/currentPowerFlow"
    data = await client.request("GET", path)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

@mcp.tool()
async def get_site_overview(site_id: int) -> str:
    """Get SolarEdge site overview with current power and energy data."""
    path = f"/site/{site_id}/overview"
    data = await client.request("GET", path)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

@mcp.tool()
async def get_site_power(site_id: int, startTime: str = None, endTime: str = None) -> str:
    """Get SolarEdge site power measurements.
    
    Args:
        site_id: The ID of the SolarEdge site
        startTime: Start time in ISO format (defaults to 24 hours ago)
        endTime: End time in ISO format (defaults to now)
    """
    from datetime import datetime, timedelta
    import pytz
    
    # Set default times to last 24 hours if not provided
    if not startTime:
        startTime = (datetime.now(pytz.UTC) - timedelta(hours=24)).isoformat()
    if not endTime:
        endTime = datetime.now(pytz.UTC).isoformat()
    
    path = f"/site/{site_id}/power"
    query_params = {
        "startTime": startTime,
        "endTime": endTime
    }
    data = await client.request("GET", path, query=query_params)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

@mcp.tool()
async def get_site_environmental_benefits(site_id: int) -> str:
    """Get SolarEdge site environmental benefits data."""
    path = f"/site/{site_id}/envBenefits"
    data = await client.request("GET", path)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

@mcp.tool()
async def get_site_inventory(site_id: int) -> str:
    """Get SolarEdge site equipment inventory."""
    path = f"/site/{site_id}/inventory"
    data = await client.request("GET", path)

    if not data:
        return "Unable to fetch data - API request failed or returned empty response"
    return data

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
