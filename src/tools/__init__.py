from .search_url import register_search_page_tool
from .scrape_url import register_scrape_page_tool
from fastmcp import FastMCP


def register_tools(mcp: FastMCP):

    # Tool to find the investor page
    register_search_page_tool(mcp=mcp)

    # Tool to scrape the investor page
    register_scrape_page_tool(mcp=mcp)
