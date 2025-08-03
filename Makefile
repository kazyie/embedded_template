CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude

SRCS = src/app/main.cpp src/middleware/message.cpp src/drivers/task_led.cpp src/middleware/task_uart.cpp src/middleware/task_log.cpp src/drivers/task_lcd.cpp src/middleware/task_bat.cpp src/drivers/task_foo.cpp src/app/task_test.cpp src/drivers/task_bar.cpp




OBJS = $(SRCS:.cpp=.o)

app: $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) app
