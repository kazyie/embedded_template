#pragma once
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <thread>
#include <functional>

#ifndef LOG_LEVEL
#define LOG_LEVEL 2  // 0:ERROR 1:WARN 2:INFO 3:DEBUG
#endif

inline uint64_t log_now_ms() {
    using namespace std::chrono;
    return duration_cast<milliseconds>(steady_clock::now().time_since_epoch()).count();
}

#define LOG_AT(level, tag, fmt, ...)                                             \
    do {                                                                         \
        if (LOG_LEVEL >= level) {                                                \
            std::fprintf(stderr, "[%llu][%s][tid=%zu] " fmt "\n",                \
                         (unsigned long long)log_now_ms(), tag,                  \
                         (size_t)std::hash<std::thread::id>{}(std::this_thread::get_id()), \
                         ##__VA_ARGS__);                                         \
        }                                                                        \
    } while (0)

#define LOG_ERROR(fmt, ...) LOG_AT(0, "E", fmt, ##__VA_ARGS__)
#define LOG_WARN(fmt, ...)  LOG_AT(1, "W", fmt, ##__VA_ARGS__)
#define LOG_INFO(fmt, ...)  LOG_AT(2, "I", fmt, ##__VA_ARGS__)
#define LOG_DEBUG(fmt, ...) LOG_AT(3, "D", fmt, ##__VA_ARGS__)
