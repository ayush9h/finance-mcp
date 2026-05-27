import json
import subprocess
import sys
from typing import List

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from services import exec_ddgs
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

    results = exec_ddgs(
        company_name=company_name,
        company_country=company_country,
    )

    mcp_logger.info(
        "Investor page search completed", total_results=len(results), results=results
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
            "services.web_scrapper",
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
            total_links=len(links.get("links")),
        )

        return links

    except Exception as e:
        mcp_logger.exception(
            "Failed parsing scraper output",
            error=f"Error occured due to:{str(e)}",
        )
        return []


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse(
        {"status": "healthy", "service": "finance-mcp is up and running"}
    )


app = mcp.http_app(transport="http", path="/v1/mcp")
