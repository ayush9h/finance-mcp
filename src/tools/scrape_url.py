import json
import subprocess
import sys

from fastmcp import FastMCP

from src.utils.logger import get_logger

logger = get_logger(__name__)


def register_scrape_page_tool(mcp: FastMCP):
    """
    Tool to scrape the investor relation page for the raw links
    """
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
            return {}

        try:
            data = json.loads(result.stdout)

            logger.info(
                "Scraping completed",
                total_links=len(data.get("links", [])),
            )

            return data

        except Exception as e:
            logger.exception(
                "Failed parsing scraper output",
                error=f"Error occured due to:{str(e)}",
            )
            return {}
