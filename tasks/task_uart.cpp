#include <iostream>
#include "task_uart.h"

void task_uart(MessageSystem &sys)
{
    Message msg = sys.receive(TaskID::UART);
    if (msg.type == MessageType::DATA)
    {
        std::cout << "[UART] HELLO\n";
    }
}
