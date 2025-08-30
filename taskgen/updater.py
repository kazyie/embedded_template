# --- ここから追記（taskgen/updater.py） ---
import re
from pathlib import Path

def _paths(layer: str, task: str, per: bool):
    """各ファイルパスを返すユーティリティ"""
    low = task.lower()
    inc_dir = Path("include") / layer / (low if per else "")
    src_dir = Path("src") / layer / (low if per else "")
    return inc_dir, src_dir, low, task.upper()

def _events_path(layer: str, task: str, per_task: bool) -> Path:
    low = task.lower()
    return Path("include")/layer/(low if per_task else "")/"events.h"

def append_events(layer: str, task: str, events: list[str], per_task: bool):
    p = _events_path(layer, task, per_task)
    text = p.read_text(encoding="utf-8")

    # enum 本体を抜き出す
    # 例: enum class LEDSEvent { ... };
    m = re.search(r'(enum\s+class\s+([A-Za-z0-9_]+)\s*\{\s*)([^}]*)(\s*\};)', text, flags=re.DOTALL)
    if not m:
        raise SystemExit(f"[append_events] enum block not found in {p}")

    prefix, body, suffix = m.group(1), m.group(3), m.group(4)

    # 既存列挙子（末尾のカンマ/空白除去）
    existing = [s.strip().rstrip(',') for s in body.split(',') if s.strip()]
    existing_set = set(x.upper() for x in existing)

    # 追加候補（大文字化）で重複除外
    adds = []
    for e in events:
        u = e.upper()
        if u not in existing_set:
            adds.append(u)
            existing_set.add(u)

    if not adds:
        print(f"[append_events] no new enums for {layer}:{task}")
        return

    # STOP の前に挿入（なければ末尾に追加）
    if "STOP" in existing:
        stop_idx = existing.index("STOP")
        new_list = existing[:stop_idx] + adds + existing[stop_idx:]
    else:
        new_list = existing + adds

    # 再構築（インデントは 4 スペース固定）
    new_body = "".join(f"    {name},\n" for name in new_list)
    new_text = text[:m.start()] + prefix + new_body + suffix + text[m.end():]

    p.write_text(new_text, encoding="utf-8")
    print(f"[append_events] {p} <- {', '.join(adds)}")

def _dispatch_h_path(layer: str, task: str, per_task: bool) -> Path:
    low = task.lower()
    return Path("include")/layer/(low if per_task else "")/"dispatch.h"

def append_dispatch_rows(layer: str, task: str, events: list[str], per_task: bool,
                         *, null_rows_if_no_stub: bool):
    """dispatch.h のアンカー間にプロトタイプとテーブル行を追加（重複防止）"""
    p = _dispatch_h_path(layer, task, per_task)
    text = p.read_text(encoding="utf-8")

    # 必要なら一度だけアンカーを挿す処理を入れておく（省略可）

    # アンカー抽出
    protos = re.search(r'// AUTOGEN-PROTOS-BEGIN(.*?)// AUTOGEN-PROTOS-END',
                       text, flags=re.DOTALL)
    table  = re.search(r'// AUTOGEN-TABLE-BEGIN(.*?)// AUTOGEN-TABLE-END',
                       text, flags=re.DOTALL)
    if not (protos and table):
        raise SystemExit(f"[append_dispatch_rows] anchors not found in {p}")

    up  = task.upper()
    low = task.lower()

    # 既存の宣言/行の文字列（重複チェック用）
    proto_block = protos.group(1)
    table_block = table.group(1)

    new_protos = []
    new_rows   = []

    for ev in events:
        EVU = ev.upper()
        evl = ev.lower()
        proto_line = (
            f"void on_{low}_{evl}(MessageSystem&, {up}Context&, "
            "const std::vector<std::uint8_t>&);\n"
        )
        if proto_line not in proto_block:
            new_protos.append(proto_line)

        if null_rows_if_no_stub:
            row_line = f"    {{ {up}Event::{EVU}, nullptr }},\n"
        else:
            row_line = f"    {{ {up}Event::{EVU}, &on_{low}_{evl} }},\n"

        if row_line not in table_block:
            new_rows.append(row_line)

    if not new_protos and not new_rows:
        print(f"[append_dispatch_rows] no changes for {layer}:{task}")
        return

    # 置換
    text = (
        text[:protos.start(1)] + proto_block + "".join(new_protos) + text[protos.end(1):]
    )
    # table の方は、STOP を特別扱いしない（events.h 側で制御済み）
    text = (
        text[:table.start(1)] + table_block + "".join(new_rows) + text[table.end(1):]
    )

    p.write_text(text, encoding="utf-8")
    print(f"[append_dispatch_rows] {p} <- {', '.join(events)} "
          f"(rows={'nullptr' if null_rows_if_no_stub else 'fn'})")

