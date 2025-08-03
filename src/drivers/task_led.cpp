#include <iostream>
#include "middleware/task_log.h"

void task_led(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::LED);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[LED] blink!\n";
    }
}
