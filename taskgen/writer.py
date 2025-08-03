# taskgen/writer.py
from pathlib import Path

def write_header(low: str, content: str, layer: str):
    # 1) 出力先ファイルパスを組み立てる
    out_path = Path("include") / layer / f"task_{low}.h"
    # 2) 親フォルダがなければ一気に作る
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # 3) ファイルに文字列を書き込む
    out_path.write_text(content)

def write_source(low: str, content: str, layer: str):
    out_path = Path("src") / layer / f"task_{low}.cpp"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content)