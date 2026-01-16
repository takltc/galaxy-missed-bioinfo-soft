# MitoZ Docker 镜像
# 线粒体基因组组装、注释和可视化工具包
# 版本: 3.6
# 参考: https://github.com/linzhi2013/MitoZ

FROM continuumio/miniconda3:latest

LABEL maintainer="Galaxy Tools"
LABEL version="3.6"
LABEL description="MitoZ: A toolkit for animal mitochondrial genome assembly, annotation and visualization"
LABEL doi="10.1093/nar/gkz173"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# 配置 conda channels 并安装 MitoZ
# 注意: 显式指定 Python 版本避免兼容性问题 (MitoZ 需要 Python >=3.6, <3.9)
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y python=3.8 mitoz=3.6 && \
    conda clean -afy

# 验证安装
RUN mitoz --version && \
    mitoz all --help | head -20

# 初始化 NCBI Taxonomy 数据库 (ETE3 需要)
# 这个步骤在首次运行时会自动执行，但预先初始化可以加速首次运行
RUN python -c "from ete3 import NCBITaxa; ncbi = NCBITaxa()" || echo "NCBI Taxonomy 数据库将在首次运行时自动下载"

WORKDIR /data

ENTRYPOINT ["mitoz"]
CMD ["--help"]
