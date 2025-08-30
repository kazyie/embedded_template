#pragma once
#include <cstddef>
#include <vector>
#include <type_traits>            // ← 追加
#include "core/dispatch.h"        // ← ここ超重要
#include "drivers/lcd/events.h"

using LCDDispatchEntry = DispatchEntry<LCDEvent, LCDContext>;
using LCDHandlerFn     = HandlerFn    <LCDEvent, LCDContext>;

// 型がズレていないかの保険（ビルド時のみ・コストゼロ）
static_assert(std::is_same_v<
    LCDDispatchEntry, DispatchEntry<LCDEvent, LCDContext>
>, "LCDDispatchEntry must match DispatchEntry<LCDEvent, LCDContext>");

#ifdef DEMO_LCD_ASSERT
// デモ用：型が一致していたら“わざと”落とす
static_assert(!std::is_same_v<
    LCDDispatchEntry, DispatchEntry<LCDEvent, LCDContext>
>, "DEMO: static_assert が効いていて、型一致を検出できています（このメッセージが出たらデモ成功）");
#endif


// --- handler prototypes (autogen) ---
// （add-event が on_lcd_xxx(...) の宣言をここに挿入）
// --- handler prototypes end ---

inline constexpr LCDDispatchEntry lcd_dispatch_table[] = {
    { static_cast<LCDEvent>(-1), nullptr }, // sentinel
};

inline constexpr std::size_t lcd_dispatch_count =
    sizeof(lcd_dispatch_table) / sizeof(lcd_dispatch_table[0]);

inline bool lcd_dispatch(MessageSystem& sys, LCDContext& ctx,
                         LCDEvent ev, const std::vector<std::uint8_t>& data) {
    return dispatch_table_invoke(sys, ctx, ev, data, lcd_dispatch_table);
}
