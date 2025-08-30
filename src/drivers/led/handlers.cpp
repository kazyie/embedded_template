#include <cstdio>
#include "drivers/led/events.h"

void on_led_blink(MessageSystem& /*sys*/, LEDContext& /*ctx*/,
                  const std::vector<std::uint8_t>& /*data*/) {
    std::printf("[LED] BLINK\n\n");
}
