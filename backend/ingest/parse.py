"""Parses California Legislative LOB files into structured text."""

from bs4 import BeautifulSoup


def parse_lob(lob_path: str) -> dict:
    """
    Parse a California Legislative LOB file into structured text.

    Returns:
        {
            'full_text': str,
            'subdivisions': list[str]
        }
    """
    with open(lob_path, "rb") as f:
        content = f.read().decode("utf-8", errors="replace")

    soup = BeautifulSoup(content, "xml")
    paragraphs = soup.find_all("p")

    subdivisions = []
    full_text_parts = []

    for p in paragraphs:
        for span in p.find_all("span"):
            span.decompose()
        text = p.get_text(strip=True)
        text = " ".join(text.split())
        if text:
            subdivisions.append(text)
            full_text_parts.append(text)

    return {"full_text": "\n".join(full_text_parts), "subdivisions": subdivisions}
