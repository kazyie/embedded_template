#include "middleware/message.h"

void MessageSystem::send(TaskID to, const Message& msg) {
    {
        std::lock_guard<std::mutex> lock(mtx_);
        queues_[to].push(msg);
    }
    cv_.notify_all();
}

Message MessageSystem::receive(TaskID tid) {
    std::unique_lock<std::mutex> lock(mtx_);
    cv_.wait(lock, [&]{ return !queues_[tid].empty(); });
    Message msg = queues_[tid].front();
    msg.from = tid;
    queues_[tid].pop();
    return msg;
}
