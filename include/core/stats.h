#pragma once
#include <atomic>
#include <cstdint>

struct MsgStats {
    std::atomic<uint64_t> enq{0};      // send() で積んだ数
    std::atomic<uint64_t> deq{0};      // 受信して取り出せた数
    std::atomic<uint64_t> drops{0};    // 将来: 溢れ等で捨てた数（今は未使用）
    std::atomic<uint64_t> timeouts{0}; // receive_for() タイムアウト
};
