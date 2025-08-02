#!/usr/bin/env python3
import argparse
from pathlib import Path

# ── ここからテンプレート定義 ──

HEADER_TPL = """\
#ifndef TASK_{UP}_HPP
#define TASK_{UP}_HPP

#include "message.h"

void task_{low}(MessageSystem& sys);

#endif // TASK_{UP}_HPP
"""

SOURCE_TPL = """\
#include <iostream>
#include "task_{low}.h"

void task_{low}(MessageSystem& sys) {{
    Message msg = sys.receive(TaskID::{UP});
    if (msg.type == MessageType::BLINK) {{
        std::cout << "[{UP}] blink!\\n";
    }}
}}
"""

# ── ここまでテンプレート定義 ──


def render(template: str, name: str) -> str:
#処理を書く
    up = name.upper()
    low = name.lower()
    return template.format(UP = up,low = low)

def write_header(low: str, content: str):
    # 1) 出力先ファイルパスを組み立てる
    out_path = Path("include") / f"task_{low}.h"
    
    # 2) 親フォルダがなければ一気に作る
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 3) ファイルに文字列を書き込む
    out_path.write_text(content)

def write_source(low: str, content: str):
    out_path = Path("tasks") / f"task_{low}.cpp"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", nargs="+", required=True)
    args = parser.parse_args()

    for task_name in args.tasks:
        # テンプレートをレンダリング
        hdr = render(HEADER_TPL, task_name)
        src = render(SOURCE_TPL, task_name)

        # ファイルを書き出し
        write_header(task_name, hdr)
        write_source(task_name, src)

if __name__ == "__main__":
    main()