from fastmcp import FastMCP
from starlette.responses import JSONResponse

from src.tools import register_tools

mcp = FastMCP("Finance MCP Server")

# Register all tools
register_tools(mcp=mcp)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse(
        {"status": "healthy", "service": "finance-mcp is up and running"}
    )


app = mcp.http_app(transport="http", path="/v1/mcp")
