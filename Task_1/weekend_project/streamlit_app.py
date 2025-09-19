import streamlit as st
import pandas as pd
from src.data_processing import load_fitness_data
from src.utils import detect_and_normalize_timestamps
from PIL import Image
import io

st.set_page_config(page_title='Task 1 - Data Uploader', layout='wide')

# Custom CSS
st.markdown("""<style>
.reportview-container .main .block-container{
    padding-top: 1rem;
}
.sidebar .sidebar-content {
    padding: 1rem;
}
.logo {
    max-width: 220px;
    margin-bottom: 8px;
}
</style>""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image('assets/logo.png', use_container_width=True)
st.sidebar.header('Project Info')
st.sidebar.markdown("""**Task 1**\n
- Simple Streamlit uploader\n
- Supports CSV / JSON \n
- Shows dataset info and first 10 rows
""")

st.title('📂 Task 1 — Data Upload & Preview')

uploaded = st.file_uploader('Upload CSV / JSON ', type=['csv','json'])
# hhh
if uploaded is not None:
    try:
        # save to buffer (Streamlit gives UploadedFile)
        with st.spinner('Loading data...'):
            # attempt to infer type from name
            name = uploaded.name
            if name.lower().endswith('.csv'):
                df = load_fitness_data(uploaded, file_type='csv')
            elif name.lower().endswith(('.xls','.xlsx')):
                df = load_fitness_data(uploaded, file_type='excel')
            elif name.lower().endswith('.json'):
                df = load_fitness_data(uploaded, file_type='json')
            else:
                df = load_fitness_data(uploaded, file_type='auto')
        st.success('File loaded successfully')
        st.subheader('Dataset Information')
        st.write(df.info())  # prints to console; also show shape
        st.write(f"**Rows:** {df.shape[0]}  —  **Columns:** {df.shape[1]}")
        st.subheader('First 10 rows')
        st.dataframe(df.head(10))
        # Timestamp normalization demo if 'timestamp' column exists
        if 'timestamp' in df.columns:
            if st.button('Normalize timestamps to UTC'):
                df2 = detect_and_normalize_timestamps(df, timestamp_col='timestamp')
                st.subheader('Timestamps after normalization (first 10)')
                st.dataframe(df2[['timestamp']].head(10))
    except Exception as e:
        st.error(f'Failed to load file: {e}')

else:
    st.info('Upload a CSV or JSON file to get started.')

# Footer / instructions
st.markdown('---')
st.write('To run locally:')
st.code('pip install -r requirements.txt && streamlit run streamlit_app.py')
