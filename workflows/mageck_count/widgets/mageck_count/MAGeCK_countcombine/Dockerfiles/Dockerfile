FROM python:3.13.1-slim-bookworm

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pandas

ADD combine_counts.py .
RUN chmod +x combine_counts.py