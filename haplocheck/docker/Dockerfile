# Haplocheck Docker Image for Galaxy
# 用于 mtDNA 和 WGS 测序研究中的样本内污染检测
#
# 基于文献调研的最佳实践:
# - Weissensteiner H, et al. (2021) Genome Res - Contamination detection
# - PMID: 33452015, DOI: 10.1101/gr.256545.119
# - García-Olivares V, et al. (2021) Sci Rep - Haplocheck 在 WGS 和 WES 中表现最佳
# - PMID: 34654896, DOI: 10.1038/s41598-021-99895-5
# - 软件版本: 1.3.3 (最新稳定版)
#
# 构建说明:
# haplocheck 是基于 Java 的工具，需要 JDK 运行环境
# VCF 模式使用预编译的二进制文件

FROM eclipse-temurin:17-jdk-jammy

LABEL maintainer="Omniverse Galaxy Team"
LABEL version="1.3.3"
LABEL description="Haplocheck - 基于线粒体系统发育的污染检测工具，支持 mtDNA 和 WGS 研究"
LABEL citation="Weissensteiner H, et al. Contamination detection in sequencing studies using the mitochondrial phylogeny. Genome Res. 2021;31:309-316."

# 设置非交互模式避免安装时的提示
ENV DEBIAN_FRONTEND=noninteractive
ENV HAPLOCHECK_VERSION=1.3.3

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 haplocheck
# haplocheck 提供预编译的 ZIP 包，包含可执行脚本
RUN mkdir -p /opt/haplocheck && \
    cd /opt/haplocheck && \
    curl -sL https://github.com/genepi/haplocheck/releases/download/v${HAPLOCHECK_VERSION}/haplocheck.zip -o haplocheck.zip && \
    unzip haplocheck.zip && \
    rm haplocheck.zip && \
    chmod +x haplocheck

# 设置 PATH
ENV PATH="/opt/haplocheck:$PATH"

# 验证安装
RUN haplocheck --version

# 设置工作目录
WORKDIR /data

# 设置入口点
ENTRYPOINT ["/opt/haplocheck/haplocheck"]
CMD ["--help"]
