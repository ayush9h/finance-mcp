import json
import subprocess
import sys
from typing import List

from ddgs import DDGS
from fastmcp import FastMCP

from utils import get_logger, setup_logging

setup_logging()

mcp_logger = get_logger(name="mcp_logger")

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

    mcp_logger.info(
        "Searching investor page",
        company_name=company_name,
        company_country=company_country,
    )

    with DDGS() as ddgs:
        results = ddgs.text(
            f'{company_name} {company_country} "annual report" investor relations url',
            max_results=5,
        )
        results = list(results)

    mcp_logger.info(
        "Investor page search completed",
        total_results=len(results),
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

    mcp_logger.info(
        "Starting scrape",
        investor_page_url=investor_page_url,
    )

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
        mcp_logger.error(
            "Scraping failed",
            stderr=result.stderr,
        )
        return []

    try:
        links = json.loads(result.stdout)

        mcp_logger.info(
            "Scraping completed",
            total_links=len(links),
        )

        return links

    except Exception as e:
        mcp_logger.exception(
            "Failed parsing scraper output",
            error=f"Error occured due to:{str(e)}",
        )
        return []


if __name__ == "__main__":
    mcp.run(transport="http", port=8000, show_banner=False)
