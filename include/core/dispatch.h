// include/core/dispatch.h
#pragma once
#include <cstddef>
#include <cstdint>
#include <stop_token>

// あなたが定義した型エイリアス（Bytes, Millis）を読み込む
// 例: Bytes = std::vector<std::uint8_t>, Millis = std::chrono::milliseconds
#include "core/types.h"

#include "core/EventIO.h"

// 循環 include 回避のための前方宣言
struct MessageSystem;
enum class TaskID : int;

// 汎用ディスパッチ・エントリ
template<class Event, class Ctx>
using HandlerFn = void(*)(MessageSystem&, Ctx&, const Bytes&);

template<class Event, class Ctx>
struct DispatchEntry {
    Event                 ev{};
    HandlerFn<Event, Ctx> fn{};
};

// テーブル実行（見つかったら true）
template<class Event, class Ctx, std::size_t N>
inline bool dispatch_table_invoke(MessageSystem& sys, Ctx& ctx, Event ev,
                                  const Bytes& data,
                                  const DispatchEntry<Event, Ctx> (&table)[N]) {
    for (const auto& row : table) {
        if (row.fn && row.ev == ev) { row.fn(sys, ctx, data); return true; }
    }
    return false;
}

// 汎用タスクループ（Event/Ctx だけテンプレ化。配列型/長さは引数から推論）
// poll 間隔は Millis で指定（デフォルト 100ms）
template<class Event, class Ctx, std::size_t N>
inline void run_task(std::stop_token st, MessageSystem& sys, TaskID id,
                     Ctx& ctx, const DispatchEntry<Event, Ctx> (&table)[N],
                     Millis poll = Millis{100}) {
    EventIO<Event> io(sys, id);
    while (!st.stop_requested()) {
        if (auto evt = io.receive_for(poll)) {
            auto& [ev, data] = *evt;
            (void)dispatch_table_invoke(sys, ctx, ev, data, table);
        }
    }
}
