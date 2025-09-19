import streamlit as st
import pandas as pd
from src.data_processing import load_fitness_data
from src.utils import detect_and_normalize_timestamps

st.set_page_config(page_title='Task 1 - Data Uploader', layout='wide')

# Custom CSS for colors and layout
st.markdown("""
<style>
/* Change background colors */
.reportview-container {
    background-color: #f7f9fc;
}
.sidebar .sidebar-content {
    background-color: #f0f4f8;
    padding: 1rem;
    border-right: 2px solid #d0d7de;
}

/* Title + headers */
h1, h2, h3 {
    color: #2c3e50;
}
h1 {
    color: #1f77b4 !important;  /* main title accent */
}
h2 {
    color: #e67e22 !important;  /* orange for subheaders */
}

/* Buttons */
div.stButton > button:first-child {
    background-color: #1f77b4;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.6em 1.2em;
}
div.stButton > button:first-child:hover {
    background-color: #155a91;
    color: white;
}

/* Checkboxes */
.stCheckbox {
    accent-color: #27ae60;  /* green accent */
}

/* Slider */
.stSlider > div[data-baseweb="slider"] {
    color: #27ae60;
}
.stSlider label {
    color: #2c3e50 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image('assets/logo.jpg', use_container_width=True)
st.sidebar.header('Project Info')
st.sidebar.markdown("""**Task 1**\n
- Simple Streamlit uploader\n
- Supports CSV / JSON \n
- Shows dataset info and preview\n
- ✅ Now with interactive widgets
""")

st.title('📂 Task 1 — Data Upload & Preview')

uploaded = st.file_uploader('Upload CSV / JSON ', type=['csv', 'json'])

if uploaded is not None:
    try:
        with st.spinner('Loading data...'):
            name = uploaded.name
            if name.lower().endswith('.csv'):
                df = load_fitness_data(uploaded, file_type='csv')
            elif name.lower().endswith(('.xls', '.xlsx')):
                df = load_fitness_data(uploaded, file_type='excel')
            elif name.lower().endswith('.json'):
                df = load_fitness_data(uploaded, file_type='json')
            else:
                df = load_fitness_data(uploaded, file_type='auto')

        st.success('✅ File loaded successfully')

        # Dataset info
        st.subheader('Dataset Information')
        st.write(f"**Rows:** {df.shape[0]}  —  **Columns:** {df.shape[1]}")
        st.text(str(df.info(verbose=True)))

        # Interactive row preview
        st.subheader('Data Preview')
        n_rows = st.slider('Select number of rows to preview:', min_value=5, max_value=50, value=10, step=5)
        st.dataframe(df.head(n_rows))

        # Timestamp normalization toggle
        if 'timestamp' in df.columns:
            st.subheader('Timestamp Normalization')
            normalize_flag = st.checkbox('Normalize timestamps to UTC automatically')
            if normalize_flag:
                df2 = detect_and_normalize_timestamps(df, timestamp_col='timestamp')
                preview_cols = ['timestamp']
                if 'timestamp_utc' in df2.columns:
                    preview_cols.append('timestamp_utc')
                st.write("✅ Normalization applied")
                st.dataframe(df2[preview_cols].head(n_rows))
            else:
                st.info('Tick the checkbox above to normalize timestamps.')

    except Exception as e:
        st.error(f'❌ Failed to load file: {e}')

else:
    st.info('Upload a CSV or JSON file to get started.')

# Footer
st.markdown('---')
st.write('To run locally:')
st.code('pip install -r requirements.txt && streamlit run streamlit_app.py')
