FROM --platform=linux/amd64 python:3.11-slim

LABEL maintainer="Galaxy Tools"
LABEL version="1.0.0"
LABEL description="HLA Disease Association: Analyze HLA-disease and drug risk associations"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 --version

WORKDIR /data

ENTRYPOINT ["python3"]
CMD ["--version"]
