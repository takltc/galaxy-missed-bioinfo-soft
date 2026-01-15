# GangSTR Docker Image
# 用于 Galaxy 工具的全基因组 STR 分析
FROM continuumio/miniconda3:latest

LABEL maintainer="Galaxy STR Tools"
LABEL description="GangSTR - Genome-wide tandem repeat profiling tool"
LABEL version="2.5.0"

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 配置 conda channels 并安装 GangSTR
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y gangstr=2.5.0 && \
    conda clean -afy

# 验证安装
RUN GangSTR --version

# 设置工作目录
WORKDIR /data

# 默认入口点
ENTRYPOINT ["GangSTR"]
CMD ["--help"]
