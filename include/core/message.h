#ifndef MESSAGE_H
#define MESSAGE_H

#include <mutex>
#include <condition_variable>
#include <queue>
#include <map>


enum class TaskID
{
    LED,
    UART,
    LOG,
    LCD,
    BAT,
    FOO,
    BAR,
    TEST,
};
enum class MessageType
{
    NONE,
    BLINK,
    DATA
};

struct Message
{
    MessageType type = MessageType::NONE;
    TaskID to;
    TaskID from;
};

class MessageSystem
{
public:
    void send(TaskID to, const Message &msg);
    Message receive(TaskID tid);

private:
    std::mutex mtx_;
    std::condition_variable cv_;
    std::map<TaskID, std::queue<Message>> queues_;
};

#endif // MESSAGE_H
