#taskgen/runner.py
import subprocess

def run_if_requested(run_flag: bool):
    if run_flag:
        subprocess.run(["make"], check=True)
        subprocess.run(["./app"], check=True)