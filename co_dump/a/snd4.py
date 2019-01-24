# Python modules
import sys
import random
import signal

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils

MY_SIGNAL = signal.SIGUSR1

#	Open the message queue.
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME )

#	file_name = '/home/brad/dev/fork/cpython/Lib/threading.py'
filename	= sys.argv[1];
lineno		= sys.argv[2];
msg = str ( { 'filename': filename, 'lineno': int(lineno) } );
print ( msg );

#	Send it -
mq.send ( msg );

#	Close this end of the queue.
print ( "Closing the queue (this end?)." )
mq.close()



