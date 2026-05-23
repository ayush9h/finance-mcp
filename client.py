import asyncio
from fastmcp import Client
import json

client = Client("http://localhost:8000/mcp")


async def call_tool(company_name: str, company_country: str):
    async with client:

        result = await client.call_tool(
            "find_investor_page_url",
            {"company_name": company_name, "company_country": company_country},
        )
        if result.content[0].type == "text":
            print(json.loads(result.content[0].text))


asyncio.run(call_tool("Nestle", "India"))
