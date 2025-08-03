# taskgen/cli.py
import argparse
from .templates import HEADER_TPL, SOURCE_TPL
from .renderer import render
from .writer import write_header, write_source
from .updater import update_makefile, update_message_header
from .runner import run_if_requested

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--layer", "-l",
        choices=["app", "middleware", "drivers"],
        required=True,
        help="output layer/directory"
    )
    parser.add_argument(
        "--tasks", "-t",
        nargs="+",
        required=True,
        help="list of task names"
    )
    parser.add_argument(
        "--run", "-r",
        action="store_true",
        help="generate, build and run"
    )
    args = parser.parse_args()
    layer = args.layer
    tasks = args.tasks

    for task_name in tasks:
        hdr = render(HEADER_TPL, task_name, layer)
        src = render(SOURCE_TPL, task_name, layer)
        write_header(task_name, hdr, layer)
        write_source(task_name, src, layer)

    update_makefile(tasks, layer)
    update_message_header(tasks)
    run_if_requested(args.run)