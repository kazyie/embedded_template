#include <iostream>
#include "middleware/task_lcd.h"

void task_lcd(MessageSystem& sys) {
    Message msg = sys.receive(TaskID::LCD);
    if (msg.type == MessageType::BLINK) {
        std::cout << "[LCD] blink!\n";
    }
}
