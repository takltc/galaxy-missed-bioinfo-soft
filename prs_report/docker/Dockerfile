FROM python:3.11-slim

LABEL maintainer="Galaxy PRS Tools"
LABEL description="PRS Report Generator - Generate HTML reports and radar charts"
LABEL version="1.0.0"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir numpy pandas matplotlib jinja2

COPY prs_report.py /usr/local/bin/prs_report.py
COPY report_template.html /usr/local/share/prs_report/report_template.html
RUN chmod +x /usr/local/bin/prs_report.py

WORKDIR /data

ENTRYPOINT ["python", "/usr/local/bin/prs_report.py"]
CMD ["--help"]
