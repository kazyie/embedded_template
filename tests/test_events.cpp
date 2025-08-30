#include "doctest/doctest.h"
#include "drivers/led/dispatch.h"

TEST_CASE("LED dispatch table compiles") {
    CHECK(led_dispatch_count >= 0);
}
