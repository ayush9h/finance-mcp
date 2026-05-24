import requests
from bs4 import BeautifulSoup


def duckduckgo_search(query):

    url = "https://html.duckduckgo.com/html/"

    response = requests.post(
        url,
        data={"q": query},
        headers={"User-Agent": ("Mozilla/5.0")},
        timeout=30,
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    results = []

    for result in soup.select(".result"):

        title_elem = result.select_one(".result__title")
        link_elem = result.select_one(".result__url")
        snippet_elem = result.select_one(".result__snippet")

        results.append(
            {
                "title": (title_elem.get_text(strip=True) if title_elem else ""),
                "url": (link_elem.get_text(strip=True) if link_elem else ""),
                "snippet": (snippet_elem.get_text(strip=True) if snippet_elem else ""),
            }
        )

    return results


results = duckduckgo_search("nestle india annual report page")


for item in results[:5]:
    print(item)
