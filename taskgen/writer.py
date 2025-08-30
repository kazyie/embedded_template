# writer.py
from pathlib import Path
from typing import Optional


# ─────────────────────────────
# internal helpers
# ─────────────────────────────
def _hdr_dir(layer: str, low: str, per_task: bool) -> Path:
    """
    include/<layer>[/<task>]
    """
    base = Path("include") / layer
    return base / low if per_task else base


def _src_dir(layer: str, low: str, per_task: bool) -> Path:
    """
    src/<layer>[/<task>]
    """
    base = Path("src") / layer
    return base / low if per_task else base


def _ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def _safe_write(path: Path, content: str, overwrite: bool = False, quiet: bool = False) -> None:
    """
    既存ファイルがあり overwrite=False のときは何もしない。
    """
    _ensure_parent(path)
    if path.exists() and not overwrite:
        if not quiet:
            print(f"[SKIP] {path} (exists)")
        return
    path.write_text(content, encoding="utf-8")
    if not quiet:
        print(f"[GEN]  {path}")


# ─────────────────────────────
# public writers (headers / sources)
# ─────────────────────────────
def write_header(name: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    task ヘッダ: include/<layer>[/<task>]/task_<task>.h
    """
    low = name.lower()
    out = _hdr_dir(layer, low, per_task) / f"task_{low}.h"
    _safe_write(out, content, overwrite=overwrite)


def write_events_header(name_or_low: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    events ヘッダ: include/<layer>[/<task>]/events.h
    """
    low = name_or_low.lower()
    out = _hdr_dir(layer, low, per_task) / "events.h"
    _safe_write(out, content, overwrite=overwrite)


def write_dispatch_header(name_or_low: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    dispatch ヘッダ（テーブル定義を含む）: include/<layer>[/<task>]/dispatch.h
    """
    low = name_or_low.lower()
    out = _hdr_dir(layer, low, per_task) / "dispatch.h"
    _safe_write(out, content, overwrite=overwrite)


def write_handlers_source(name: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    handlers 実装: src/<layer>[/<task>]/handlers.cpp
    """
    low = name.lower()
    out = _src_dir(layer, low, per_task) / "handlers.cpp"
    _safe_write(out, content, overwrite=overwrite)


def write_task_main(name: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    タスクのエントリ（受信ループ）: src/<layer>[/<task>]/task_<task>_main.gen.cpp
    """
    low = name.lower()
    out = _src_dir(layer, low, per_task) / f"task_{low}_main.gen.cpp"
    _safe_write(out, content, overwrite=overwrite)


def write_app_main(content: str, *, overwrite: bool = True) -> None:
    """
    アプリ側のメイン: src/app/main.gen.cpp
    生成物は常に上書きする運用が多いので overwrite=True を既定に。
    """
    out = Path("src/app/main.gen.cpp")
    _safe_write(out, content, overwrite=overwrite)


# ─────────────────────────────
# IO（必要なら使用）※現状はヘッダ完結想定
# ─────────────────────────────
def write_io_header(name_or_low: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    IO ヘッダ: include/<layer>[/<task>]/task_<task>_io.h
    """
    low = name_or_low.lower()
    out = _hdr_dir(layer, low, per_task) / f"task_{low}_io.h"
    _safe_write(out, content, overwrite=overwrite)


def write_io_source(name_or_low: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    IO 実装: src/<layer>[/<task>]/task_<task>_io.cpp
    ※ 現在は未使用（ヘッダ完結）。後方互換で残す。
    """
    low = name_or_low.lower()
    out = _src_dir(layer, low, per_task) / f"task_{low}_io.cpp"
    _safe_write(out, content, overwrite=overwrite)


# ─────────────────────────────
# 互換用（旧アーキで使っていたAPI）
# ─────────────────────────────
def write_source(name_or_low: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    旧: src/<layer>[/<task>]/task_<task>.cpp
    新アーキでは生成しない想定。互換のため残す。
    """
    low = name_or_low.lower()
    out = _src_dir(layer, low, per_task) / f"task_{low}.cpp"
    _safe_write(out, content, overwrite=overwrite)


def write_dispatch_source(name: str, content: str, layer: str, per_task: bool, *, overwrite: bool = False) -> None:
    """
    【非推奨／後方互換】旧: src/<layer>[/<task>]/dispatch.cpp
    新アーキでは dispatch.h に集約。呼ばれても一応生成はする。
    """
    low = name.lower()
    out = _src_dir(layer, low, per_task) / "dispatch.cpp"
    _safe_write(out, content, overwrite=overwrite)


# ─────────────────────────────
# tests
# ─────────────────────────────
def write_test_dispatch(name_or_low: str, content: str, *, overwrite: bool = False) -> None:
    """
    tests/test_<task>_dispatch.cpp
    既定では上書きしない（手編集が入る可能性があるため）。
    """
    low = name_or_low.lower()
    out = Path("tests") / f"test_{low}_dispatch.cpp"
    _safe_write(out, content, overwrite=overwrite)
