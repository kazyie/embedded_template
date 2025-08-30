#pragma once
#include <cstddef>
#include <vector>
#include "core/dispatch.h"
#include "drivers/led/events.h"

using LEDDispatchEntry = DispatchEntry<LEDEvent, LEDContext>;
using LEDHandlerFn     = HandlerFn    <LEDEvent, LEDContext>;

// --- handler prototypes (autogen) ---
// （add-event が on_led_xxx(...) の宣言をここに挿入）
// --- handler prototypes end ---

inline constexpr LEDDispatchEntry led_dispatch_table[] = {
    // --- table (autogen) ---
    { static_cast<LEDEvent>(-1), nullptr }, // sentinel（ゼロ件でも配列サイズを保つ）
    // --- table (autogen) end ---
};

inline constexpr std::size_t led_dispatch_count =
    sizeof(led_dispatch_table) / sizeof(led_dispatch_table[0]);

inline bool led_dispatch(MessageSystem& sys, LEDContext& ctx,
                           LEDEvent ev, const std::vector<std::uint8_t>& data) {
    return dispatch_table_invoke(sys, ctx, ev, data, led_dispatch_table);
}