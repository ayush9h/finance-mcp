import asyncio
import json
import sys
from pathlib import Path

import nodriver as uc

from utils import get_logger, setup_logging

setup_logging()

web_logger = get_logger("web_scrapper")


PROFILE_DIR = Path("./automation_profile").absolute()
def ensure_protocol(url: str) -> str:

    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    return url


async def scrap_url(url: str):
    browser = await uc.start(
        headless=False,
        user_data_dir=str(PROFILE_DIR),
    )

    normalized_url = ensure_protocol(url)

    web_logger.info("Warming up session to bypass deep-link redirect...")

    base_url = "/".join(normalized_url.split("/")[:3])

    page = await browser.get(base_url)
    try:
        await page.verify_cf()
    except Exception as e:
        web_logger.warning(
            "Cloudflare verification failed during warm-up", error=str(e)
        )

    await asyncio.sleep(20)
    web_logger.info("Navigation started", requested_url=url)
    await page.get(normalized_url)
    await page.activate()
    await asyncio.sleep(20)

    web_logger.info("Navigation completed", final_url=page.url)

    links = await page.evaluate("""
        Array.from(document.querySelectorAll('a'))
            .map(a => ({
                text: (a.innerText || '').trim(),
                href: a.href
            }))
            .filter(x => x.href)
        """)

    browser.stop()

    return {
        "links": links,
    }


async def main():

    url = sys.argv[1]

    links = await scrap_url(url)
    web_logger.info(
        "Navigation completed",
        total_links=len(links),
    )

    print(json.dumps(links))


if __name__ == "__main__":
    asyncio.run(main())
