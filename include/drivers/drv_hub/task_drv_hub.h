#pragma once
#include <stop_token>
#include "core/message.h"
void task_drv_hub(std::stop_token, MessageSystem&);
