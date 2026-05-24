from typing import Dict, List
import json


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
