"""
Test script for get_user_email tool - testing header passthrough with httpx
"""
import httpx
import json

base_url = "http://localhost:8000/mcp"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "user-email": "kiran@example.com",
    "user-level": "Expert"
}

# Initialize the MCP connection
init_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
}

print("Testing MCP server with user-email header...")
print(f"Headers: user-email={headers['user-email']}, user-level={headers['user-level']}")
print("-" * 50)

with httpx.Client() as client:
    try:
        # Initialize
        response = client.post(base_url, json=init_payload, headers=headers, timeout=10)
        print(f"Init Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Init Response: {response.text[:300]}...")
        else:
            print(f"Init Response: {response.text}")
        
        # Call the get_user_email tool
        tool_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_user_email",
                "arguments": {}
            }
        }
        
        response = client.post(base_url, json=tool_payload, headers=headers, timeout=10)
        print(f"\nTool Call Status: {response.status_code}")
        print(f"Tool Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")
