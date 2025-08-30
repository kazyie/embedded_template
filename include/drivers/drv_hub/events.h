#pragma once
#include <cstdint>
#include <vector>
#include "core/message.h"

enum class DRV_HUBEvent {
        TO_LED,
    TO_LCD,
    TO_UART,
    STOP,
};

struct DRV_HUBContext {};
