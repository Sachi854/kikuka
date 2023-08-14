#!/usr/bin/env bash

echo -e "[safe]\n  directory = *" > ~/.gitconfig

if [ "$1" = "reinstall" ]; then
    cd /workspace/ComfyUI
    rm -rf venv
fi

cd /workspace
# 最新のリポジトリに更新する
git pull
git submodule foreach git pull origin master
# モデルをダウンロードする
cat ./extensions/custom_nodes.json | python3 ./downloader.py
cat ./extensions/controlnet_fp16.json | python3 ./downloader.py
cat ./extensions/models.json | python3 ./downloader.py
# web ui dir に移動
cd ./ComfyUI
python3.10 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip wheel
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118 xformers
pip install -r requirements.txt

# 起動
python main.py
