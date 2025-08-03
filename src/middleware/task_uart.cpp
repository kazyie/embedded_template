#include <iostream>
#include "middleware/task_uart.h"

void task_uart(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::UART);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[UART] blink!\n";
    }
}
