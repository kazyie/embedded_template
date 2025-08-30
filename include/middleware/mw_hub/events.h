#pragma once
#include <cstdint>
#include <vector>
#include "core/message.h"

enum class MW_HUBEvent {
        REQ_LED_ON,
    REQ_LCD_PRINT,
    REQ_UART_SEND,
    STOP,
};

struct MW_HUBContext {};
