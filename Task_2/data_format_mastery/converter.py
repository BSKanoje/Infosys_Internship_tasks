import pandas as pd

def convert_format(df: pd.DataFrame, output_path: str, file_type: str):
    """Convert dataframe to another format: csv, json, excel, parquet, xml"""
    try:
        if file_type == 'csv':
            df.to_csv(output_path, index=False)
        elif file_type == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif file_type == 'excel':
            df.to_excel(output_path, index=False)
        elif file_type == 'parquet':
            df.to_parquet(output_path, index=False)
        elif file_type == 'xml':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<root>\n')
                for _, row in df.iterrows():
                    f.write('  <record>\n')
                    for col, val in row.items():
                        f.write(f'    <{col}>{val}</{col}>\n')
                    f.write('  </record>\n')
                f.write('</root>\n')
        else:
            raise ValueError(f"Unsupported conversion format: {file_type}")
    except Exception as e:
        raise ValueError(f"Failed to convert to {file_type}: {e}")
