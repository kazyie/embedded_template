# Embedded Template & TaskGen
![CI](https://github.com/kazyie/embedded_template/actions/workflows/ci.yml/badge.svg)

> VS Code + WSL 上で動く、組み込みテンプレートと Python タスクジェネレータのサンプルプロジェクト
---
## 🎯 目的
- 組み込み風のマルチタスク C++ テンプレートを素早く作成  
- `taskgen.py` でタスク雛形（ヘッダー／ソース）を自動生成  
## ⚙️ 前提環境
- Windows 10/11 + WSL2（Ubuntu）  
- VS Code（Remote-WSL 拡張インストール済み）  
- Python 3.x（仮想環境推奨）  
- g++ (C++17)  
## 🚀 セットアップ

1. **クローン & WSL/仮想環境**  
   ```bash
   git clone https://github.com/kazyie/embedded_template.git
   cd embedded_template
   python3 -m venv .venv
   source .venv/bin/activate
## 🚀 セットアップ手順

## 🚀 Getting Started

1. リポジトリをクローン  
   ```bash
   git clone https://github.com/kazyie/embedded_template.git
   cd embedded_template

    Python 仮想環境の作成 & 有効化

python3 -m venv .venv
source .venv/bin/activate

開発モードでパッケージをインストール

pip install -e .

タスクひな形を生成

# middleware層に led, uart, log を生成
taskgen -l middleware -t led uart log

※ 直接スクリプトを呼ぶ場合：

./taskgen.py -l middleware --tasks led uart log -r

(-lはlayerを意味しており、--tasksは追加するcppと.hの名前)
C++テンプレートをビルド & 実行
(-rをつけると実行される仕組みになっている)



