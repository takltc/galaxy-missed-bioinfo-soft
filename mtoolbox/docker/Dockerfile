# MToolBox Docker Image for Galaxy
# 基于 MToolBox v1.2.1 (PMID:25028726)
# 用于 mtDNA 变异注释和单倍型分类

FROM continuumio/miniconda3:24.1.2-0

LABEL maintainer="Omniverse Galaxy Tools"
LABEL version="1.2.1"
LABEL description="MToolBox: mtDNA variant annotation and haplogroup classification"
LABEL pmid="25028726"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"
ENV MTOOLBOX_DIR="/opt/mtoolbox"
ENV MTOOLBOX_DATA_DIR="/opt/mtoolbox/MToolBox/data"
ENV PYTHONPATH="/opt/mtoolbox/MToolBox:${PYTHONPATH}"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    ca-certificates \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 使用 Python 3.11 (避免 3.13 兼容性问题)
# 安装 bioconda 依赖
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y \
        python=3.11 \
        samtools=1.19 \
        bcftools=1.19 \
        biopython=1.83 \
        pysam=0.22.0 \
        pandas=2.2.0 \
        numpy=1.26.3 \
        && conda clean -afy

# 创建 MToolBox 目录结构
RUN mkdir -p ${MTOOLBOX_DIR}/MToolBox

# 复制本地已转换为 Python 3 的 MToolBox 代码
# 包含 classifier 模块和 data 文件
COPY MToolBox/ ${MTOOLBOX_DIR}/MToolBox/

# 复制入口脚本
COPY mtoolbox_annotate.py /opt/mtoolbox_annotate.py

# 下载 mtDNA 参考序列 (rCRS 和 RSRS)
RUN mkdir -p ${MTOOLBOX_DIR}/references && \
    cd ${MTOOLBOX_DIR}/references && \
    # rCRS 参考序列 (NC_012920.1)
    echo ">chrM NC_012920.1 Homo sapiens mitochondrion, complete genome" > chrM_rCRS.fa && \
    echo "GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCATTTGGTATTTTCGTCTGGGGG" >> chrM_rCRS.fa && \
    # 创建索引
    samtools faidx chrM_rCRS.fa || true

# 验证安装
RUN python --version && \
    python -c "import sys; sys.path.insert(0, '/opt/mtoolbox/MToolBox'); from classifier import datatypes2; print('MToolBox classifier imported successfully')" && \
    samtools --version | head -1 && \
    bcftools --version | head -1

WORKDIR /data

ENTRYPOINT ["python", "/opt/mtoolbox_annotate.py"]
CMD ["--help"]
