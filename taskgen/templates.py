# taskgen/templates.py

HEADER_TPL = """\
#ifndef TASK_{UP}_H
#define TASK_{UP}_H

#include "middleware/message.h"

void task_{low}(MessageSystem& sys);

#endif // TASK_{UP}_H
"""

SOURCE_TPL = """\
#include <iostream>
#include "{layer}/task_{low}.h"

void task_{low}(MessageSystem& sys) {{
    Message msg = sys.receive(TaskID::{UP});
    if (msg.type == MessageType::BLINK) {{
        std::cout << "[{UP}] blink!\\n";
    }}
}}
"""