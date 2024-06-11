# pitch_curve_viewer_backend

ピッチカーブビューアー(https://github.com/laTH380/pitch_curve_viewer) のバックエンドプログラム。

## 機能
- httpでmp3データを受信
- ダウンサンプリング
- 基本周波数推定
- 送り返す

## 謎
- デプロイ時にFFmpegをサーバー環境にインストールさせる方法
- とりあえず対処法：デプロイ後SSHでapt install ffmpegする
