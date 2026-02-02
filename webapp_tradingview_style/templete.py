import os
from pathlib import Path
import logging

# ------------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s'
)

# ------------------------------------------------------------------
# Project root name
# ------------------------------------------------------------------
project_name = "tradingview_super_chart"

# ------------------------------------------------------------------
# Files & folders to be created
# ------------------------------------------------------------------
list_of_files = [
    # Root app package
    f"{project_name}/app/__init__.py",
    f"{project_name}/app/config.py",
    f"{project_name}/app/main_fastapi.py",
    f"{project_name}/app/main_streamlit.py",
    f"{project_name}/app/main_dash.py",

    # Core logic
    f"{project_name}/app/core/__init__.py",
    f"{project_name}/app/core/data.py",
    f"{project_name}/app/core/ta.py",

    # Charts
    f"{project_name}/app/charts/__init__.py",
    f"{project_name}/app/charts/lightweight.py",
    f"{project_name}/app/charts/plotly_charts.py",

    # Data
    f"{project_name}/data/sample_ohlcv.csv",

    # Docker
    f"{project_name}/docker/Dockerfile.fastapi",
    f"{project_name}/docker/Dockerfile.streamlit",
    f"{project_name}/docker/Dockerfile.dash",

    # Project-level files
    f"{project_name}/requirements.txt",
    f"{project_name}/docker-compose.yml",
    f"{project_name}/.env",
    f"{project_name}/README.md",
]

# ------------------------------------------------------------------
# Create directories and files
# ------------------------------------------------------------------
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Create directory if needed
    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir}")

    # Create file if missing or empty
    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")