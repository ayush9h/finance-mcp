import json
from typing import Any, Dict

from fastmcp import Client

from src.utils import deduplicate_links

MCP_SERVER_URL = "http://localhost:8000/v1/mcp"


class InvestorWorkflow:

    def __init__(self):

        self.client = Client(MCP_SERVER_URL)

    async def find_investor_page(
        self,
        company_name: str,
        company_country: str,
    ):

        async with self.client:

            result = await self.client.call_tool(
                "search_page_tool",
                {
                    "company_name": company_name,
                    "company_country": company_country,
                },
            )

            if result.content and result.content[0].type == "text":
                return json.loads(result.content[0].text)

            return []

    async def scrape_page(
        self,
        investor_page_url: str,
    ) -> Dict:

        async with self.client:

            result = await self.client.call_tool(
                "scrape_page_tool",
                {
                    "investor_page_url": investor_page_url,
                },
            )

            if result.content and result.content[0].type == "text":
                return json.loads(result.content[0].text)

            return {}

    async def execute(
        self,
        company_name: str,
        company_country: str,
    ) -> Dict[str, Any]:
        investor_results = await self.find_investor_page(
            company_name=company_name,
            company_country=company_country,
        )

        if not investor_results:

            return {
                "status": "error",
                "message": "No investor page found",
            }

        best_match = investor_results[0]

        scraped_data: Dict = await self.scrape_page(investor_page_url=best_match["url"])

        unique_links = deduplicate_links(scraped_data.get("links", []))
        return {
            "status": "success",
            "company_name": company_name,
            "company_country": company_country,
            "investor_page_url": best_match["url"],
            "links": unique_links,
        }
