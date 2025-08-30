#pragma once
#include "core/std_sanity.h"
#include "core/message.h"
#include <cstdint>
#include <utility>
#include <vector>
#include <optional>     // ★ 追加
#include <chrono>       // ★ 追加

template <typename Ev>
class EventIO {
public:
    EventIO(MessageSystem& sys, TaskID self) : sys_(sys), self_(self) {}

    void send(TaskID to, Ev ev, const std::vector<std::uint8_t>& data = {}) {
        Message m;
        m.type  = MessageType::PAYLOAD;
        m.to    = to;
        m.from  = self_;
        m.payload = pack(ev, data);
        sys_.send(to, m);
    }

    std::pair<Ev, std::vector<std::uint8_t>> receive() {
        Message m = sys_.receive(self_);
        auto [ev, data] = unpack(m.payload);
        return {ev, std::move(data)};
    }

    // ★ 追加：タイムアウト付き受信
    std::optional<std::pair<Ev, std::vector<std::uint8_t>>>
    receive_for(std::chrono::milliseconds timeout) {
        Message m;
        if (!sys_.receive_for(self_, m, timeout)) return std::nullopt;
        auto [ev, data] = unpack(m.payload);
        return std::make_optional(std::make_pair(ev, std::move(data)));
    }

    static std::vector<std::uint8_t> pack(Ev ev, const std::vector<std::uint8_t>& data) {
        std::vector<std::uint8_t> buf;
        const std::uint16_t code = static_cast<std::uint16_t>(ev);
        buf.push_back(static_cast<std::uint8_t>(code & 0xFF));
        buf.push_back(static_cast<std::uint8_t>((code >> 8) & 0xFF));
        buf.insert(buf.end(), data.begin(), data.end());
        return buf;
    }

    static std::pair<Ev, std::vector<std::uint8_t>> unpack(const std::vector<std::uint8_t>& buf) {
        if (buf.size() < 2) return {static_cast<Ev>(0), {}};
        std::uint16_t code = static_cast<std::uint16_t>(buf[0]) |
                             (static_cast<std::uint16_t>(buf[1]) << 8);
        std::vector<std::uint8_t> data(buf.begin() + 2, buf.end());
        return {static_cast<Ev>(code), std::move(data)};
    }

private:
    MessageSystem& sys_;
    TaskID self_;
};
