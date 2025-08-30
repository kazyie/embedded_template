#pragma once
#include <cstdint>
#include <vector>
#include "core/message.h"

enum class LEDEvent {
            BLINK,
    BLINK_FAST,
    BLINK_SOS,
    STOP,
};

struct LEDContext {};
