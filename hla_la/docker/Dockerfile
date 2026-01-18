FROM --platform=linux/amd64 continuumio/miniconda3:24.7.1-0

LABEL maintainer="Galaxy Tools"
LABEL version="1.0.3"
LABEL description="HLA-LA: Graph-based HLA typing from whole genome data"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:/opt/HLA-LA/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    ca-certificates \
    procps \
    libz-dev \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install -y python=3.11 bwa=0.7.18 samtools=1.21 picard=3.1.1 && \
    conda clean -afy

RUN cd /opt && \
    git clone https://github.com/DiltheyLab/HLA-LA.git && \
    cd HLA-LA && \
    git checkout v1.0.3 && \
    make -j4

RUN mkdir -p /opt/HLA-LA/graphs && \
    cd /opt/HLA-LA/graphs && \
    wget -q http://www.well.ox.ac.uk/~dilthey/graphs/PRG_MHC_GRCh38_withIMGT.tar.gz && \
    tar -xzf PRG_MHC_GRCh38_withIMGT.tar.gz && \
    rm PRG_MHC_GRCh38_withIMGT.tar.gz

RUN echo "/opt/HLA-LA/bin/HLA-LA.pl --help" && \
    ls -la /opt/HLA-LA/bin/

WORKDIR /data

ENTRYPOINT ["perl", "/opt/HLA-LA/bin/HLA-LA.pl"]
CMD ["--help"]
