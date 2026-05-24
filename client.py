import asyncio
import json

from fastmcp import Client

client = Client("http://localhost:8000/mcp")


def normalize_link(link: dict) -> dict:

    if "href" in link:
        return {
            "text": (link.get("text") or "").strip(),
            "href": (link.get("href") or "").strip(),
        }

    values = dict(link.get("value", []))

    text_obj = values.get("text", {})
    href_obj = values.get("href", {})

    return {
        "text": (text_obj.get("value") or "").strip(),
        "href": (href_obj.get("value") or "").strip(),
    }


def deduplicate_links(links: list[dict]) -> list[dict]:
    seen = set()
    unique_links = []

    for raw_link in links:

        link = normalize_link(raw_link)

        href = link["href"]
        text = link["text"]

        if not href:
            continue

        if href in seen:
            continue

        seen.add(href)

        unique_links.append(
            {
                "text": text,
                "href": href,
            }
        )

    return unique_links


async def some_fn(company_name: str, company_country: str):

    async with client:

        result = await client.call_tool(
            "scrape_url",
            {
                "investor_page_url": "www.nestle.in/investors/stockandfinancials/annualreports",
            },
        )

        scraped_json = {}

        if result.content and result.content[0].type == "text":
            scraped_json = json.loads(result.content[0].text)

        raw_links = scraped_json.get("links", [])

        unique_links = deduplicate_links(raw_links)

        return {
            "company_name": company_name,
            "company_country": company_country,
            "links": unique_links,
        }


if __name__ == "__main__":

    data = asyncio.run(
        some_fn(
            company_name="Nestle",
            company_country="India",
        )
    )

    print(json.dumps(data, indent=2, ensure_ascii=False))
