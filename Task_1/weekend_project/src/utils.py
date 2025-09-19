import pandas as pd
import pytz
from dateutil import parser
from typing import Optional

def detect_and_normalize_timestamps(df: pd.DataFrame, timestamp_col: str = 'timestamp', user_location: Optional[str] = None) -> pd.DataFrame:
    """Detect timestamp formats and normalize to UTC (ISO format).
    - Converts column `timestamp_col` to pandas datetime (UTC-aware).
    - If timezone info is missing, assumes UTC.
    - user_location is currently unused but left for extension.
    """
    if timestamp_col not in df.columns:
        raise ValueError(f"Timestamp column '{timestamp_col}' not found in dataframe.")
    # parse datetimes robustly
    def _parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            dt = parser.parse(str(x))
            # if naive, treat as UTC (could be improved to detect zone)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=pytz.UTC)
            return dt.astimezone(pytz.UTC)
        except Exception:
            return pd.NaT
    df = df.copy()
    df[timestamp_col] = df[timestamp_col].apply(_parse)
    return df
