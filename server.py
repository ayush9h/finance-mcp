import json
import subprocess
import sys
from typing import List

from ddgs import DDGS
from fastmcp import FastMCP

mcp = FastMCP("Finance MCP Server")


@mcp.tool(
    name="find_investor_page_url",
    meta={
        "version": "0.1",
    },
    description="Extracts the investor page url for a particular company for annual reports scraping",
    tags={"investor page link", "annual report url"},
)
def find_investor_page_url(company_name: str, company_country: str) -> List:

    with DDGS() as ddgs:
        results = ddgs.text(
            f'{company_name} {company_country} "annual report" investor relations url',
            max_results=5,
        )

        return results


@mcp.tool(
    name="scrape_url",
    meta={
        "version": "0.1",
    },
    description="Scraps the investor page url for the annual reports",
    tags={"investor page link", "scrape"},
)
def scrape_url(investor_page_url: str):

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "scrappers.web_scrapper",
            investor_page_url,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    links = json.loads(result.stdout)
    return links


if __name__ == "__main__":
    mcp.run(transport="http", port=8000, show_banner=False)
