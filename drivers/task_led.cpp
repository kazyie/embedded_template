#include <iostream>
#include "task_led.h"

void task_led(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::LED);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[LED] blink!\n";
    }
}
