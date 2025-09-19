# Weekend Project — Streamlit Data Uploader

## Overview
This project is a small data-science-friendly starter template that includes:
- A clean project structure
- A Streamlit app to upload CSV/JSON/Excel files
- Utilities for robust data loading and timestamp normalization

## Structure
```
weekend_project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data_processing.py
│   └── utils.py
├── assets/
│   └── logo.png
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Tasks implemented
- Project scaffold (folders + example data)
- `load_fitness_data` supporting CSV/JSON/Excel with graceful errors
- `detect_and_normalize_timestamps` for converting timestamps to UTC
- Streamlit app with file upload, dataset info, preview, and sidebar

## Run locally
1. Create a virtual environment (recommended)
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run the Streamlit app:
```
streamlit run streamlit_app.py
```

## Deliverables included
- Complete folder structure
- Working Streamlit app code
- `requirements.txt` and this `README.md`
- Sample data in `data/raw/sample_fitness.csv`
- Simple logo at `assets/logo.png`

## Bonus / Ideas to extend
- Add custom CSS (partial included)
- Add interactive widgets (filters, sliders)
- Export cleaned data to `data/processed/`
- Add unit tests and CI config

