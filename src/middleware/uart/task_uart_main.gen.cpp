#include <stop_token>
#include "core/dispatch.h"
#include "middleware/uart/events.h"
#include "middleware/uart/dispatch.h"

void task_uart(std::stop_token st, MessageSystem& sys) {
    UARTContext ctx{};
    run_task<UARTEvent>(st, sys, TaskID::UART, ctx, uart_dispatch_table);
}