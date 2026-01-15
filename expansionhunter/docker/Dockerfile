# ExpansionHunter Docker Image
# 用于 Galaxy 工具的 STR 扩展检测
FROM continuumio/miniconda3:latest

LABEL maintainer="Galaxy STR Tools"
LABEL description="ExpansionHunter - STR expansion detection tool"
LABEL version="5.0.0"

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:$PATH"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 配置 conda channels 并安装 ExpansionHunter
# 注意: expansionhunter 需要 Python 3.8-3.12，miniconda3:latest 默认 Python 3.13 不兼容
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y python=3.11 expansionhunter=5.0.0 libboost && \
    conda clean -afy

# 验证安装
RUN ExpansionHunter --version

# 设置工作目录
WORKDIR /data

# 默认入口点
ENTRYPOINT ["ExpansionHunter"]
CMD ["--help"]
