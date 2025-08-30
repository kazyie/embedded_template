#!/usr/bin/env python3
import argparse
import itertools
import os

from .templates import (
    HEADER_TPL,
    EVENTS_HEADER_TPL,
    DISPATCH_HEADER_TPL,      # ← header-only dispatcher
    HANDLERS_SOURCE_TPL,      # ← スタブ生成用（任意）
    TASK_MAIN_TPL,
    APP_MAIN_TPL,
    TEST_DISPATCH_TPL,        # ← 任意：テスト雛形
)
from .renderer import render, render_app_main
from .runner import run_if_requested
from .writer import (
    write_header,
    write_events_header,
    write_dispatch_header,
    write_handlers_source,
    write_task_main,
    write_app_main,
    write_test_dispatch,
)
from .updater import update_message_header   # TaskID 追加だけ残す


# ---- ユーティリティ ---------------------------------------------------------

def _hdr_dir(layer: str, task: str, per_task: bool) -> str:
    return f"include/{layer}/{task}" if per_task else f"include/{layer}"

def _src_dir(layer: str, task: str, per_task: bool) -> str:
    return f"src/{layer}/{task}" if per_task else f"src/{layer}"


def ensure_task_exists(layer: str, task: str, per_task: bool, *, events=None) -> bool:
    """
    既存のタスクに不足物があれば“治す”。無ければ一式を新規生成する。
      - include/<layer>/<task>/task_<task>.h
      - include/<layer>/<task>/events.h
      - include/<layer>/<task>/dispatch.h   （ヘッダ完結で constexpr テーブル）
      - src/<layer>/<task>/task_<task>_main.gen.cpp
      - src/<layer>/<task>/handlers.cpp      （必要なら / 初回のみ）
    """
    from pathlib import Path
    low = task.lower()

    hdr_dir = _hdr_dir(layer, low, per_task)
    src_dir = _src_dir(layer, low, per_task)

    hdr_path     = Path(hdr_dir) / f"task_{low}.h"
    events_path  = Path(hdr_dir) / "events.h"
    disp_h_path  = Path(hdr_dir) / "dispatch.h"
    handlers_cpp = Path(src_dir) / "handlers.cpp"
    main_gen_cpp = Path(src_dir) / f"task_{low}_main.gen.cpp"

    evs = list(events or [])
    created_any = False

    # 1) 必要なソース文字列を一括レンダリング
    hdr_txt     = render(HEADER_TPL,          task, layer, per_task)
    events_txt  = render(EVENTS_HEADER_TPL,   task, layer, per_task, events=evs)
    dispatch_h  = render(DISPATCH_HEADER_TPL, task, layer, per_task, events=evs)
    main_txt    = render(TASK_MAIN_TPL,       task, layer, per_task)
    # handlers は events が無くても“空実装”を書けるテンプレの想定
    handlers_txt= render(HANDLERS_SOURCE_TPL, task, layer, per_task, events=evs)

    # 2) なければ作る（上書きはしない）
    if not hdr_path.exists():
        write_header(task, hdr_txt, layer, per_task); created_any = True
    if not events_path.exists():
        write_events_header(task, events_txt, layer, per_task); created_any = True
    if not disp_h_path.exists():
        # アンカー入り dispatch.h（ヘッダ完結）
        write_dispatch_header(task, dispatch_h, layer, per_task); created_any = True
    if not main_gen_cpp.exists():
        write_task_main(task, main_txt, layer, per_task); created_any = True
    if not handlers_cpp.exists():
        # 初回だけスタブを作る（以降は add-event の --handler-skeleton=on で増やす）
        write_handlers_source(task, handlers_txt, layer, per_task); created_any = True

    if created_any:
        # TaskID enum を自動追記
        update_message_header([task])

    return created_any


