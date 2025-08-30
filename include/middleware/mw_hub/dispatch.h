#pragma once
#include <cstddef>
#include <vector>
#include "middleware/mw_hub/events.h"
#include "core/dispatch.h"

using MW_HUBDispatchEntry = DispatchEntry<MW_HUBEvent, MW_HUBContext>;
using MW_HUBHandlerFn     = HandlerFn    <MW_HUBEvent, MW_HUBContext>;

// --- handler prototypes (autogen) ---
// （add-event が on_mw_hub_xxx(...) の宣言をここに挿入）
// --- handler prototypes end ---

inline constexpr MW_HUBDispatchEntry mw_hub_dispatch_table[] = {
    // --- table (autogen) ---
    { static_cast<MW_HUBEvent>(-1), nullptr }, // sentinel（ゼロ件でも配列サイズを保つ）
    // --- table (autogen) end ---
};

inline constexpr std::size_t mw_hub_dispatch_count =
    sizeof(mw_hub_dispatch_table) / sizeof(mw_hub_dispatch_table[0]);

inline bool mw_hub_dispatch(MessageSystem& sys, MW_HUBContext& ctx,
                           MW_HUBEvent ev, const std::vector<std::uint8_t>& data) {
    return dispatch_table_invoke(sys, ctx, ev, data, mw_hub_dispatch_table);
}