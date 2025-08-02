#include <iostream>
#include "task_log.h"

void task_log(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::LOG);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[LOG] blink!\n";
    }
}
