# Python modules

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils


# Create the message queue.
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME, posix_ipc.O_CREX)

while ( 1 ):
	try:
		message, priority = mq.receive ( timeout = 1.0 )
		print("Ding! Message with priority %d received: %s" % (priority, message))
		print ( 'message: ' + message.decode() );
	except posix_ipc.BusyError:
		print ( 'timeout' );
	print ( 'trying again' );



print ( 'waiting for anything - enter to terminate' );
utils.get_input();

print ( "Destroying the message queue." );
mq.close();
posix_ipc.unlink_message_queue ( utils.QUEUE_NAME );

