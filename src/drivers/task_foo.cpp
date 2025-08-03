#include <iostream>
#include "drivers/task_foo.h"

void task_foo(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::FOO);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[FOO] blink!\n";
    }
}
