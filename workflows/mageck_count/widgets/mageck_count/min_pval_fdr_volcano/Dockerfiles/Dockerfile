FROM python:3.13.1-slim-bookworm

# Install system dependencies (mainly for dash-bio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libhdf5-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pandas numpy plotly nbformat dash-bio

ADD mageck_test_min_pval_fdr.py .
RUN chmod +x mageck_test_min_pval_fdr.py