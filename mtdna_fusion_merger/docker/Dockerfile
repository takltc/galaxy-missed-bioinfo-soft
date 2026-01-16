# mtDNA Fusion Merger - Dockerfile
# Implements mtDNA-Server 2 fusion mode for merging Mutserve and Mutect2 variant calls
# Reference: PMID:38709886 (Weissensteiner et al., NAR 2024)

FROM continuumio/miniconda3:24.1.2-0

LABEL maintainer="Omniverse Bioinformatics Team"
LABEL version="1.0.0"
LABEL description="mtDNA variant fusion merger based on mtDNA-Server 2 fusion mode"
LABEL source="https://github.com/genepi/mtdna-server-2"
LABEL pmid="38709886"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    openjdk-11-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖和 bioinformatics 工具
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y \
        python=3.11 \
        bcftools=1.19 \
        csvtk=0.30.0 \
        tabix=1.11 \
        pandas=2.1.4 \
        && conda clean -afy

# 安装 jbang 用于运行 VariantMerger.java
RUN curl -Ls https://sh.jbang.dev | bash -s - app setup && \
    echo 'export PATH="$HOME/.jbang/bin:$PATH"' >> ~/.bashrc

ENV PATH="/root/.jbang/bin:$PATH"

# 复制融合合并脚本
COPY mtdna_fusion_merger.py /opt/mtdna_fusion_merger.py
RUN chmod +x /opt/mtdna_fusion_merger.py

# 复制测试文件
COPY tests/ /opt/tests/

# 验证安装
RUN python --version && \
    bcftools --version && \
    csvtk version

WORKDIR /data

ENTRYPOINT ["python", "/opt/mtdna_fusion_merger.py"]
CMD ["--help"]
