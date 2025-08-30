#pragma once
#include "core/std_sanity.h"
#include <mutex>
#include <condition_variable>
#include <queue>
#include <map>
#include <vector>
#include <cstdint>
#include <chrono>   // ★ 追加
#include "core/stats.h"
#include "core/log.h"

enum class TaskID {
    APP,
    DRV_HUB,
    LCD,
    LED,
    MW_HUB,
    TEST,
    TEST_IO,
    UART,
};

enum class MessageType { NONE, BLINK, DATA, PAYLOAD };

struct Message {
    MessageType type = MessageType::NONE;
    TaskID to;
    TaskID from;
    std::vector<std::uint8_t> payload;
};

class MessageSystem {
public:
    void send(TaskID to, const Message& msg);
    Message receive(TaskID tid);

    // ★ 追加：タイムアウト付き受信（成功なら true）
    bool receive_for(TaskID tid, Message& out,
                     std::chrono::milliseconds timeout);
    
    const MsgStats& stats() const { return stats_; }

private:
    std::mutex mtx_;
    std::condition_variable cv_;
    std::map<TaskID, std::queue<Message>> queues_;
    MsgStats stats_;
};
