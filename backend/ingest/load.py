import os
import pandas as pd
from dotenv import load_dotenv
from parse import parse_lob

load_dotenv()

PUBINFO_DIR = os.getenv("PUBINFO_DIR")


def load_tenant_sections(pubinfo_dir: str = PUBINFO_DIR) -> pd.DataFrame:
    df = pd.read_csv(
        os.path.join(pubinfo_dir, "LAW_SECTION_TBL.dat"),
        sep="\t",
        encoding="latin-1",
        header=0,
    )
    df.columns = [
        "section_id",
        "code",
        "section_num",
        "statute_year",
        "chapter",
        "col5",
        "col6",
        "uuid",
        "col8",
        "col9",
        "col10",
        "col11",
        "col12",
        "enactment_history",
        "lob_file",
        "active_flag",
        "source",
        "updated_at",
    ]

    civ = df[df["code"] == "`CIV`"].copy()
    civ["section_num_clean"] = civ["section_num"].str.strip("`").str.rstrip(".")
    civ["section_num_float"] = pd.to_numeric(civ["section_num_clean"], errors="coerce")

    tenant = civ[civ["section_num_float"].between(1940, 1954)].copy()
    tenant = tenant.sort_values("section_num_float")
    return tenant


def build_chunks(pubinfo_dir: str = PUBINFO_DIR) -> list[dict]:
    tenant = load_tenant_sections(pubinfo_dir)
    chunks = []

    for _, row in tenant.iterrows():
        section_num = row["section_num_clean"]
        lob_path = os.path.join(pubinfo_dir, row["lob_file"])

        try:
            parsed = parse_lob(lob_path)
            chunk = {
                "section_num": section_num,
                "section_id": row["section_id"].strip("`"),
                "enactment_history": row["enactment_history"].strip("`")
                if pd.notna(row["enactment_history"])
                else "",
                "full_text": parsed["full_text"],
                "subdivisions": parsed["subdivisions"],
                "citation_url": f"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum={section_num}",
            }
            chunks.append(chunk)
            print(f"{section_num} OK")
        except Exception as e:
            print(f"{section_num} - {e}")

    return chunks
