import json
import subprocess
import sys
from src.utils.logger import get_logger
from src.utils.patterns import annual_report_regex
from fastmcp import FastMCP

logger = get_logger(__name__)


def register_scrape_page_tool(mcp: FastMCP):

    @mcp.tool(
        name="scrape_page_tool",
        meta={
            "version": "0.1",
        },
        description="Scraps the investor page url for the annual reports",
        tags={"investor page link", "scrape"},
    )
    def scrape_url(investor_page_url: str):

        logger.info(
            "Starting scrape",
            investor_page_url=investor_page_url,
        )

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "src.services.scrape_inv_url",
                investor_page_url,
            ],
            capture_output=True,
            text=True,
        )
        if result.stderr:
            logger.info("Logs from standalone scraper:\n%s", result.stderr)

        if result.returncode != 0:
            logger.error(
                "Scraping failed",
                stderr=result.stderr,
            )
            return []

        try:
            data = json.loads(result.stdout)
            logger.info(f"data:{data}")

            annual_report_links = []

            for link in data.get("links", []):

                obj = {}

                for key, value in link.get("value", []):
                    obj[key] = value.get("value")

                text = obj.get("text", "")
                href = obj.get("href", "")

                searchable_text = f"{text} {href}".lower()

                if annual_report_regex.search(searchable_text):
                    annual_report_links.append(
                        {
                            "text": text,
                            "href": href,
                        }
                    )

            logger.info(
                "Scraping completed",
                total_links=len(data.get("links", [])),
                annual_report_links=len(annual_report_links),
            )

            return annual_report_links

        except Exception as e:
            logger.exception(
                "Failed parsing scraper output",
                error=f"Error occured due to:{str(e)}",
            )
            return []
