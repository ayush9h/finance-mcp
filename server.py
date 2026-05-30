import json
import subprocess
import sys

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from src.services import exec_ddgs
from src.utils import get_logger, setup_logging
from src.utils.patterns import annual_report_regex
from prefab_ui.components import DataTable, DataTableColumn

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
    app=True,
)
def find_investor_page_url(company_name: str, company_country: str) -> DataTable:

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

    return DataTable(
        columns=[
            DataTableColumn(key="title", header="Title", sortable=True),
            DataTableColumn(key="url", header="URL", sortable=True),
            DataTableColumn(key="snippet", header="Short Snippet", sortable=True),
        ],
        rows=results,  # type: ignore
        search=True,
    )


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
        data = json.loads(result.stdout)

        annual_report_links = []

        for link in data.get("links", []):
            text = link.get("text", "")
            href = link.get("href", "")

            searchable_text = f"{text} {href}".lower()

            if annual_report_regex.search(searchable_text):
                annual_report_links.append(link)

        mcp_logger.info(
            "Scraping completed",
            total_links=len(data.get("links", [])),
            annual_report_links=len(annual_report_links),
        )

        return annual_report_links

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
