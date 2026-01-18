FROM continuumio/miniconda3:latest

LABEL maintainer="Galaxy PRS Tools"
LABEL description="PRSice-2 - Polygenic Risk Score software for PRS calculation"
LABEL version="2.3.5"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y python=3.11 prsice2=2.3.5 r-base=4.3 && \
    conda clean -afy

RUN PRSice --help || echo "PRSice-2 installed"

WORKDIR /data

ENTRYPOINT ["PRSice"]
CMD ["--help"]
