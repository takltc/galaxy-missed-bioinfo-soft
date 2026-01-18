FROM python:3.11-slim

LABEL maintainer="Galaxy PRS Tools"
LABEL description="PRS Percentile Calculator - Calculate population percentiles for PRS scores"
LABEL version="1.0.0"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir numpy pandas scipy

COPY prs_percentile.py /usr/local/bin/prs_percentile.py
RUN chmod +x /usr/local/bin/prs_percentile.py

WORKDIR /data

ENTRYPOINT ["python", "/usr/local/bin/prs_percentile.py"]
CMD ["--help"]
