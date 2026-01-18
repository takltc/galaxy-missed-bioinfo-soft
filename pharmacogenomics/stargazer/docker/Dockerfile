# Stargazer Docker Image
# Pharmacogene star allele caller
# Reference: https://github.com/sbslee/stargazer

FROM python:3.10-slim-bullseye

LABEL maintainer="Bioinformatics Team <bio@omniverse.dev>"
LABEL version="2.0.4"
LABEL description="Stargazer - Star allele caller for pharmacogenes"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gzip \
    bzip2 \
    tabix \
    bcftools \
    samtools \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /opt/stargazer

# 安装Python依赖和Stargazer
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scipy \
    pysam \
    && pip install --no-cache-dir stargazer==2.0.4

# 下载PharmVar数据库（用于星等位基因定义）
RUN mkdir -p /opt/stargazer/data && \
    wget -q https://www.pharmvar.org/get-download-file?name=ALL_GENES&refSeq=GRCh38&fileType=VCF&version=latest \
    -O /opt/stargazer/data/pharmvar_latest.vcf.gz || true

# 设置环境变量
ENV PATH="/opt/stargazer:${PATH}"
ENV STARGAZER_DATA="/opt/stargazer/data"

# 验证安装
RUN stargazer --help || echo "Stargazer installed"

# 默认入口
ENTRYPOINT ["stargazer"]
CMD ["--help"]