def append_handler_stubs(layer: str, task: str, events: list[str], per_task: bool, *, enabled: bool):
    """src/<layer>[/<task>]/handlers.cpp に on_<task>_<event>() のスタブを追記する。
    - layer: 'drivers' / 'middleware' / 'app' など
    - task : タスク名（例: 'led'）※大文字化して <TASK>Context を使う
    - events: 追加するイベント名のリスト（例: ['BLINK', 'BLINK_FAST']）
    - per_task: True のとき src/<layer>/<task>/handlers.cpp、False のとき src/<layer>/handlers.cpp を対象
    - enabled: False のときは何もしない（--handler-skeleton=off 相当）
    """
    if not enabled:
        return

    import re
    from pathlib import Path

    low = task.lower()
    up  = task.upper()

    # handlers.cpp の所在を決定
    src_dir = Path("src") / layer / (low if per_task else "")
    path = src_dir / "handlers.cpp"
    if not path.exists():
        raise SystemExit(f"[add-event] not found: {path}")

    text = path.read_text(encoding="utf-8")
    added: list[str] = []

    # 既存の on_<task>_<event>() がなければ末尾に定義を追記
    for e in (events or []):
        evu = e.upper()
        if evu == "STOP":
            # STOP はディスパッチ終了用・スタブは不要
            continue

        name = f"on_{low}_{e.lower()}"
        # すでに定義があればスキップ
        if re.search(rf'\bvoid\s+{re.escape(name)}\s*\(', text):
            continue

        stub = f"""

void {name}(MessageSystem& /*sys*/, {up}Context& /*ctx*/, const std::vector<std::uint8_t>& /*data*/) {{
    std::printf("[{up}] handle {evu}\\n");
}}
"""
        text += stub
        added.append(evu)

    if added:
        path.write_text(text, encoding="utf-8")
        print(f"[add-event] handler stubs += {added} in {path}")
    else:
        print("[add-event] no handler stubs added (all existed)")


# --- compatibility shim: Makefile is auto-discovered, so this is a no-op.
def update_makefile(tasks, layer, add_io=False, per_task_dir=False, extra_suffixes=None):
    """Kept for backward-compat with cli.py. No-op because SRCS is auto-discovered."""
    return

def _find_message_header():
    """プロジェクト内の message.h の候補を順に探す。"""
    candidates = [
        Path("include/core/message.h"),
        Path("include/middleware/message.h"),
        Path("include/message.h"),
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("message.h が見つかりませんでした: " +
                            ", ".join(str(c) for c in candidates))

def update_message_header(tasks):
    """include/**/message.h の enum class TaskID に tasks を追記する。"""
    if not tasks:
        return
    path = _find_message_header()
    text = path.read_text(encoding="utf-8")

    m = re.search(r'(enum\s+class\s+TaskID\s*\{\s*)([^}]*)(\s*\})',
                  text, flags=re.DOTALL)
    if not m:
        print(f"TaskID enum が見つかりませんでした（{path}）")
        return

    prefix, body, suffix = m.group(1), m.group(2), m.group(3)
    # 既存列挙子を集合化（末尾カンマや空白を正規化）
    existing = {item.strip().rstrip(',') for item in body.split(',') if item.strip()}

    to_add = []
    for t in tasks:
        name = t.upper()
        if name and name not in existing:
            to_add.append(f"    {name},")

    if not to_add:
        print("追加する TaskID はありません。")
        return

    new_body = body.rstrip() + "\n" + "\n".join(to_add) + "\n"
    new_text = text[:m.start(2)] + new_body + text[m.end(2):]
    path.write_text(new_text, encoding="utf-8")
    print(f"TaskID enum に {to_add} を追加しました。（{path}）")

