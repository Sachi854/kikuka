# README
Stable Diffusion web UI の環境構築及びモデルのダウンロードとUIの実行を行うスクリプト群です。

# Quick Start

## pre-requirements
CUDA/git/Nvida Docker 2

## Nvidia Docker 2
初回実行

```bash
git clone --recursive https://github.com/Sachi854/kukuri.git
cd kukuri
# 大量のダウンロードが発生するため時間がかかります。
sudo docker compose up init
```

2回目以降

```bash
cd kukuri
sudo docker compose up
```

## Native
初回実行

```bash
git clone --recursive https://github.com/Sachi854/kukuri.git
cd kukuri
./setup.sh init
```

2回目以降

```bash
cd kukuri
./setup.sh
```

# Tips

## ダウンロードするモデルや拡張機能を変更したい場合
extensions/model.json を編集してください。
