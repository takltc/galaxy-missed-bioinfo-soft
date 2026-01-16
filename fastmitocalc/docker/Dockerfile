# fastMitoCalc Docker Image
# 用于从全基因组测序数据估算线粒体DNA拷贝数
#
# 构建命令: docker build -t omniverse/fastmitocalc:1.0.0 .
# 测试命令: docker run --rm omniverse/fastmitocalc:1.0.0 perl /opt/fastMitoCalc/fastMitoCalc.pl

FROM continuumio/miniconda3:24.1.2-0

LABEL maintainer="Galaxy Tools <galaxy@omniverse.com>"
LABEL version="1.0.0"
LABEL description="fastMitoCalc: ultra-fast mtDNA copy number estimation from WGS data"
LABEL doi="10.1093/bioinformatics/btx167"

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:/opt/fastMitoCalc:$PATH"

# 安装系统依赖
# g++: 编译 BaseCoverage.cpp
# perl: 运行 fastMitoCalc.pl
# samtools: BAM 文件处理
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    perl \
    wget \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安装 samtools (用于 BAM 索引验证和处理)
RUN conda config --add channels defaults && \
    conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    conda install -y python=3.11 samtools=1.21 && \
    conda clean -afy

# 克隆 fastMitoCalc 仓库
RUN git clone https://github.com/qian0001/fastMitoCalc.git /opt/fastMitoCalc

# 修复原始脚本中的 $filename 变量未声明 bug (应为 $bamfile)
RUN sed -i 's/\$filename/\$bamfile/g' /opt/fastMitoCalc/fastMitoCalc.pl

# 编译 BaseCoverage
WORKDIR /opt/fastMitoCalc
RUN g++ -O2 -o BaseCoverage BaseCoverage.cpp

# 验证安装
RUN perl fastMitoCalc.pl 2>&1 | head -5 || true
RUN ./BaseCoverage 2>&1 | head -3 || true
RUN samtools --version | head -1

# 设置工作目录
WORKDIR /data

# 默认入口点
ENTRYPOINT ["perl", "/opt/fastMitoCalc/fastMitoCalc.pl"]
CMD ["--help"]
