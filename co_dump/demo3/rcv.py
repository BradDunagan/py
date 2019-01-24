# Python modules
import time
import signal

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils


MY_SIGNAL = signal.SIGUSR1


def handle_signal(signal_number, stack_frame):
    message, priority = mq.receive()

    print("Ding! Message with priority %d received: %s" % (priority, message))


# Create the message queue.
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME, posix_ipc.O_RDONLY)

# Register my signal handler
signal.signal(MY_SIGNAL, handle_signal)

mq.request_notification(MY_SIGNAL);

print ( 'waiting for anything' );
utils.get_input();

