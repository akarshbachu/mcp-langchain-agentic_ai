from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(city: str) -> str:
    """
    Get the weather for a given city
    """
    if city == "Hyderabad":
        return "25 degrees Celsius and sunny"
    elif city == "Bengaluru":
        return "30 degrees Celsius and humid"
    elif city == "Delhi":
        return "28 degrees Celsius and cloudy"
    else:
        return "Weather information not available for this city"

if __name__ == "__main__":
    print("Starting Weather MCP Server...")
    # What is streamable-http?
    # It runs in the form of an API with a specific URL hosted
    mcp.run(transport="streamable-http")
