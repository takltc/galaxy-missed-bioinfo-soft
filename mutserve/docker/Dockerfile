# Mutserve Docker Image for Galaxy
# 用于线粒体 DNA (mtDNA) 变异检测，检测同质性 (homoplasmic) 和异质性 (heteroplasmic) 位点
#
# 基于文献调研的最佳实践:
# - Weissensteiner H, et al. (2021) Genome Res - Contamination detection
# - PMID: 33452015, DOI: 10.1101/gr.256545.119
# - Ip EKK, et al. (2022) Front Genet - Benchmark 研究显示 Mutserve 表现最佳
# - PMID: 35350246, DOI: 10.3389/fgene.2022.692257
# - 软件版本: 2.0.0-rc15 (最新稳定版)
#
# 构建说明:
# mutserve 是基于 Java 的工具，需要 JDK 运行环境
# 使用预编译的二进制文件安装

FROM eclipse-temurin:17-jdk-jammy

LABEL maintainer="Omniverse Galaxy Team"
LABEL version="2.0.0-rc15"
LABEL description="Mutserve - 线粒体 DNA 变异检测工具，支持同质性和异质性位点检测"
LABEL citation="Weissensteiner H, et al. Contamination detection in sequencing studies using the mitochondrial phylogeny. Genome Res. 2021;31:309-316."

# 设置非交互模式避免安装时的提示
ENV DEBIAN_FRONTEND=noninteractive
ENV MUTSERVE_VERSION=2.0.0-rc15

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    unzip \
    samtools \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 mutserve
# mutserve 提供预编译的 JAR 包
RUN mkdir -p /opt/mutserve && \
    cd /opt/mutserve && \
    curl -sL https://github.com/seppinho/mutserve/releases/download/v${MUTSERVE_VERSION}/mutserve.zip -o mutserve.zip && \
    unzip mutserve.zip && \
    rm mutserve.zip && \
    chmod +x mutserve

# 下载 rCRS 参考序列 (revised Cambridge Reference Sequence)
# 这是线粒体 DNA 分析的标准参考
RUN mkdir -p /opt/mutserve/reference && \
    curl -sL https://raw.githubusercontent.com/seppinho/mutserve/master/files/rCRS.fasta -o /opt/mutserve/reference/rCRS.fasta && \
    samtools faidx /opt/mutserve/reference/rCRS.fasta

# 下载注释文件
RUN curl -sL https://raw.githubusercontent.com/seppinho/mutserve/master/files/rCRS_annotation_2020-08-20.txt \
    -o /opt/mutserve/reference/rCRS_annotation.txt

# 设置 PATH
ENV PATH="/opt/mutserve:$PATH"

# 验证安装
RUN mutserve --version

# 设置工作目录
WORKDIR /data

# 设置入口点
ENTRYPOINT ["/opt/mutserve/mutserve"]
CMD ["--help"]
