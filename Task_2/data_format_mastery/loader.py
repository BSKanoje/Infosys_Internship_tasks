import pandas as pd
import json
import xml.etree.ElementTree as ET
import time
from typing import Union

def load_fitness_data(file_path: Union[str, bytes], file_type: str = 'auto') -> pd.DataFrame:
    """
    Load fitness data from CSV, JSON, Excel, Parquet, XML.
    Provides graceful error handling.
    """
    start_time = time.time()
    try:
        # Auto-detect type
        if file_type == 'auto':
            lower = str(file_path).lower()
            if lower.endswith('.csv'):
                file_type = 'csv'
            elif lower.endswith('.json'):
                file_type = 'json'
            elif lower.endswith('.xlsx'):
                file_type = 'excel'
            elif lower.endswith('.parquet'):
                file_type = 'parquet'
            elif lower.endswith('.xml'):
                file_type = 'xml'
            else:
                raise ValueError("Could not auto-detect file type")

        # Load accordingly
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        elif file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            df = pd.json_normalize(raw)
        elif file_type == 'excel':
            df = pd.read_excel(file_path)
        elif file_type == 'parquet':
            df = pd.read_parquet(file_path)
        elif file_type == 'xml':
            tree = ET.parse(file_path)
            root = tree.getroot()
            records = []
            for child in root:
                record = {elem.tag: elem.text for elem in child}
                records.append(record)
            df = pd.DataFrame(records)
        else:
            raise ValueError(f"Unsupported file_type: {file_type}")

        # Clean columns
        df.columns = [str(c).strip().lower() for c in df.columns]
        elapsed = time.time() - start_time
        df.attrs['load_time'] = elapsed
        df.attrs['source_type'] = file_type
        return df

    except Exception as e:
        raise ValueError(f"Failed to load {file_type} file '{file_path}': {e}")
