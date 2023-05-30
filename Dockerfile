FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04
WORKDIR /workspace

ENV TZ=Asia/Tokyo
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get install -y libglib2.0-0 python3.10-full python3.10-venv python3-pip git wget curl ffmpeg libsm6 unzip && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["webui"]
