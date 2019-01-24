# Python modules
import random
import time
import signal

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils


MY_SIGNAL = signal.SIGUSR1



# Create the message queue.
# Open 
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME )

# Request notifications
#mq.request_notification(MY_SIGNAL)

#	Send a bunch of messages.
for j in range ( 0, 10 ):
	start = random.randrange ( 1, 500+1-20 )
	count = random.randrange ( 1, 10+1 )
	for i in range ( start, start+count+1 ):
		mq.send ( str ( i ) );
		time.sleep ( 0.10 );	#	Need to sleep longer for notifications to happen?

# The signal fires almost instantly, but if I don't pause at least
# briefly then the main thread may exit before the notification fires.
print("Sleeping for one second to allow the notification to happen.")
time.sleep ( 1.0  )

print("Closing the queue (this end?).")
mq.close()
# I could call simply mq.unlink() here but in order to demonstrate
# unlinking at the module level I'll do it that way.
#posix_ipc.unlink_message_queue(utils.QUEUE_NAME)
