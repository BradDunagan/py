# Python modules
import time
import signal

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils


MY_SIGNAL = signal.SIGUSR1


def handle_signal(signal_number, stack_frame):
    while ( 1 ):
        message, priority = mq.receive()
        print("Ding! Message with priority %d received: %s" % (priority, message))
        print ( 'message: ' + message.decode() );


# Create the message queue.
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME, posix_ipc.O_CREX)

# Register my signal handler
signal.signal(MY_SIGNAL, handle_signal)

mq.request_notification(MY_SIGNAL);

print ( 'waiting for anything - enter to terminate' );
utils.get_input();

print ( "Destroying the message queue." );
mq.close();
posix_ipc.unlink_message_queue ( utils.QUEUE_NAME );

