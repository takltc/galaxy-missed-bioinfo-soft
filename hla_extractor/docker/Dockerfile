FROM --platform=linux/amd64 continuumio/miniconda3:24.7.1-0

LABEL maintainer="Galaxy Tools"
LABEL version="1.0.0"
LABEL description="HLA Region Extractor: Extract reads from HLA region"

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
    conda install -y python=3.11 samtools=1.21 && \
    conda clean -afy

RUN samtools --version

WORKDIR /data

ENTRYPOINT ["samtools"]
CMD ["--help"]
