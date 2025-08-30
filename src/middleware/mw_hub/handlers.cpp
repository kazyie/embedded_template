// src/middleware/mw_hub/handlers.cpp
#include <cstdio>
#include "middleware/mw_hub/events.h"
#include "drivers/drv_hub/events.h"
#include "core/EventIO.h"

void on_mw_hub_req_led_on(MessageSystem& sys, MW_HUBContext&, const std::vector<uint8_t>&) {
    EventIO<DRV_HUBEvent> out(sys, TaskID::MW_HUB);
    out.send(TaskID::DRV_HUB, DRV_HUBEvent::TO_LED);
}

void on_mw_hub_req_lcd_print(MessageSystem& sys, MW_HUBContext&, const std::vector<uint8_t>& data) {
    EventIO<DRV_HUBEvent> out(sys, TaskID::MW_HUB);
    out.send(TaskID::DRV_HUB, DRV_HUBEvent::TO_LCD, data);
}

void on_mw_hub_req_uart_send(MessageSystem& sys, MW_HUBContext&, const std::vector<uint8_t>& data) {
    EventIO<DRV_HUBEvent> out(sys, TaskID::MW_HUB);
    out.send(TaskID::DRV_HUB, DRV_HUBEvent::TO_UART, data);
}