# ---- 引数パーサ -------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="taskgen")
    sub = p.add_subparsers(dest="cmd")

    # 通常生成（サブコマンド無し）
    p.add_argument("--layer", "-l", choices=["app", "middleware", "drivers"], required=False)
    p.add_argument("--tasks", "-t", nargs="+", required=False)
    p.add_argument("--events", "-e", nargs="+")
    p.add_argument("--per-task-dir", "-p", action="store_true")
    p.add_argument("--run", "-r", action="store_true")
    p.add_argument("--gen-tests", action="store_true",
                   help="generate tests/test_<task>_dispatch.cpp")
    p.add_argument("--gen-main", action="store_true",
                   help="generate src/app/main.gen.cpp that spawns threads")
    p.add_argument("--spawn", "-s", nargs="+", action="append",
                   help="tasks to spawn; repeatable: -s drivers:lcd -s middleware:uart")

    # add-event
    add = sub.add_parser("add-event", help="append events & dispatch rows to an existing task (header-only)")
    add.add_argument("--layer","-l", choices=["app","middleware","drivers"], required=True)
    add.add_argument("--task","-t", required=True)
    add.add_argument("--events","-e", nargs="+", required=True)
    add.add_argument("--per-task-dir","-p", action="store_true")
    add.add_argument("--handler-skeleton", choices=["on","off"], default="on",
                     help="also append handler stubs to handlers.cpp (default: on)")

    return p


# ---- メイン -----------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()

    # add-event モード
    if args.cmd == "add-event":
        from .updater import append_events, append_dispatch_rows, append_handler_stubs

        layer = args.layer
        task  = args.task
        evs   = args.events
        per   = args.per_task_dir
        make_stubs = (args.handler_skeleton != "off")

        # events.h の enum 追記
        append_events(layer, task, evs, per)

        # dispatch.h のプロトタイプ & テーブル行をアンカーに追記
        # skeleton=off のときは {EV, nullptr} を挿入（安全）
        append_dispatch_rows(layer, task, evs, per,
                             null_rows_if_no_stub=(not make_stubs))

        # 必要なら handlers.cpp にスタブ追加
        append_handler_stubs(layer, task, evs, per_task, enabled=make_stubs)

        print(f"[add-event] {layer}:{task} <- {', '.join(evs)} "
              f"(stubs={'on' if make_stubs else 'off'})")
        return

    # 通常生成 / gen-main
    layer    = args.layer
    tasks    = args.tasks
    per_task = args.per_task_dir
    events   = args.events or []

    # 通常生成の必須チェック
    if not args.gen_main and (not layer or not tasks):
        parser.error("--layer/-l と --tasks/-t は必須です（または add-event を使ってください）")

    # 1) タスク生成
    if tasks:
        for t in tasks:
            ensure_task_exists(layer, t, per_task, events=events)
            if args.gen_tests:
                test_src = render(TEST_DISPATCH_TPL, t, layer, per_task)
                write_test_dispatch(t.lower(), test_src)

    # 2) main.gen.cpp 生成
    if args.gen_main:
        spawn_specs = list(itertools.chain.from_iterable(args.spawn or []))  # ['drivers:lcd', ...]
        if spawn_specs:
            pairs = []
            for spec in spawn_specs:
                try:
                    ly, tk = spec.split(":", 1)
                except ValueError:
                    raise SystemExit(f"Bad -s spec: {spec} (expected layer:task)")
                pairs.append((ly, tk))
        else:
            if not (layer and tasks):
                parser.error("--gen-main 単独の場合は -s layer:task か --layer+--tasks を指定してください")
            pairs = [(layer, t) for t in tasks]

        # 生成対象が未作成なら先に作る
        for ly, tk in pairs:
            ensure_task_exists(ly, tk, per_task, events=None)

        app_main_src = render_app_main(APP_MAIN_TPL, pairs, per_task)
        write_app_main(app_main_src)

    # 3) 実行
    run_if_requested(args.run)


if __name__ == "__main__":
    main()
