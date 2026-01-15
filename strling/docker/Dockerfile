# STRling Docker Image (linux/amd64 only - bioconda package constraint)
FROM --platform=linux/amd64 continuumio/miniconda3:24.7.1-0

LABEL maintainer="Galaxy Tools"
LABEL version="0.6.0"
LABEL description="STRling: a k-mer counting approach for STR expansion detection"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install -y python=3.11 strling=0.6.0 samtools=1.21 && \
    conda clean -afy

RUN strling 2>&1 | head -3 && \
    strling-outliers.py --help | head -3

WORKDIR /data

ENTRYPOINT ["strling"]
CMD ["--help"]
