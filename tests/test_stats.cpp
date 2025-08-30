#include "doctest/doctest.h"
#include "core/message.h"

TEST_CASE("MessageSystem stats increase on send/receive") {
    MessageSystem sys;

    // 送信 → 受信の最小ケース
    Message m; m.type = MessageType::DATA; m.to = TaskID::LED; m.from = TaskID::UART;
    sys.send(TaskID::LED, m);

    Message got = sys.receive(TaskID::LED);
    CHECK(got.type == MessageType::DATA);

   const auto& st = sys.stats();  // ← 参照で受ける
   CHECK(st.enq.load() >= 1);
   CHECK(st.deq.load() >= 1);
}
