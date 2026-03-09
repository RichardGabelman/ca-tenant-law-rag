from bs4 import BeautifulSoup


def parse_lob(lob_path):
    with open("pubinfo_2025/" + lob_path, "r", encoding="latin-1") as f:
        content = f.read()

    # Fix curly quote encoding artifacts
    content = content.replace("â", '"').replace("â", '"').replace("â", "'")

    soup = BeautifulSoup(content, "xml")
    paragraphs = soup.find_all("p")

    subdivisions = []
    full_text_parts = []

    for p in paragraphs:
        for span in p.find_all("span"):
            span.decompose()
        text = p.get_text(strip=True)
        if text:
            subdivisions.append(text)
            full_text_parts.append(text)

    return {"full_text": "\n".join(full_text_parts), "subdivisions": subdivisions}
