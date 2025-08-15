# Generated using ChatGPT

## Prompt

```plain
From now on, write code for Python 3.6+. I said Python 3.6+ means the code itself must be able to run on Python 3.6. So no type hints here.

Write classes wrapping sockets to ease multimachine communication. Based on the builtin module socket. Use framing. The class hierarchy:

1. FramedSocket <-- JSONSocket
2. FramedServer <-- JSONServer
3. FramedClient <-- JSONClient

where Framed classes send and receive bytes ; JSON classes inherit them to send and receive JSON payloads instead, i.e. builtin (de)serialization.

Divide into multiple files. Each class has its own file.

Supports multithreading so that a server could handle multiple connections simultaneously.

Make them all easy to use. Answer directly in chat.

Provide examples on how to use them.
```

## Test

Run server:

```sh
python -m pefe_common.messaging server 0.0.0.0 5000
```

Run multiple clients with the same command:

```sh
python -m pefe_common.messaging client 0.0.0.0 5000
```
