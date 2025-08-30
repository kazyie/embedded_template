#include "core/message.h"
#include "core/log.h"

void MessageSystem::send(TaskID to, const Message& in) {
    Message m = in;
    m.to = to;  // 念のため上書き
    {
        std::lock_guard<std::mutex> lock(mtx_);
        queues_[to].push(std::move(m));  // to 用のキューへ
        stats_.enq.fetch_add(1, std::memory_order_relaxed);   // ★追加
    }
    cv_.notify_one(); // 待ってる受信者を1つ起こす（複数同時なら notify_all でもOK）
     LOG_DEBUG("send to=%d type=%d", (int)to, (int)m.type);
}

Message MessageSystem::receive(TaskID tid) {
    std::unique_lock<std::mutex> lock(mtx_);
    cv_.wait(lock, [this, tid]{
        auto it = queues_.find(tid);
        return it != queues_.end() && !it->second.empty();
    });
    Message m = std::move(queues_[tid].front());
    queues_[tid].pop();
    stats_.deq.fetch_add(1, std::memory_order_relaxed);          // ★追加
    LOG_DEBUG("recv (blocking) for=%d type=%d", (int)tid, (int)m.type);
    return m;
}

// ★ 追加
bool MessageSystem::receive_for(TaskID tid, Message& out,
                                std::chrono::milliseconds timeout) {
    std::unique_lock<std::mutex> lock(mtx_);
    bool ready = cv_.wait_for(lock, timeout, [&]{ return !queues_[tid].empty(); });
    if (!ready) return false;
    out = queues_[tid].front();
    queues_[tid].pop();
    return true;
}