# SpaceX Falcon 9 First-Stage Landing Capstone

This repository contains the course capstone notebooks and Python scripts for API collection, data wrangling, EDA, SQL, Folium, Plotly Dash and classification.

## Run locally
1. `python -m venv .venv`
2. Activate the environment.
3. `pip install -r requirements.txt`
4. `python src/download_data.py`
5. `python src/analysis.py`
6. `python src/folium_map.py`
7. `python src/dashboard.py` and open `http://127.0.0.1:8050`.

The SQL queries in `sql/analysis_queries.sql` are for the IBM course SQL lab dataset/table `SPACEXTBL`. Its 101-row snapshot is distinct from the 179-row modelling extract. SQL results are transcribed from the IBM course notebook and labelled accordingly.

## Project structure
- `notebooks/`: collection, wrangling, EDA, SQL, map, dashboard and prediction notebooks
- `src/`: Python scripts for data download, analysis, Folium and Dash
- `sql/`: SQL lab queries
- `outputs/`: model metrics, SQL summaries and chart/map previews

**Data note:** The course CSV is downloaded by `src/download_data.py` into `data/`. Run that step before the notebooks or analysis scripts. The data file is not committed here.
