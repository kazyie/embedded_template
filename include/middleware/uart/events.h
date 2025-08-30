#pragma once
#include <cstdint>
#include <vector>
#include "core/message.h"

enum class UARTEvent {
        SEND_HEX,
    STOP,
};

struct UARTContext {};
