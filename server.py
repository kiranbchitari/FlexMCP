"""
FastMCP Server with FlexOffers Integration
"""

import requests
import xmltodict
import json
import time
from fastmcp import FastMCP

# Create server
mcp = FastMCP("FlexOffers MCP Server")

# FlexOffers API Configuration
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
    Search for promotional LINKS, OFFERS, DEALS, and COUPONS from FlexOffers. 
    Use this tool when users ask for affiliate links, promotional offers, deals, coupons, or product links to share.
    
    Args:
        api_key: FlexOffers API key (required - ask user if not provided)
        name: Search term for the promotion/offer (e.g. "nike shoes", "travel deals", "electronics")
        page: Page number (default: 1)
        page_size: Number of results per page (default: 10)
        
    Returns:
        JSON string containing promotional links and offers
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
    Get top affiliate PROGRAMS to JOIN or APPLY for. 
    Use this tool when users want to discover NEW programs to partner with, NOT for finding promotional links or offers.
    This returns programs the user can apply to become an affiliate for.
    The response contains ProgramID which should be used as advertiser_id in apply_to_program tool.
    
    Args:
        api_key: FlexOffers API key (required - ask user if not provided)
        country_code: Optional country code to filter programs (e.g., 'US', 'GB')
    
    Returns:
        JSON string containing top programs with ProgramID, ProgramName, DomainURL, etc.
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
        
        # Add cache-busting parameter and country_code if provided
        params = {"_t": int(time.time() * 1000)}  # Cache buster
        if country_code:
            params["countryCode"] = country_code
        
        response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
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
def apply_to_program_by_name(api_key: str = None, program_name: str = None, country_code: str = None, accept_terms: bool = None) -> str:
    """
    Find a program by name and apply to it. This tool automatically finds the correct ProgramID.
    Use this when the user wants to apply to a program they saw in the get_top_programs results.
    
    Args:
        api_key: FlexOffers API key (required - ask user if not provided)
        program_name: The name of the program to apply for (from ProgramName in get_top_programs results)
        country_code: Optional country code to filter programs (e.g., 'US', 'GB')
        accept_terms: User must explicitly accept the terms (required - must be true to proceed)
    
    Returns:
        JSON string containing the application result
    """
    # Check if API key is provided
    if not api_key:
        return json.dumps({
            "status": "missing_api_key",
            "message": "Please provide your FlexOffers API key to proceed. Ask the user for their API key."
        }, indent=2)
    
    # Check if program_name is provided
    if not program_name:
        return json.dumps({
            "status": "missing_program_name",
            "message": "Please provide the program name you want to apply for (e.g., 'Total AV', 'Nike')."
        }, indent=2)
    
    # Check if user has accepted terms
    if accept_terms is None:
        return json.dumps({
            "status": "terms_not_accepted",
            "message": "You must accept the terms to apply for this program. Please confirm that you accept the terms and conditions."
        }, indent=2)
    
    if not accept_terms:
        return json.dumps({
            "status": "terms_rejected",
            "message": "You must accept the terms to proceed with the application. Please set accept_terms to true if you agree."
        }, indent=2)
    
    try:
        # Step 1: Fetch programs to find the matching one
        programs_url = "https://content.flexlinks.com/chat/GetGapOpportunityPrograms"
        headers = {"apikey": api_key}
        params = {"_t": int(time.time() * 1000)}  # Cache buster
        if country_code:
            params["countryCode"] = country_code
        
        response = requests.get(programs_url, headers=headers, params=params, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("Success", False):
            return json.dumps({
                "status": "error",
                "message": "Failed to fetch programs list"
            }, indent=2)
        
        programs = data.get("Data", [])
        
        # Step 2: Find matching program by name (case-insensitive partial match)
        matching_program = None
        search_name = program_name.lower()
        for program in programs:
            prog_name = program.get("ProgramName", "").lower()
            if search_name in prog_name or prog_name in search_name:
                matching_program = program
                break
        
        if not matching_program:
            # Return available programs for user to choose from
            available = [p.get("ProgramName") for p in programs[:10]]
            return json.dumps({
                "status": "program_not_found",
                "message": f"Could not find a program matching '{program_name}'. Available programs: {', '.join(available)}"
            }, indent=2)
        
        program_id = matching_program.get("ProgramID")
        actual_name = matching_program.get("ProgramName")
        
        # Step 3: Apply to the program
        apply_url = f"{FLEXOFFERS_BASE_URL}/advertisers/applyAdvertiser"
        apply_params = {
            "advertiserId": program_id,
            "acceptTerms": "true"
        }
        
        apply_response = requests.get(apply_url, headers=headers, params=apply_params, timeout=10, verify=False)
        apply_response.raise_for_status()
        
        try:
            apply_data = apply_response.json()
        except:
            apply_data = apply_response.text
        
        result = {
            "status": "success",
            "message": f"Successfully applied to '{actual_name}' (ProgramID: {program_id})",
            "program_details": {
                "ProgramID": program_id,
                "ProgramName": actual_name,
                "DomainURL": matching_program.get("DomainURL")
            },
            "response": apply_data
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
def apply_to_program(api_key: str = None, advertiser_id: int = None, accept_terms: bool = None) -> str:
    """
    Apply to an affiliate program/advertiser on FlexOffers.
    IMPORTANT: Use the ProgramID from get_top_programs response as the advertiser_id parameter.
    
    Args:
        api_key: FlexOffers API key (required - ask user if not provided)
        advertiser_id: The ProgramID from get_top_programs response (required - do not make up this value)
        accept_terms: User must explicitly accept the terms (required - must be true to proceed)
    
    Returns:
        JSON string containing the application result
    """
    # Check if API key is provided
    if not api_key:
        return json.dumps({
            "status": "missing_api_key",
            "message": "Please provide your FlexOffers API key to proceed. Ask the user for their API key."
        }, indent=2)
    
    # Check if advertiser_id is provided
    if not advertiser_id:
        return json.dumps({
            "status": "missing_advertiser_id",
            "message": "Please provide the Advertiser ID (also called Program ID) you want to apply for."
        }, indent=2)
    
    # Check if user has accepted terms
    if accept_terms is None:
        return json.dumps({
            "status": "terms_not_accepted",
            "message": "You must accept the terms to apply for this program. Please confirm that you accept the terms and conditions."
        }, indent=2)
    
    if not accept_terms:
        return json.dumps({
            "status": "terms_rejected",
            "message": "You must accept the terms to proceed with the application. Please set accept_terms to true if you agree."
        }, indent=2)
    
    try:
        url = f"{FLEXOFFERS_BASE_URL}/advertisers/applyAdvertiser"
        headers = {
            "apikey": api_key
        }
        params = {
            "advertiserId": advertiser_id,
            "acceptTerms": "true"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10, verify=False)
        response.raise_for_status()
        
        # Try to parse response
        try:
            data = response.json()
        except:
            data = response.text
        
        result = {
            "status": "success",
            "message": f"Successfully applied to program/advertiser ID: {program_id}",
            "response": data
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