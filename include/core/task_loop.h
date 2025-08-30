#pragma once
#include <stop_token>
#include <chrono>
#include "core/dispatch.h"
#include "core/EventIO.h"

template<class Event, class Ctx, class Entry, std::size_t N>
inline void run_task(std::stop_token st, MessageSystem& sys, TaskID id,
                     Ctx& ctx, const Entry (&table)[N]) {
    using namespace std::chrono_literals;
    EventIO<Event> io(sys, id);
    while (!st.stop_requested()) {
        if (auto evt = io.receive_for(100ms)) {
            auto [ev, data] = *evt;
            for (const auto& row : table) {
                if (row.fn && row.ev == ev) { row.fn(sys, ctx, data); break; }
            }
        }
    }
}
