# =========================
# Build config
# =========================
CXX ?= g++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Wpedantic -Iinclude -Iinclude/core -pthread -MMD -MP
CXXFLAGS += -DLOG_LEVEL=2   # 0:ERROR 1:WARN 2:INFO 3:DEBUG

# =========================
# Sources (auto collect)
# =========================
# 全ての .cpp を収集
SRCS := $(shell find src -type f -name '*.cpp' | sort)

# main と main.gen は片方だけ
ifneq ("$(wildcard src/app/main.gen.cpp)","")
  SRCS := $(filter-out src/app/main.cpp,$(SRCS))
else
  SRCS := $(filter-out src/app/main.gen.cpp,$(SRCS))
endif

# task_*_main.gen.cpp があるときは対応する task_*.cpp を除外
GEN_MAINS := $(shell find src -type f -name 'task_*_main.gen.cpp')
DUP_BASES := $(patsubst %_main.gen.cpp,%.cpp,$(GEN_MAINS))
SRCS := $(filter-out $(DUP_BASES),$(SRCS))

OBJS := $(SRCS:.cpp=.o)
DEPS := $(OBJS:.o=.d)

# =========================
# Per-layer include/macros
# =========================
BASE_INC = -Iinclude -Iinclude/core
APP_INC  = -Iinclude/app -Iinclude/middleware
MW_INC   = -Iinclude/middleware -Iinclude/drivers
DRV_INC  = -Iinclude/drivers

src/app/%.o:        CXXFLAGS += $(BASE_INC) $(APP_INC) -DCURRENT_LAYER_APP
src/middleware/%.o: CXXFLAGS += $(BASE_INC) $(MW_INC)  -DCURRENT_LAYER_MW
src/drivers/%.o:    CXXFLAGS += $(BASE_INC) $(DRV_INC) -DCURRENT_LAYER_DRV
src/core/%.o:       CXXFLAGS += $(BASE_INC)

# =========================
# Build targets
# =========================
.PHONY: all clean run
all: app

app: $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(DEPS) app

-include $(DEPS)

run: app
	./app

# =========================
# Tests (auto link all src/* except mains & duplicates)
# =========================
TEST_SRCS := $(shell find tests -type f -name '*.cpp' 2>/dev/null | sort)
TEST_OBJS := $(TEST_SRCS:.cpp=.o)
TEST_BIN  := tests/bin/unit

# テスト用にリンクする実装を自動収集（main 系は除外）
TEST_LINK_SRCS := $(shell find src -type f -name '*.cpp' ! -name 'main.cpp' ! -name 'main.gen.cpp' | sort)
# 上で求めた DUP_BASES をさらに除外（task_* と task_*_main.gen の多重定義回避）
TEST_LINK_SRCS := $(filter-out $(DUP_BASES),$(TEST_LINK_SRCS))
TEST_LINK_OBJS := $(TEST_LINK_SRCS:.cpp=.o)

# doctest ヘッダ
TEST_CXXFLAGS := $(CXXFLAGS) -Ithird_party

.PHONY: test
test: $(TEST_BIN)
	$(TEST_BIN)

$(TEST_BIN): $(TEST_OBJS) $(TEST_LINK_OBJS)
	@mkdir -p $(dir $@)
	$(CXX) $(TEST_OBJS) $(TEST_LINK_OBJS) -o $@ -pthread

tests/%.o: tests/%.cpp
	$(CXX) $(TEST_CXXFLAGS) -c $< -o $@

# =========================
# Sanitizers (optional)
# =========================
ASAN_FLAGS = -fsanitize=address,undefined -fno-omit-frame-pointer
TSAN_FLAGS = -fsanitize=thread -fno-omit-frame-pointer

.PHONY: test-asan
test-asan: CXXFLAGS += $(ASAN_FLAGS)
test-asan: clean test

.PHONY: test-tsan
test-tsan: CXXFLAGS += $(TSAN_FLAGS)
test-tsan: clean test

# =========================
# JUnit output (doctest reporter)
# =========================
.PHONY: test-junit
test-junit: $(TEST_BIN)
	@mkdir -p test-results
	@$(TEST_BIN) --reporters=junit --out=test-results/unit.xml --no-skip
	@ls -lh test-results/unit.xml

.PHONY: scan-format
scan-format:
	@for f in $(SRCS); do \
	  g++ -std=c++20 -E -H -Iinclude -Iinclude/core $$f 2>&1 >/dev/null | \
	  grep -q '/format$$' && echo "FORMAT included by: $$f"; \
	done || true



