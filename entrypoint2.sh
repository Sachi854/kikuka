#!/usr/bin/env bash

echo -e "[safe]\n  directory = *" > ~/.gitconfig

if [ "$1" = "init" ]; then
    cd /workspace
    # モデルをダウンロードする
    cat ./extensions/base.json | python3 ./downloader.py
    cat ./extensions/model.json | python3 ./downloader.py
    # web ui dir に移動
    cd ./stable-diffusion-webui
    python3.10 -m venv venv
    source venv/bin/activate
    python -m pip install --upgrade pip wheel
    # requirements_versions.txt の内容をインストール
    # torch 2.0 を先に入れる
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
    pip install -r requirements_versions.txt
fi

cd /workspace/stable-diffusion-webui

if [ "$1" = "reinstall" ]; then
    rm -rf venv
    python3.10 -m venv venv
    source venv/bin/activate
    python -m pip install --upgrade pip wheel
    # requirements_versions.txt の内容をインストール
    # torch 2.0 を先に入れる
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
    pip install -r requirements_versions.txt
fi

mkdir -p /workspace/stable-diffusion-webui/tfchache
# 起動オプション
export TORCH_COMMAND="pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2"
export REQS_FILE="requirements_versions.txt"
export COMMANDLINE_ARGS="--deepdanbooru --theme dark --upcast-sampling --opt-sdp-no-mem-attention"
export TRANSFORMERS_CACHE="/workspace/stable-diffusion-webui/tfchache"

# web ui の実行
source venv/bin/activate
python launch.py
