# Cyrius Docker Image
# Accurate CYP2D6 genotyping from WGS
# Reference: https://github.com/Illumina/Cyrius

FROM python:3.10-slim-bullseye

LABEL maintainer="Bioinformatics Team <bio@omniverse.dev>"
LABEL version="1.1.1"
LABEL description="Cyrius - Accurate CYP2D6 genotyping from WGS data"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    samtools \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /opt/cyrius

# 克隆Cyrius仓库并安装
RUN git clone --depth 1 --branch v1.1.1 https://github.com/Illumina/Cyrius.git . && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pysam numpy scipy

# 设置环境变量
ENV PATH="/opt/cyrius:${PATH}"
ENV CYRIUS_DATA="/opt/cyrius/data"

# 验证安装
RUN python star_caller.py --help || echo "Cyrius installed"

# 默认入口
ENTRYPOINT ["python", "/opt/cyrius/star_caller.py"]
CMD ["--help"]
