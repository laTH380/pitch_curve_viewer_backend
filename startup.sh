#!/bin/bash

# 必要なパッケージのインストール
apt-get update
apt-get install -y ffmpeg ffprobe

# インストール確認（デバッグ用）
which ffmpeg
which ffprobe
