#include <stop_token>
#include "core/dispatch.h"
#include "drivers/drv_hub/events.h"
#include "drivers/drv_hub/dispatch.h"
#include "core/dispatch.h"

void task_drv_hub(std::stop_token st, MessageSystem& sys) {
    DRV_HUBContext ctx{};
    run_task<DRV_HUBEvent>(st, sys, TaskID::DRV_HUB, ctx, drv_hub_dispatch_table);
}