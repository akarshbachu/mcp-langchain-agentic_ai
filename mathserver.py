from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Given 2 numbers a and b, it will add those numbers and returns the result
    Note: It is capable of just add functionality, other math operations are not supported
    """
    return a+b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    Given 2 numbers a and b, it will multiply those numbers and returns the result
    Note: It is capable of just multiply functionality, other math operations are not supported
    """
    return a*b

@mcp.tool()
def sub(a: int, b: int) -> int:
    """
    Given 2 numbers a and b, it will subtract those numbers and returns the result
    Note: It is capable of just sub functionality, other math operations are not supported
    """
    return a-b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """
    Given 2 numbers a and b, it will divide those numbers and returns the result
    Note: It is capable of just divide functionality, other math operations are not supported
    """
    return a/b

if __name__ == "__main__":
    print("Starting Math MCP Server...")
    # What is stdio? 
    # It runs in the terminal it self, it wont run as an API
    mcp.run(transport="stdio")