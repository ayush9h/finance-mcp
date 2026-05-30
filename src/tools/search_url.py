from src.services import exec_ddgs
from prefab_ui.components import DataTable, DataTableColumn
from src.utils.logger import get_logger

from fastmcp import FastMCP

logger = get_logger(__name__)


def register_search_page_tool(mcp: FastMCP):
    @mcp.tool(
        name="search_page_tool",
        meta={
            "version": "0.1",
        },
        description="Extracts the investor page url for a particular company for annual reports scraping",
        tags={"investor page link", "annual report url"},
        app=True,
    )
    def search_page_url(company_name: str, company_country: str) -> DataTable:

        logger.info(
            "Searching investor page",
            company_name=company_name,
            company_country=company_country,
        )

        results = exec_ddgs(
            company_name=company_name,
            company_country=company_country,
        )

        logger.info(
            "Investor page search completed",
            total_results=len(results),
            results=results,
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
