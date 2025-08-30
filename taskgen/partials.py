# taskgen/partials.py
# テンプレの共通断片（パーシャル）

# ── 共通インクルード ──
MAIN_COMMON_INCLUDES = """\
#include <thread>
#include <chrono>
#include <vector>
#include <stop_token>
"""

EVENT_IO_INCLUDE = '#include "core/EventIO.h"'

# ── タスクのヘッダ（最小） ──
TASK_HEADER = """\
#pragma once
#include "core/layer_rules.h"
#include <stop_token>
#include "core/message.h"
void task_{low}(std::stop_token, MessageSystem&);
"""

# ── イベントヘッダ ──
EVENTS_HEADER = """\
#pragma once
#include <cstdint>
#include <vector>
#include "core/message.h"

enum class {UP}Event {{
{EVENT_ENUMS}
}};

struct {UP}Context {{}};
"""

# ── dispatch.h ──
DISPATCH_HEADER = """\
#pragma once
#include <cstddef>
#include <vector>
#include <type_traits>
#include "core/dispatch.h"
#include "{events_hdr_path}"

// --- handler prototypes (autogen) ---
// （add-event が on_{low}_xxx(...) の宣言をここに挿入）
// ※ 名前空間外に置く：既存 handlers.cpp がグローバル定義でもリンク可
// --- handler prototypes end ---

{NS_OPEN}

// core 側の将来の名前空間化に備えて {CORE} 接頭辞を許容（今は "" の想定）
using {UP}DispatchEntry = {CORE}DispatchEntry<{UP}Event, {UP}Context>;
using {UP}HandlerFn     = {CORE}HandlerFn    <{UP}Event, {UP}Context>;

// --- table (autogen) ---
// （add-event は &::on_{low}_xxx を挿れること：グローバル定義を指す）
inline constexpr {UP}DispatchEntry {low}_dispatch_table[] = {{
    {{ static_cast<{UP}Event>(-1), nullptr }}, // sentinel（ゼロ件でも配列サイズを保つ）
}};
// --- table (autogen) end ---

inline constexpr std::size_t {low}_dispatch_count =
    sizeof({low}_dispatch_table) / sizeof({low}_dispatch_table[0]);

inline bool {low}_dispatch(MessageSystem& sys, {UP}Context& ctx,
                           {UP}Event ev, const std::vector<std::uint8_t>& data) {{
    return {CORE}dispatch_table_invoke(sys, ctx, ev, data, {low}_dispatch_table);
}}

// 生成型の健全性チェック
static_assert(std::is_same_v<
    {UP}DispatchEntry, {CORE}DispatchEntry<{UP}Event, {UP}Context>
>);

{NS_CLOSE}
"""

# ── handlers.cpp ──
HANDLERS_SOURCE = """\
#include <cstdio>
#include "{hdr_dir}/dispatch.h"

// 初回は空でOK（add-event --handler-skeleton=on で追記）
// 追記スタブは下記の形：
// void on_{low}_xxx(MessageSystem& sys, {UP}Context& ctx, const std::vector<std::uint8_t>& data) {
//     std::printf("[{UP}] handle XXX\\n");
// }
"""

# ── タスク本体（.gen.cpp） ──
TASK_MAIN = """\
#include <stop_token>
#include "core/dispatch.h"
#include "{events_hdr_path}"
#include "{hdr_dir}/dispatch.h"

void task_{low}(std::stop_token st, MessageSystem& sys) {{
    using namespace {NS};  // ← これで {low}_dispatch_table が見える
    {UP}Context ctx{{}};
    run_task<{UP}Event>(st, sys, TaskID::{UP}, ctx, {low}_dispatch_table);
}}
"""

# ── アプリ main.gen.cpp ──
APP_MAIN = """\
#include <thread>
#include <vector>
#include <chrono>
#include <stop_token>
#include "core/message.h"

{INCLUDES}

int main() {{
    MessageSystem sys;
    std::vector<std::jthread> threads;

{SPAWNS}

    using namespace std::chrono_literals;
    std::this_thread::sleep_for(300ms);
    return 0; // jthread dtor => request_stop + join
}}
"""

# ── テスト（dispatchテーブル検査） ──
TEST_DISPATCH = """\
#include "doctest/doctest.h"
#include "{dispatch_hdr_path}"
#include <unordered_set>

TEST_CASE("{UP} dispatch: table has no duplicate events") {{
    using namespace {NS};
    CHECK({low}_dispatch_count >= 0);
    std::unordered_set<int> seen;
    for (std::size_t i = 0; i < {low}_dispatch_count; ++i) {{
        int key = static_cast<int>({low}_dispatch_table[i].ev);
        CHECK(seen.count(key) == 0);
        seen.insert(key);
        CHECK({low}_dispatch_table[i].fn != nullptr);
    }}
}}
"""

