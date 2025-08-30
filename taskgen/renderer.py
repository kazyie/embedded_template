# taskgen/renderer.py
from typing import List

def render(template: str, name: str, layer: str, per_task: bool=False, events=None) -> str:
    up, low = name.upper(), name.lower()
    hdr_dir = f"{layer}/{low}" if per_task else f"{layer}"
    events = list(events or [])
    has_stop = any(e.lower()=="stop" for e in events)
    enum_events = events + ([] if has_stop else ["STOP"])
    enum_lines = [f"    {e.upper()}," for e in (enum_events or ["STOP"])]

    return template.format(
        UP=up, low=low, layer=layer,
        hdr_dir=hdr_dir,
        events_hdr_path=f"{hdr_dir}/events.h",
        EVENT_ENUMS="\n".join(enum_lines),
    )



def render_app_main(template: str, pairs: list[tuple[str, str]], per_task: bool=False) -> str:
    incs, spawns = [], []
    for layer, name in pairs:
        low = name.lower()
        hdr_dir = f"{layer}/{low}" if per_task else f"{layer}"
        incs.append(f'#include "{hdr_dir}/task_{low}.h"')
        spawns.append(f'    threads.emplace_back(task_{low}, std::ref(sys));')
    return template.format(INCLUDES="\n".join(incs), SPAWNS="\n".join(spawns))
    
