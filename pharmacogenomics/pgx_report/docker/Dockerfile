# PGx Report Generator Docker Image
# Comprehensive pharmacogenomics clinical report generation
# Integrates CPIC, DPWG, and PharmCAT outputs

FROM python:3.11-slim-bullseye

LABEL maintainer="Bioinformatics Team <bio@omniverse.dev>"
LABEL version="1.0.0"
LABEL description="PGx Report Generator - Comprehensive pharmacogenomics clinical report generation"

# 安装系统依赖（包括WeasyPrint所需的库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    jq \
    # WeasyPrint依赖
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    # 字体支持
    fonts-liberation \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /opt/pgx-report

# 安装Python依赖
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    jinja2 \
    pyyaml \
    requests \
    jsonschema \
    weasyprint \
    markdown \
    pygments

# 创建目录结构
RUN mkdir -p /opt/pgx-report/data && \
    mkdir -p /opt/pgx-report/templates && \
    mkdir -p /opt/pgx-report/static

# 复制报告生成器脚本
COPY pgx_report_generate.py /opt/pgx-report/
COPY templates/ /opt/pgx-report/templates/
COPY static/ /opt/pgx-report/static/

# 设置环境变量
ENV PATH="/opt/pgx-report:${PATH}"
ENV PGX_REPORT_DATA="/opt/pgx-report/data"
ENV PGX_REPORT_TEMPLATES="/opt/pgx-report/templates"

# 默认入口
ENTRYPOINT ["python", "/opt/pgx-report/pgx_report_generate.py"]
CMD ["--help"]
