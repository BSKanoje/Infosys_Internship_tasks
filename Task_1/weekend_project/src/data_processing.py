import pandas as pd
from typing import Optional
import json

def load_fitness_data(file_path: str, file_type: str = 'auto') -> pd.DataFrame:
    """Load fitness data from various formats (CSV, JSON, Excel).
    - file_type: 'csv', 'json', 'excel', or 'auto'
    Returns a pandas.DataFrame standardized to columns: ['timestamp', ...]
    Raises ValueError with helpful message on failure.
    """
    if file_type == 'auto':
        if str(file_path).lower().endswith('.csv'):
            file_type = 'csv'
        elif str(file_path).lower().endswith(('.json', '.geojson')):
            file_type = 'json'
        elif str(file_path).lower().endswith(('.xls', '.xlsx')):
            file_type = 'excel'
        else:
            # try CSV first, then JSON, then Excel
            try:
                return pd.read_csv(file_path)
            except Exception:
                pass
            try:
                return pd.read_json(file_path)
            except Exception:
                pass
            try:
                return pd.read_excel(file_path)
            except Exception as e:
                raise ValueError(f"Could not auto-detect file type and failed to load: {e}")
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        elif file_type == 'json':
            # support nested json by normalizing
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            df = pd.json_normalize(raw)
        elif file_type == 'excel':
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file_type: {file_type}")
    except Exception as e:
        raise ValueError(f"Failed to load file '{file_path}': {e}")
    # Basic standardization: lower-case columns
    df.columns = [c.strip() for c in df.columns]
    return df
