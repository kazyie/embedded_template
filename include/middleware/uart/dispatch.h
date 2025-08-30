
#pragma once
#include <cstddef>
#include <vector>
#include "core/dispatch.h"
#include "middleware/uart/events.h"

using UARTDispatchEntry = DispatchEntry<UARTEvent, UARTContext>;
using UARTHandlerFn     = HandlerFn    <UARTEvent, UARTContext>;

// --- handler prototypes (autogen) ---
// （add-event が on_uart_xxx(...) の宣言をここに挿入）
// --- handler prototypes end ---

inline constexpr UARTDispatchEntry uart_dispatch_table[] = {
    // --- table (autogen) ---
    { static_cast<UARTEvent>(-1), nullptr }, // sentinel（ゼロ件でも配列サイズを保つ）
    // --- table (autogen) end ---
};

inline constexpr std::size_t uart_dispatch_count =
    sizeof(uart_dispatch_table) / sizeof(uart_dispatch_table[0]);

inline bool uart_dispatch(MessageSystem& sys, UARTContext& ctx,
                           UARTEvent ev, const std::vector<std::uint8_t>& data) {
    return dispatch_table_invoke(sys, ctx, ev, data, uart_dispatch_table);
}