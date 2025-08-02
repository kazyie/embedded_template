# Embedded Template & TaskGen

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
## 🚀 セットアップ手順
## 🚀 Getting Started
1. リポジトリをクローン  
   ```bash
   git clone https://github.com/kazyie/embedded_template.git
   cd embedded_template
2. Python 仮想環境の作成 & 有効化

   python3 -m venv .venv
   source .venv/bin/activate

3. タスクひな形を生成
   ./taskgen.py --tasks led uart log

4. C++テンプレートをビルド、実行
   make
   ./app
=> [LED] blink!



