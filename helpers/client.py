import json
import logging
import os
from typing import Any

from urllib.parse import quote, urlencode
import httpx

API_BASE_URL = "https://monitoringapi.solaredge.com"
DEFAULT_HEADERS = dict(Accept="application/json")


class Client:
    def __init__(
        self,
        host,
        api_key=None
    ):
        self.host = host
        self.api_key = api_key or os.getenv("SOLAREDGE_API_KEY")
        self.custom_headers = {}

    async def request(self, method, path, query=None, data=None, headers=None):
        escaped_path = quote(path.strip("/"))
        if escaped_path:
            escaped_path = "/" + escaped_path
        url = "{0}{1}".format(self.host, escaped_path)
        
        # Add API key to query parameters for SolarEdge API
        if self.api_key:
            query = query or {}
            query['api_key'] = self.api_key
            
        if query:
            url = "{0}?{1}".format(url, urlencode(query))
            
        logging.info(f"DEBUG: Request URL: {url}")
        return await self._request(method, url, data=data, headers=headers)

    def _login_generate_auth_data(self):
        """
        Creates a dictionary of the required API key data
        """
        return urlencode(
            dict(
                api_key=self.api_key
            )
        ) 

    async def _request(self, method: str, url: str, data=None, query=None, headers=None) -> dict[str, Any] | None:
        """Make a request to the EM API with proper error handling."""
        headers = headers or {"Accept": "application/json"}
        if query:
            url = "{0}?{1}".format(url, urlencode(query))

        async with httpx.AsyncClient() as async_client:
            try:
                if method.upper() == "GET":
                    response = await async_client.get(url, headers=headers, timeout=30.0)
                elif method.upper() == "POST":
                    if data:
                        response = await async_client.post(url, data=data, headers=headers, timeout=30.0)
                    else:
                        response = await async_client.post(url, headers=headers, timeout=30.0)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
            
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logging.error(f"API Error: {e}")
                logging.error(f"Response status: {response.status_code if 'response' in locals() else 'Unknown'}")
                logging.error(f"Response text: {response.text if 'response' in locals() else 'Unknown'}")
                return None
