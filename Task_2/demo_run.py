import pandas as pd
import matplotlib.pyplot as plt
import os
import random
from data_format_mastery.loader import load_fitness_data
from data_format_mastery.converter import convert_format

def create_sample_data():
    return pd.DataFrame({
        'timestamp': pd.date_range('2023-01-01', periods=100, freq='h'),
        'heart_rate' : random.randint(55, 120),          
        'sleep_duration' : random.uniform(0, 12),         
        'step_count' : random.randint(0, 200),  
    })

def compare_formats(df, base_dir='Task_2/visuals'):
    formats = ['csv','json','excel','parquet']
    results = []
    os.makedirs(base_dir, exist_ok=True)

    for f in formats:
        path = os.path.join(base_dir, f'data.{f if f != "excel" else "xlsx"}')
        convert_format(df, path, f)
        size = os.path.getsize(path)
        try:
            df2 = load_fitness_data(path, file_type=f if f != 'excel' else 'excel')
            load_time = df2.attrs.get('load_time', None)
        except Exception:
            load_time = None
        results.append({'format': f, 'size': size, 'load_time': load_time})

    res_df = pd.DataFrame(results)
    res_df.to_csv(os.path.join(base_dir, 'comparison.csv'), index=False)

    # Plot size comparison
    fig, ax1 = plt.subplots()
    ax1.bar(res_df['format'], res_df['size'])
    ax1.set_title('File Size by Format')
    ax1.set_ylabel('Bytes')
    plt.savefig(os.path.join(base_dir, 'size_comparison.png'))
    plt.close()

    # Plot time comparison
    fig, ax2 = plt.subplots()
    ax2.bar(res_df['format'], res_df['load_time'])
    ax2.set_title('Load Time by Format')
    ax2.set_ylabel('Seconds')
    plt.savefig(os.path.join(base_dir, 'time_comparison.png'))
    plt.close()

if __name__ == "__main__":
    df = create_sample_data()
    compare_formats(df)
    print("Comparison done. Check visuals/ folder.")
