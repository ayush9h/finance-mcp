import asyncio
import json

from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool(company_name: str, company_country: str):
    async with client:

        result = await client.call_tool(
            "scrape_url",
            {"investor_page_url": "https://www.nestle.com/investors/annual-report"},
        )
        # print(f"Got the results from the playwright:{result}")
        if result.content[0].type == "text":
            print(json.loads(result.content[0].text))


asyncio.run(call_tool("Nestle", "India"))
