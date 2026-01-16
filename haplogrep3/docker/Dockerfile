# Haplogrep3 Docker Image
# 线粒体 DNA 单倍群分类工具
# 
# 版本: 3.2.2
# 论文: DOI 10.1093/nar/gkad284
# GitHub: https://github.com/genepi/haplogrep3

FROM eclipse-temurin:17-jre-jammy

LABEL maintainer="Galaxy Tools"
LABEL version="3.2.2"
LABEL description="Haplogrep3 - Free mtDNA Haplogroup Classification Service"
LABEL citation="Schönherr S, et al. Nucleic Acids Res. 2023. doi:10.1093/nar/gkad284"

ENV DEBIAN_FRONTEND=noninteractive
ENV HAPLOGREP_VERSION=3.2.2

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Haplogrep3
WORKDIR /opt/haplogrep3

RUN wget -q "https://github.com/genepi/haplogrep3/releases/download/v${HAPLOGREP_VERSION}/haplogrep3-${HAPLOGREP_VERSION}-linux.zip" \
    && unzip "haplogrep3-${HAPLOGREP_VERSION}-linux.zip" \
    && rm "haplogrep3-${HAPLOGREP_VERSION}-linux.zip" \
    && chmod +x haplogrep3

# 添加到 PATH
ENV PATH="/opt/haplogrep3:${PATH}"

# 验证安装 (默认已包含 PhyloTree 17 rCRS/RSRS 和 Forensic Update)
RUN haplogrep3 trees

# 安装额外的系统发育树版本
RUN ./haplogrep3 install-tree phylotree-rcrs@16.0 || true

WORKDIR /data

ENTRYPOINT ["haplogrep3"]
CMD ["--help"]
