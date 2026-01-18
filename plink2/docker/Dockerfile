# PLINK2 Docker Image
# 用于 Galaxy 工具的基因型数据质控和PCA分析
FROM continuumio/miniconda3:latest

LABEL maintainer="Galaxy PRS Tools"
LABEL description="PLINK2 - Comprehensive genotype data analysis tool"
LABEL version="2.0"

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 配置 conda channels 并安装 PLINK2
# 注意: 显式指定 Python 3.11 以避免兼容性问题
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y python=3.11 plink2=2.00a5.12 && \
    conda clean -afy

# 验证安装
RUN plink2 --version

# 设置工作目录
WORKDIR /data

# 默认入口点
ENTRYPOINT ["plink2"]
CMD ["--help"]
