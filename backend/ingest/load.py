import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

PUBINFO_DIR = os.getenv('PUBINFO_DIR')

def load_tenant_sections(pubinfo_dir: str = PUBINFO_DIR) -> pd.DataFrame:
    df = pd.read_csv(
        os.path.join(pubinfo_dir, 'LAW_SECTION_TBL.dat'),
        sep='\t',
        encoding='latin-1',
        header=0
    )
    df.columns = [
        'section_id', 'code', 'section_num', 'statute_year', 'chapter',
        'col5', 'col6', 'uuid', 'col8', 'col9', 'col10', 'col11', 'col12',
        'enactment_history', 'lob_file', 'active_flag', 'source', 'updated_at'
    ]

    civ = df[df['code'] == '`CIV`'].copy()
    civ['section_num_clean'] = civ['section_num'].str.strip('`').str.rstrip('.')
    civ['section_num_float'] = pd.to_numeric(civ['section_num_clean'], errors='coerce')

    tenant = civ[civ['section_num_float'].between(1940, 1954)].copy()
    tenant = tenant.sort_values('section_num_float')
    return tenant
