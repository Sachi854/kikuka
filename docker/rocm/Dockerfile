FROM rocm/dev-ubuntu-22.04:5.6-complete
WORKDIR /workspace
 
ENV TZ=Asia/Tokyo
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get update && \
    apt-get install -y python3.10-full python3.10-dev python3.10-venv python3-pip git wget curl ffmpeg unzip build-essential pkg-config libcairo2-dev libjpeg-dev libgif-dev libglib2.0-0 libsm6 && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
