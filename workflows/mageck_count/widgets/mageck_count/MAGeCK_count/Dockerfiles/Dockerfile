# Base image Debian trixie (13)
FROM debian:trixie-20241202-slim

# Install Python andbasic dependencies for R
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    git \
    gcc \
    python3-pip \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    zlib1g-dev \
    libudunits2-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libpq-dev \
    libcairo2-dev \
    libsqlite3-dev \
    libmariadbd-dev \
    libssh2-1-dev \
    unixodbc-dev \
    pandoc \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    cmake \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# (Python 3.12 installed by default)

# Install python packages
RUN rm /usr/lib/python3.12/EXTERNALLY-MANAGED \
    && pip install numpy scipy setuptools

# Install R for Debian 13 (should be version 4.4.2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    r-base \
    r-base-dev

# Install R packages
RUN R -e "install.packages(c('tidyverse', 'rmarkdown', 'reshape2', 'fgsea', 'pheatmap', 'xtable', 'RColorBrewer', 'gplots'), dependencies=TRUE, repos='https://cloud.r-project.org/')"

## Install MAGeCK v0.5.9.5 by downloading and unzipping from sourceforge source code
# RUN wget -O mageck-0.5.9.5.tar.gz https://sourceforge.net/projects/mageck/files/0.5/mageck-0.5.9.5.tar.gz/download && \
#    tar -xzf mageck-0.5.9.5.tar.gz
##  Set the working directory to the MAGeCK directory
# WORKDIR liulab-mageck-c491c3874dca

# Copy run_mageck_count.sh script into the container's /usr/local/bin and make it executable
COPY run_mageck_count.sh /usr/local/bin/run_mageck_count.sh
RUN chmod +x /usr/local/bin/run_mageck_count.sh

# Copy MAGeCK v0.5.9.5 folder (with --pdf_report fix)
COPY mageck-0.5.9.5 /app/mageck-0.5.9.5

# Set working directory to MAGeCK directory
WORKDIR /app/mageck-0.5.9.5

# Install MAGeCK
RUN python3 setup.py install

# Set working directory to /outputs (MAGeCK outputs are stored here, will move to mounted user-specified directory later)
WORKDIR /outputs

# Enter container as bash
CMD ["/bin/bash"]
# ENTRYPOINT echo "Welcome to MAGeCK Docker" & mageck --version & /bin/bash