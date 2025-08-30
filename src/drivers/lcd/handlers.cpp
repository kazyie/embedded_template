#include <cstdio>
#include "drivers/lcd/events.h"

void on_lcd_print(MessageSystem& /*sys*/, LCDContext& /*ctx*/, const std::vector<std::uint8_t>& /*data*/) {
    std::printf("[LCD] handle PRINT\n");
}

void on_lcd_clear(MessageSystem& /*sys*/, LCDContext& /*ctx*/, const std::vector<std::uint8_t>& /*data*/) {
    std::printf("[LCD] handle CLEAR\n");
}

void on_lcd_power_on(MessageSystem& /*sys*/, LCDContext& /*ctx*/, const std::vector<std::uint8_t>& /*data*/) {
    std::printf("[LCD] handle POWER_ON\n");
}
