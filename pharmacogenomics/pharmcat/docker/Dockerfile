FROM eclipse-temurin:17-jre-jammy

LABEL maintainer="Galaxy Tools"
LABEL version="2.13.0"
LABEL description="PharmCAT - Pharmacogenomics Clinical Annotation Tool"

ENV DEBIAN_FRONTEND=noninteractive
ENV PHARMCAT_VERSION=2.13.0

# 安装依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    bcftools \
    tabix \
    wget \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖（PharmCAT VCF预处理器需要）
RUN pip3 install --no-cache-dir \
    pysam \
    pandas \
    packaging

# 创建PharmCAT目录
RUN mkdir -p /opt/pharmcat/preprocessor

# 下载PharmCAT JAR文件
RUN wget -q "https://github.com/PharmGKB/PharmCAT/releases/download/v${PHARMCAT_VERSION}/pharmcat-${PHARMCAT_VERSION}-all.jar" \
    -O /opt/pharmcat/pharmcat.jar

# 下载并解压VCF预处理器
RUN wget -q "https://github.com/PharmGKB/PharmCAT/releases/download/v${PHARMCAT_VERSION}/pharmcat_vcf_preprocessor-${PHARMCAT_VERSION}.tar.gz" \
    -O /tmp/preprocessor.tar.gz && \
    tar -xzf /tmp/preprocessor.tar.gz -C /opt/pharmcat/preprocessor --strip-components=1 && \
    rm /tmp/preprocessor.tar.gz

# 验证安装
RUN java -jar /opt/pharmcat/pharmcat.jar --version && \
    python3 /opt/pharmcat/preprocessor/pharmcat_vcf_preprocessor.py --help | head -5

# 设置环境变量
ENV PATH="/opt/pharmcat:${PATH}"

WORKDIR /data

# 默认显示帮助
CMD ["java", "-jar", "/opt/pharmcat/pharmcat.jar", "--help"]
