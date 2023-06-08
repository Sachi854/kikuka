# README
Stable Diffusion web UI の環境構築及びモデルのダウンロードとUIの実行を行うスクリプト群です。

# Quick Start

## pre-requirements
CUDA11.8/git/Nvida Docker 2/ROCm5.4.2

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
git submodule update --recursive --remote
sudo docker compose up web
```

## ROCm Docker

初回実行

```bash
git clone --recursive https://github.com/Sachi854/kukuri.git
cd kukuri
# 大量のダウンロードが発生するため時間がかかります。
sudo docker compose up init2
```

2回目以降

```bash
cd kukuri
git submodule update --recursive --remote
sudo docker compose up web2
```

# Tips

## ダウンロードするモデルや拡張機能を変更したい場合
extensions/model.json を編集してください。

## WSL2のネットワークが遅い場合
https://qiita.com/bioflowy/items/02c9e945439a2d032cd2

powershellを管理者権限で実行し、以下のコマンドを実行してください。

```powershell
Set-NetAdapterAdvancedProperty -InterfaceDescription 'Hyper-V Virtual Ethernet Adapter' -DisplayName 'Large Send Offload Version 2 (IPv4)' -DisplayValue 'Disabled' -IncludeHidden
Set-NetAdapterAdvancedProperty -InterfaceDescription 'Hyper-V Virtual Ethernet Adapter' -DisplayName 'Large Send Offload Version 2 (IPv6)' -DisplayValue 'Disabled' -IncludeHidden
```

## Deploy ROCm Docker containers

https://rocm.docs.amd.com/en/latest/deploy/docker.html

## PyTorch

https://pytorch.org
