#!/usr/bin/env bash

echo -e "[safe]\n  directory = *" > ~/.gitconfig

if [ "$1" = "reinstall" ]; then
    cd /workspace/ComfyUI
    rm -rf venv
fi

cd /workspace
# モデルをダウンロードする
cat ./extensions/extension.json | python3 ./downloader.py
cat ./extensions/controlnet.json | python3 ./downloader.py
cat ./extensions/model.json | python3 ./downloader.py
# web ui dir に移動
cd ./ComfyUI
python3.10 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip wheel
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm5.6
pip install -r requirements.txt

# 起動
python main.py --use-pytorch-cross-attention
