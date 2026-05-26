from typing import List

import requests
from bs4 import BeautifulSoup
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_exponential)

from utils import HEADERS

DDGS_URL = "https://html.duckduckgo.com/html/"


session = requests.Session()
session.headers.update(HEADERS)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(
        (
            requests.RequestException,
            requests.Timeout,
        )
    ),
)
def _search(query: str) -> str:
    try:
        response = session.post(
            DDGS_URL,
            data={"q": query},
            timeout=60,
        )
        return response.text
    except requests.RequestException as e:
        return f"Error occurred due to:{e}"


def exec_ddgs(
    company_name: str,
    company_country: str,
) -> List:
    """
    Search DuckDuckGo HTML results.

    Returns:
    - List of relevant search results
    """

    html = _search(f"{company_name} {company_country} annual report investor relations")

    soup = BeautifulSoup(html, "html.parser")

    results = [
        {
            "title": (e := result.select_one(".result__title"))
            and e.get_text(strip=True)
            or "",
            "url": (e := result.select_one(".result__url"))
            and e.get_text(strip=True)
            or "",
            "snippet": (e := result.select_one(".result__snippet"))
            and e.get_text(strip=True)
            or "",
        }
        for result in soup.select(".result")
    ]

    return results
