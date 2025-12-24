"""
Test script for get_user_email tool using FastMCP client
"""
import asyncio
from fastmcp import Client

async def test_email_tool():
    # Connect to the running server
    async with Client("http://localhost:8000/sse") as client:
        # Call the get_user_email tool
        result = await client.call_tool("get_user_email", {})
        print("Result from get_user_email:")
        print(result)
        
        # Parse and display the result content
        if result.content:
            for content in result.content:
                if hasattr(content, 'text'):
                    print("\nParsed response:")
                    print(content.text)

if __name__ == "__main__":
    asyncio.run(test_email_tool())
