import asyncio
import json
import sys
from pathlib import Path
from src.utils.logger import get_logger
import nodriver as uc

logger = get_logger(__name__)

PROFILE_DIR = Path("./automation_profile").absolute()


def ensure_protocol(url: str) -> str:

    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    return url


async def scrape_url(url: str):
    browser = await uc.start(
        headless=False,
        user_data_dir=str(PROFILE_DIR),
    )
    try:

        # ===========This code block================
        # can be made better: Done to prevent redirection=======
        normalized_url = ensure_protocol(url)
        base_url = "/".join(normalized_url.split("/")[:3])

        page = await browser.get(base_url)

        try:
            await page.verify_cf()
        except Exception as e:
            raise Exception(f"Error occured due to{e}")

        await asyncio.sleep(20)

        await page.get(normalized_url)
        await page.activate()
        await asyncio.sleep(10)

        # =======================================================================

        links = await page.evaluate("""
            Array.from(document.querySelectorAll('a'))
                .map(a => ({
                    text: (a.innerText || '').trim(),
                    href: a.href
                }))
                .filter(x => x.href)
            """)
        # logger.info(f"got these:{links}")
        return {
            "links": links,
        }
    finally:
        browser.stop()


async def main():

    try:
        url = sys.argv[1]

        links = await scrape_url(url)

        print(json.dumps(links))

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
