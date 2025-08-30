#include <stop_token>
#include "core/dispatch.h"
#include "drivers/lcd/events.h"
#include "drivers/lcd/dispatch.h"
#include <type_traits>

void task_lcd(std::stop_token st, MessageSystem& sys) {
    LCDContext ctx{};
    run_task<LCDEvent>(st, sys, TaskID::LCD, ctx, lcd_dispatch_table);
}
