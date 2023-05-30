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
    pip install clean-fid numba numpy torch==2.0.0+cu118 torchvision --extra-index-url https://download.pytorch.org/whl/cu118
    pip install -r requirements_versions.txt
fi

cd /workspace/stable-diffusion-webui
# 起動オプション
export TORCH_COMMAND="pip install torch==2.0.0 torchvision --extra-index-url https://download.pytorch.org/whl/cu118"
export REQS_FILE="requirements_versions.txt"
export COMMANDLINE_ARGS="--deepdanbooru --theme dark --opt-channelslast --opt-sdp-no-mem-attention"

# web ui の実行
source venv/bin/activate
python launch.py
