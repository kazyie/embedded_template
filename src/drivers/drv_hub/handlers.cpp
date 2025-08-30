#include <vector>
#include "drivers/drv_hub/events.h"
#include "drivers/led/events.h"
#include "middleware/uart/events.h"
#include "core/EventIO.h"
#include <cstdio>

void on_drv_hub_to_led(MessageSystem& sys, DRV_HUBContext&, const std::vector<std::uint8_t>&) {
    EventIO<LEDEvent> led(sys, TaskID::DRV_HUB);
    // 以前の LEDEvent::TURN_ON → 現在の BLINK に合わせる
    led.send(TaskID::LED, LEDEvent::BLINK);
}

void on_drv_hub_to_uart(MessageSystem& sys, DRV_HUBContext&, const std::vector<std::uint8_t>& data) {
    EventIO<UARTEvent> uart(sys, TaskID::DRV_HUB);
    // 以前の UARTEvent::SEND_PRINT → 現在の SEND_HEX に合わせる
    uart.send(TaskID::UART, UARTEvent::SEND_HEX, data);
}
