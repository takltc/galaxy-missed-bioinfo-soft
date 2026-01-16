# ExpansionHunter Denovo Docker Image for Galaxy
# 用于检测短串联重复序列 (STR) 的新型扩增
#
# 基于文献调研的最佳实践:
# - Dolzhenko et al. (2020) Genome Biology - 原始论文
# - PMID: 32345345, DOI: 10.1186/s13059-020-02017-z
# - 软件版本: 0.9.0 (最新稳定版)
#
# 构建说明:
# expansionhunterdenovo 依赖 backports.lzma，该包仅支持 Python 3.6-3.9
# 因此需要创建独立的 conda 环境并指定 Python 3.9

FROM continuumio/miniconda3:24.1.2-0

LABEL maintainer="Omniverse Galaxy Team"
LABEL version="0.9.0"
LABEL description="ExpansionHunter Denovo - 短串联重复序列新型扩增检测工具"
LABEL citation="Dolzhenko E, et al. ExpansionHunter Denovo: a computational method for locating known and novel repeat expansions in short-read sequencing data. Genome Biol. 2020;21(1):102."

# 设置非交互模式避免安装时的提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    libcurl4-openssl-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# 配置 conda channels
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority flexible

# 创建独立环境，指定 Python 3.9 以满足 backports.lzma 依赖
# expansionhunterdenovo 0.9.0 依赖 backports.lzma，仅支持 Python <=3.9
RUN conda create -n ehdn python=3.9 \
        expansionhunterdenovo=0.9.0 \
        samtools \
    -y && \
    conda clean -afy

# 激活环境并设置 PATH
ENV PATH="/opt/conda/envs/ehdn/bin:$PATH"
ENV CONDA_DEFAULT_ENV=ehdn

# 验证安装
RUN ExpansionHunterDenovo --version && \
    samtools --version | head -1

# 设置工作目录
WORKDIR /data

# 设置入口点 - 使用完整路径确保正确的环境
ENTRYPOINT ["/opt/conda/envs/ehdn/bin/ExpansionHunterDenovo"]
CMD ["--help"]
