#include <stop_token>
#include "core/dispatch.h"
#include "middleware/mw_hub/events.h"
#include "middleware/mw_hub/dispatch.h"

void task_mw_hub(std::stop_token st, MessageSystem& sys) {
    MW_HUBContext ctx{};
    run_task<MW_HUBEvent>(st, sys, TaskID::MW_HUB, ctx, mw_hub_dispatch_table);
}
