# CPIC Interpreter Docker Image
# CPIC guideline-based pharmacogenomics interpretation
# Reference: https://cpicpgx.org/

FROM python:3.11-slim-bullseye

LABEL maintainer="Bioinformatics Team <bio@omniverse.dev>"
LABEL version="1.0.0"
LABEL description="CPIC Interpreter - Clinical Pharmacogenetics Implementation Consortium guideline interpretation"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /opt/cpic-interpreter

# 安装Python依赖
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    jinja2 \
    pyyaml \
    requests \
    jsonschema \
    weasyprint

# 创建数据目录并下载CPIC数据
RUN mkdir -p /opt/cpic-interpreter/data && \
    mkdir -p /opt/cpic-interpreter/templates

# 复制解释器脚本（这里创建一个基础框架）
COPY cpic_interpret.py /opt/cpic-interpreter/
COPY templates/ /opt/cpic-interpreter/templates/

# 设置环境变量
ENV PATH="/opt/cpic-interpreter:${PATH}"
ENV CPIC_DATA="/opt/cpic-interpreter/data"

# 默认入口
ENTRYPOINT ["python", "/opt/cpic-interpreter/cpic_interpret.py"]
CMD ["--help"]
