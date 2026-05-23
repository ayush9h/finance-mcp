from fastmcp import FastMCP
from ddgs import DDGS

mcp = FastMCP("Finance MCP Server")


@mcp.tool
def greet(name: str) -> str:
    return f"Hello my name is {name}"


@mcp.tool(
    name="find_investor_page_url",
    meta={
        "version": "0.1",
    },
    description="Extracts the investor page url for a particular company for annual reports scraping",
    tags={"investor page link", "annual report url"},
)
def find_investor_page_url(company_name: str, company_country: str):

    with DDGS() as ddgs:
        results = ddgs.text(
            f'{company_name} {company_country} "annual report" investor relations url',
            max_results=5,
        )

        return results


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
