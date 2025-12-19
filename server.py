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
def get_flexoffers_domains(api_key: str = None, limit: int = 10) -> str:
    """
    Fetch domains from FlexOffers API
    
    Args:
        api_key: FlexOffers API key (required - ask user if not provided)
        limit: Maximum number of domains to return (default: 10)
    
    Returns:
        JSON string containing domain information
    """
    # Check if API key is provided
    if not api_key:
        return json.dumps({
            "status": "missing_api_key",
            "message": "Please provide your FlexOffers API key to proceed. Ask the user for their API key."
        }, indent=2)
    
    try:
        url = f"{FLEXOFFERS_BASE_URL}/domains"
        headers = {
            "accept": "application/xml",
            "apiKey": api_key
        }
        
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        
        # Parse XML response to dict
        data = xmltodict.parse(response.text)
        
        # Handle different response structures
        # Check for DomainDto (single domain response)
        if "DomainDto" in data:
            domain_count = 1
        else:
            # Check for domains collection
            domains = data.get("domains", {}).get("domain", [])
            domain_count = len(domains) if isinstance(domains, list) else (1 if domains else 0)
        
        result = {
            "status": "success",
            "data": data,
            "total_domains": domain_count
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
def get_flexoffers_promotions(api_key: str = None, name: str = None, page: int = 1, page_size: int = 10) -> str:
    """
    Search for promotions from FlexOffers API.
    
    Args:
        api_key: FlexOffers API key (required - ask user if not provided)
        name: Search term for the promotion (e.g. "nike shoe")
        page: Page number (default: 1)
        page_size: Number of results per page (default: 10)
        
    Returns:
        JSON string containing filtered promotion information
    """
    # Check if API key is provided
    if not api_key:
        return json.dumps({
            "status": "missing_api_key",
            "message": "Please provide your FlexOffers API key to proceed. Ask the user for their API key."
        }, indent=2)
    
    # Check if name is provided
    if not name:
        return json.dumps({
            "status": "missing_name",
            "message": "Please provide a search term for the promotion (e.g. 'nike shoe')."
        }, indent=2)
    
    try:
        url = f"{FLEXOFFERS_BASE_URL}/promotions"
        headers = {
            "accept": "application/xml",
            "apiKey": api_key
        }
        params = {
            "names": name,
            "page": page,
            "pageSize": page_size
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
        response.raise_for_status()
        
        # Parse XML response to dict
        data = xmltodict.parse(response.text)
        
        # Extract Results
        results_container = data.get("PaginatedResultSetOfLinkDto", {}).get("Results", {})
        if not results_container:
             return json.dumps({"status": "success", "data": [], "total_count": 0}, indent=2)
             
        link_dtos = results_container.get("LinkDto", [])
        
        # Ensure it's a list even if single item
        if not isinstance(link_dtos, list):
            link_dtos = [link_dtos]
            
        # Filter fields
        filtered_results = []
        for item in link_dtos:
            filtered_item = {
                "AdvertiserId": item.get("AdvertiserId"),
                "AdvertiserName": item.get("AdvertiserName"),
                "LinkName": item.get("LinkName"),
                "LinkDescription": item.get("LinkDescription"),
                "PromotionalTypes": item.get("PromotionalTypes"),
                "LinkUrl": item.get("LinkUrl")
            }
            filtered_results.append(filtered_item)
            
        total_count = data.get("PaginatedResultSetOfLinkDto", {}).get("TotalCount", 0)
        
        result = {
            "status": "success",
            "data": filtered_results,
            "total_count": total_count,
            "page": page,
            "page_size": page_size
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
def get_top_programs(api_key: str = None, country_code: str = None) -> str:
    """
    Get top 10 affiliate programs for promoting and applying from FlexLinks API.
    
    Args:
        api_key: FlexOffers API key (required - ask user if not provided)
        country_code: Optional country code to filter programs (e.g., 'US', 'GB')
    
    Returns:
        JSON string containing top programs for promotion opportunities
    """
    # Check if API key is provided
    if not api_key:
        return json.dumps({
            "status": "missing_api_key",
            "message": "Please provide your FlexOffers API key to proceed. Ask the user for their API key."
        }, indent=2)
    
    try:
        url = "https://content.flexlinks.com/chat/GetGapOpportunityPrograms"
        headers = {
            "apikey": api_key
        }
        
        # Add country_code as query parameter if provided
        params = {}
        if country_code:
            params["countryCode"] = country_code
        
        response = requests.get(url, headers=headers, params=params if params else None, timeout=10, verify=False)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Check if API returned success
        if not data.get("Success", False):
            return json.dumps({
                "status": "error",
                "message": "API returned unsuccessful response"
            }, indent=2)
        
        # Extract programs from Data field and return top 10
        programs = data.get("Data", [])
        top_programs = programs[:10]
        
        result = {
            "status": "success",
            "data": top_programs,
            "total_returned": len(top_programs),
            "message": "Top programs for promoting and applying"
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