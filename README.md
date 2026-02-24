# 🗾 Traveled Japan - Interactive Travel Map

訪問した都道府県を可視化するインタラクティブ日本地図です。

Python（Folium）でGeoJSONデータから地図HTMLを生成し、  
JavaScriptで検索・モーダル表示・動的UI機能を実装しています。

🔗 Live Demo  
https://miraikami111.github.io/visited_japan/

---

## 🎯 Project Concept

アナログの「スクラッチ世界地図」をデジタルで再現したいと思い制作しました。  
趣味をベースにしながらも、軽量性とUI体験を意識した設計を行っています。

---

## 🌟 Features

- 🗺 GeoJSONを用いたインタラクティブ日本地図
- 🟢 訪問済み都道府県の動的色変更
- 🖱 ホバー時のツールチップ表示
- 🖼 クリックでアルバムモーダル表示
- 🔍 #タグ検索機能（2文字以上で候補表示）
- ✨ 一致タグのリアルタイムハイライト
- 📊 訪問率（％表示）の自動計算
- 💾 localStorageによる状態保存
- ⚡ 軽量設計（必要時のみ画像読み込み）

---

## 🛠 Tech Stack

### Programming Languages
- Python
- JavaScript
- HTML / CSS

### Library / Data
- Folium（Python地図描画ライブラリ）
- GeoJSON（地理データ形式）
- localStorage（ブラウザ保存機能）

---

### 処理の流れ

1. GeoJSONを読み込み
2. Python（Folium）で日本地図HTMLを生成
3. JavaScriptで検索・モーダル・動的UIを追加
4. GitHub Pagesで静的Webアプリとして公開


## 🚀 How to Run (Local)

```bash
python visited_japan.py
python -m http.server 8000
