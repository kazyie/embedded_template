#taskgen/updater.py
from pathlib import Path
import re

def update_makefile(tasks: str,layer: str):
    with open("Makefile", "r+", encoding="UTF-8") as f:
        content = f.read()

        pos = content.find("SRCS =")
        end = content.find("\n", pos)
        srcstext = content[pos + 7:end].strip()
        srcname = srcstext.split()

        for task in tasks:
            if not any(task in cmakename for cmakename in srcname):
                insert_line = f" src/{layer}/task_{task}.cpp\n"
                content = content[:end] + insert_line + content[end:]
                end += len(insert_line)

        # ✅ ← for文の外、でも with の中！
        f.seek(0)
        f.write(content)
        f.truncate()

def update_message_header(tasks: list[str]):
    # 1) ファイルを読み込む
    path = Path("include/middleware/message.h")
    text = path.read_text(encoding="utf-8")

    # 2) enum 本体を探す
    #    キャプチャ: { ... } 全体と、中の要素リスト
    m = re.search(
        r'(enum\s+class\s+TaskID\s*\{\s*)([^}]*)(\s*\})',
        text, flags=re.DOTALL
    )
    if not m:
        print("TaskID enum が見つかりませんでした。")
        return

    prefix, body, suffix = m.group(1), m.group(2), m.group(3)
    # 既存の要素をリスト化（カンマ区切り／改行スペースをトリム）
    existing = {item.strip().rstrip(',') for item in body.split(',') if item.strip()}

    # 3) 追加分だけをリストアップ
    to_add = []
    for t in tasks:
        name = t.upper()
        if name not in existing:
            to_add.append(f"    {name},")  #enum 内の書式に合わせる

    if not to_add:
        print("追加する TaskID はありません。")
        return

    # 4) 新しい enum 本体を組み立て
    new_body = body.rstrip() + "\n" + "\n".join(to_add) + "\n"
    new_enum = prefix + new_body + suffix

    # 5) テキスト全体を書き換え
    new_text = text[:m.start()] + new_enum + text[m.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"TaskID enum に {to_add} を追加しました。")