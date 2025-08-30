#include <stop_token>
#include "core/dispatch.h"
#include "drivers/led/events.h"
#include "drivers/led/dispatch.h"
#include "core/dispatch.h"

void task_led(std::stop_token st, MessageSystem& sys) {
    LEDContext ctx{};
    run_task<LEDEvent>(st, sys, TaskID::LED, ctx, led_dispatch_table);
}