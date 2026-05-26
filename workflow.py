import json
from typing import Any, Dict

from fastmcp import Client

from utils import deduplicate_links

MCP_SERVER_URL = "http://localhost:8000/mcp"


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
                "find_investor_page_url",
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
    ):

        async with self.client:

            result = await self.client.call_tool(
                "scrape_url",
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

        workflow_logs = []

        workflow_logs.append("Searching investor relations page...")

        investor_results = await self.find_investor_page(
            company_name=company_name,
            company_country=company_country,
        )

        if not investor_results:

            return {
                "status": "error",
                "logs": workflow_logs,
                "message": "No investor page found",
            }

        best_match = investor_results[0]

        workflow_logs.append(f"Investor page found: {best_match['url']}")

        workflow_logs.append("Starting annual report scraping...")

        scraped_data = await self.scrape_page(investor_page_url=best_match["url"])

        raw_links = scraped_data.get("links", [])

        workflow_logs.append(f"Found {len(raw_links)} raw links")

        unique_links = deduplicate_links(raw_links)

        workflow_logs.append(f"Deduplicated into {len(unique_links)} links")

        return {
            "status": "success",
            "company_name": company_name,
            "company_country": company_country,
            "investor_page_url": best_match["url"],
            "links": unique_links,
            "logs": workflow_logs,
        }
