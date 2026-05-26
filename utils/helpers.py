from typing import Dict, List


def normalize_link(link: Dict) -> Dict:

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


def deduplicate_links(links: List[Dict]) -> List[Dict]:
    seen = set()
    result = []
    for link in map(normalize_link, links):

        href = link.get("href")
        if href and href not in seen:
            seen.add(href)
            result.append(href)

    return result
