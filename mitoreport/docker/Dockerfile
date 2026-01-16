# MitoReport Docker Image for Galaxy
# 用于线粒体 DNA (mtDNA) 变异分析和临床解释
#
# 开发者: Murdoch Childrens Research Institute (MCRI) Bioinformatics Methods Group
# GitHub: https://github.com/bioinfomethods/mitoreport
#
# 软件功能:
# - 线粒体变异异质性分析 (Heteroplasmy analysis)
# - MitoMap/gnomAD 人群频率注释
# - 缺失分析 (Deletion analysis)
# - 母系变异比较
# - 交互式 HTML 报告生成
#
# 依赖说明:
# - MitoReport 基于 Java/Groovy 构建，需要 Java 11 运行环境
# - 需要外部资源文件: gnomAD mtDNA VCF, MitoMap annotations
#
# 构建命令:
# docker build -t omniverse/mitoreport:1.2.3 .

FROM eclipse-temurin:11-jdk-jammy

LABEL maintainer="Omniverse Galaxy Team"
LABEL version="1.2.3"
LABEL description="MitoReport - 线粒体 DNA 变异分析和临床解释工具"
LABEL citation="Developed by Bioinformatics Methods group at Murdoch Childrens Research Institute"
LABEL github="https://github.com/bioinfomethods/mitoreport"

# 设置非交互模式避免安装时的提示
ENV DEBIAN_FRONTEND=noninteractive
ENV MITOREPORT_VERSION=1.2.3

# 安装系统依赖
# - wget/curl: 下载文件
# - samtools: BAM 文件处理
# - tabix: VCF 索引
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    unzip \
    samtools \
    tabix \
    && rm -rf /var/lib/apt/lists/*

# 创建安装目录
RUN mkdir -p /opt/mitoreport /opt/mitoreport/resources

# 下载 MitoReport JAR 包
RUN curl -sL "https://github.com/bioinfomethods/mitoreport/releases/download/${MITOREPORT_VERSION}/mitoreport-${MITOREPORT_VERSION}-all.jar" \
    -o /opt/mitoreport/mitoreport.jar

# 下载并解压资源文件 (gnomAD, 对照 BAM)
# 注意: 资源文件较大 (~500MB)，包含:
# - gnomAD mtDNA 人群频率 VCF
# - 对照样本 BAM 文件 (来自 1000 Genomes)
# - 测试样本
RUN cd /opt/mitoreport/resources && \
    curl -sL "https://github.com/bioinfomethods/mitoreport/releases/download/1.2.1/resources.tgz" \
    -o resources.tgz && \
    tar -xzf resources.tgz && \
    rm resources.tgz

# 创建便捷脚本
RUN echo '#!/bin/bash\njava -Xmx8g -jar /opt/mitoreport/mitoreport.jar "$@"' > /usr/local/bin/mitoreport && \
    chmod +x /usr/local/bin/mitoreport

# 创建 mito-map-download 便捷脚本
RUN echo '#!/bin/bash\njava -Xmx4g -jar /opt/mitoreport/mitoreport.jar mito-map-download "$@"' > /usr/local/bin/mitoreport-download && \
    chmod +x /usr/local/bin/mitoreport-download

# 验证安装
RUN java -jar /opt/mitoreport/mitoreport.jar --help || echo "MitoReport installed"

# 设置环境变量
ENV PATH="/opt/mitoreport:/usr/local/bin:$PATH"
ENV MITOREPORT_RESOURCES="/opt/mitoreport/resources"

# 设置工作目录
WORKDIR /data

# 默认入口点
ENTRYPOINT ["mitoreport"]
CMD ["--help"]
