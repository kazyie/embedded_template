#include <iostream>
#include "drivers/task_bar.h"

void task_bar(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::BAR);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[BAR] blink!\n";
    }
}
