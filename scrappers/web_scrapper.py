import asyncio
import json
import sys
from pathlib import Path

import nodriver as uc

PROFILE_DIR = Path("./automation_profile").absolute()


async def scrap_url(url: str):

    browser = await uc.start(
        headless=False,
        user_data_dir=str(PROFILE_DIR),
    )

    page = await browser.get(url)

    try:
        await page.verify_cf()

    except Exception as e:
        print("Cloudflare verify failed:", e)

    await asyncio.sleep(50)

    links = await page.evaluate(
        """
        Array.from(document.querySelectorAll('a'))
            .map(a => ({
                text: (a.innerText || '').trim(),
                href: a.href
            }))
            .filter(x => x.href)
    """
    )

    browser.stop()

    return links


async def main():
    url = sys.argv[1]
    links = await scrap_url(url)
    print(json.dumps(links))


if __name__ == "__main__":
    asyncio.run(main())
