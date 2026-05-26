import asyncio
import json
import sys
from pathlib import Path

import nodriver as uc


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

    await asyncio.sleep(20)
    # =======================================================================

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

    # Using this to be used in stdout
    print(json.dumps(links))


if __name__ == "__main__":
    asyncio.run(main())
