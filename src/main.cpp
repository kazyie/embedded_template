#include <thread>
#include "message.h"
#include "task_led.h"
#include "task_uart.h"

int main() {
    MessageSystem sys;
    // LEDタスクを起動
    std::thread ledThread(task_led, std::ref(sys));
    std::thread uartThread(task_uart, std::ref(sys));
    // メッセージ送信
    Message msgLed;
    Message msgUart;
    msgLed.type = MessageType::BLINK;
    msgUart.type = MessageType::DATA;
    sys.send(TaskID::LED, msgLed);
    sys.send(TaskID::UART, msgUart);
    ledThread.join();
    uartThread.join();
    return 0;
}