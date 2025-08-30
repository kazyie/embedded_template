// include/middleware/TaskIO.h
#pragma once
#include <vector>
#include <cstdint>
#include "message.h"

template<typename T>
std::vector<std::uint8_t> serialize(const T&);

template<typename T>
T deserialize(const std::vector<std::uint8_t>&);

template<typename Payload>
class TaskIO {
public:
    TaskIO(MessageSystem& sys, TaskID self) : sys_(sys), self_(self) {}

    void send(TaskID to, const Payload& data) {
        Message msg;
        msg.type    = MessageType::PAYLOAD;        // ← message.h に PAYLOAD を追加してあること
        msg.payload = serialize<Payload>(data);    // ← テンプレート呼び出しOK
        sys_.send(to, msg);
    }

    Payload receive() {
        Message msg = sys_.receive(self_);
        return deserialize<Payload>(msg.payload);  // ← テンプレート呼び出しOK
    }

private:
    MessageSystem& sys_;
    TaskID         self_;
};
