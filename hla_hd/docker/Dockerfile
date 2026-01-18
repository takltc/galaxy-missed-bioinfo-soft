# HLA-HD Docker Image
FROM --platform=linux/amd64 continuumio/miniconda3:24.7.1-0

LABEL maintainer="Galaxy Tools"
LABEL version="1.7.0"
LABEL description="HLA-HD: High-resolution HLA typing from NGS data"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:/opt/hlahd:$PATH"
ENV HLAHD_HOME="/opt/hlahd"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    unzip \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install -y python=3.11 bowtie2=2.5.4 samtools=1.21 && \
    conda clean -afy

RUN mkdir -p /opt/hlahd && \
    cd /opt/hlahd && \
    wget -q https://www.genome.med.kyoto-u.ac.jp/HLA-HD/download/hlahd.1.7.0.tar.gz && \
    tar -xzf hlahd.1.7.0.tar.gz && \
    mv hlahd.1.7.0/* . && \
    rm -rf hlahd.1.7.0 hlahd.1.7.0.tar.gz && \
    sh install.sh && \
    chmod +x bin/*

RUN ln -s /opt/hlahd/bin/hlahd.sh /usr/local/bin/hlahd.sh

RUN mkdir -p /opt/hlahd/dictionary && \
    cd /opt/hlahd && \
    wget -q https://www.genome.med.kyoto-u.ac.jp/HLA-HD/download/release/dictionary_v1.7.0.zip && \
    unzip -q dictionary_v1.7.0.zip -d dictionary && \
    rm dictionary_v1.7.0.zip

RUN hlahd.sh 2>&1 | head -5 || echo "HLA-HD installed"

WORKDIR /data

ENTRYPOINT ["hlahd.sh"]
CMD ["--help"]
