"""
FastMCP Server with FlexOffers Integration
"""

import requests
import xmltodict
import json
from fastmcp import FastMCP

# Create server
mcp = FastMCP("FlexOffers MCP Server")

# FlexOffers API Configuration
FLEXOFFERS_API_KEY = "beb20686-606a-4e92-8c71-bfa967317ddc"
FLEXOFFERS_BASE_URL = "https://api.flexoffers.com/v3"


@mcp.tool
def get_flexoffers_domains(limit: int = 10) -> str:
    """
    Fetch domains from FlexOffers API
    
    Args:
        limit: Maximum number of domains to return (default: 10)
    
    Returns:
        JSON string containing domain information
    """
    try:
        url = f"{FLEXOFFERS_BASE_URL}/domains"
        headers = {
            "accept": "application/xml",
            "apiKey": FLEXOFFERS_API_KEY
        }
        
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        # Parse XML response to dict
        data = xmltodict.parse(response.text)
        
        # Convert to JSON for easier handling
        result = {
            "status": "success",
            "data": data,
            "total_domains": len(data.get("domains", {}).get("domain", [])) if data.get("domains") else 0
        }
        
        return json.dumps(result, indent=2)
        
    except requests.exceptions.RequestException as e:
        return json.dumps({
            "status": "error",
            "message": f"API request failed: {str(e)}"
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }, indent=2)


@mcp.tool
def echo_tool(text: str) -> str:
    """Echo the input text"""
    return text


@mcp.resource("echo://static")
def echo_resource() -> str:
    return "Echo!"


@mcp.resource("echo://{text}")
def echo_template(text: str) -> str:
    """Echo the input text"""
    return f"Echo: {text}"


@mcp.prompt("echo")
def echo_prompt(text: str) -> str:
    return text