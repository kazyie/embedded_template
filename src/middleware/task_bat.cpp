#include <iostream>
#include "middleware/task_bat.h"

void task_bat(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::BAT);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[BAT] blink!\n";
    }
}
