FROM nvidia/cuda:12.1.1-runtime-ubuntu20.04
WORKDIR /workspace

ENV TZ=Asia/Tokyo

RUN apt-get update && \
    apt-get install -y software-properties-common tzdata && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y \
    apt-get install -y libglib2.0-0 python3.10-full python3.10-venv python3-pip git wget curl ffmpeg libsm6 unzip && \
    update-alternatives --install /usr/local/bin/python python /usr/bin/python3.10 1 && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
	ln -sf /usr/bin/python3.10 /usr/bin/python

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["webui"]
