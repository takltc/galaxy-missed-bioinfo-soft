FROM python:3.11-slim

LABEL maintainer="Galaxy PRS Tools"
LABEL description="PRS Risk Interpreter - Interpret PRS percentiles and generate risk categories"
LABEL version="1.0.0"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir numpy pandas

COPY prs_interpreter.py /usr/local/bin/prs_interpreter.py
RUN chmod +x /usr/local/bin/prs_interpreter.py

WORKDIR /data

ENTRYPOINT ["python", "/usr/local/bin/prs_interpreter.py"]
CMD ["--help"]
