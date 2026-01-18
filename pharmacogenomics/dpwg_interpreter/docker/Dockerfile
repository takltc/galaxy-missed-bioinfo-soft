# DPWG Interpreter Docker Image
# Dutch Pharmacogenetics Working Group guideline interpretation
# Reference: https://www.pharmgkb.org/page/dpwg

FROM python:3.11-slim-bullseye

LABEL maintainer="Bioinformatics Team <bio@omniverse.dev>"
LABEL version="1.0.0"
LABEL description="DPWG Interpreter - Dutch Pharmacogenetics Working Group guideline interpretation"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /opt/dpwg-interpreter

# 安装Python依赖
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    jinja2 \
    pyyaml \
    requests \
    jsonschema

# 创建数据目录
RUN mkdir -p /opt/dpwg-interpreter/data && \
    mkdir -p /opt/dpwg-interpreter/templates

# 复制解释器脚本
COPY dpwg_interpret.py /opt/dpwg-interpreter/
COPY templates/ /opt/dpwg-interpreter/templates/

# 设置环境变量
ENV PATH="/opt/dpwg-interpreter:${PATH}"
ENV DPWG_DATA="/opt/dpwg-interpreter/data"

# 默认入口
ENTRYPOINT ["python", "/opt/dpwg-interpreter/dpwg_interpret.py"]
CMD ["--help"]
