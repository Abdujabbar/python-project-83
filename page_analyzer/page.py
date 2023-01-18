from bs4 import BeautifulSoup

TAGS = [("title", {}), ("h1", {}), ("meta", {"name": "description"})]


def get_page_data(content):
    soup = BeautifulSoup(content, "html.parser")

    res = {}

    for search_tag, conditions in TAGS:
        found_node = soup.find(search_tag, conditions)
        if not found_node:
            continue

        res[search_tag] = (
            found_node.get_text()
            or found_node.attrs.get("content", "")
        )

    return res
