#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include "core/message.h"
#include "core/EventIO.h"
#include <chrono>

TEST_CASE("MessageSystem basic send/receive") {
    MessageSystem sys;
    Message m;
    m.type = MessageType::PAYLOAD;
    m.to   = TaskID::LED;   // 手元の enum を適当に利用
    m.from = TaskID::UART;
    m.payload = {1,2,3};
    sys.send(TaskID::LED, m);

    auto got = sys.receive(TaskID::LED);
    CHECK(got.type == MessageType::PAYLOAD);
    CHECK(got.from == TaskID::UART);
    CHECK(got.payload.size() == 3);
}

TEST_CASE("receive_for times out when no message") {
    MessageSystem sys;
    Message out;
    using namespace std::chrono_literals;
    bool ok = sys.receive_for(TaskID::LCD, out, 20ms);
    CHECK_FALSE(ok);
}

enum class TESTEv : uint16_t { A = 1, B = 2 };

TEST_CASE("EventIO pack/unpack") {
    MessageSystem sys;
    EventIO<TESTEv> tx(sys, TaskID::UART), rx(sys, TaskID::LED);
    tx.send(TaskID::LED, TESTEv::B, {9,9});
    auto [ev, data] = rx.receive();
    CHECK(ev == TESTEv::B);
    REQUIRE(data.size() == 2);
    CHECK(data[0] == 9);
    CHECK(data[1] == 9);
}
