#pragma once
#include <cstddef>
#include <vector>
#include "core/dispatch.h"
#include "drivers/drv_hub/events.h"

using DRV_HUBDispatchEntry = DispatchEntry<DRV_HUBEvent, DRV_HUBContext>;
using DRV_HUBHandlerFn     = HandlerFn    <DRV_HUBEvent, DRV_HUBContext>;

// --- handler prototypes (autogen) ---
// （add-event が on_drv_hub_xxx(...) の宣言をここに挿入）
// --- handler prototypes end ---

inline constexpr DRV_HUBDispatchEntry drv_hub_dispatch_table[] = {
    // --- table (autogen) ---
    { static_cast<DRV_HUBEvent>(-1), nullptr }, // sentinel（ゼロ件でも配列サイズを保つ）
    // --- table (autogen) end ---
};

inline constexpr std::size_t drv_hub_dispatch_count =
    sizeof(drv_hub_dispatch_table) / sizeof(drv_hub_dispatch_table[0]);

inline bool drv_hub_dispatch(MessageSystem& sys, DRV_HUBContext& ctx,
                           DRV_HUBEvent ev, const std::vector<std::uint8_t>& data) {
    return dispatch_table_invoke(sys, ctx, ev, data, drv_hub_dispatch_table);
}