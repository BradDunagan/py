# Python modules
import curses

# 3rd party modules
#   https://github.com/osvenskan/posix_ipc/
#   https://github.com/osvenskan/posix_ipc/blob/master/posix_ipc_module.c
import posix_ipc

# Utils for this demo
import utils

def looper():
	while ( 1 ):
		try:
			message, priority = mq.receive ( timeout = 1.0 )
			print("Ding! Message with priority %d received: %s" % (priority, message))
			print ( 'message: ' + message.decode() );
		except posix_ipc.BusyError:
			print ( 'timeout' );
		print ( 'trying again' );

# Create the message queue.
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME, posix_ipc.O_CREX)

#looper();

def main(win):
	curses.curs_set ( 0 );		#	hide the bliniking cursor
	hw = win.getmaxyx()
	win.addstr ( 'hw: ' + str ( hw ) )
	#win.nodelay(True)
	nLoops = 0;
	while 1:          
		try:                 
			win.timeout ( 100 )
			key = win.getkey()         
			win.addstr( 2, 0, "Detected key: " + str ( key ) );
			if key == 'q':
				break           
		except Exception as e:
			pass         
		try:
			message, priority = mq.receive ( timeout = 0.25 )
			win.addstr( 3, 0, "message: " + message.decode() );
			win.clrtoeol();
		except posix_ipc.BusyError:
			pass;
		nLoops += 1;
		win.addstr ( 1, 0, str ( nLoops ) );
		#win.move ( hw[0] - 1, hw[1] - 1 );

curses.wrapper(main)

print ( "Destroying the message queue." );
mq.close();
posix_ipc.unlink_message_queue ( utils.QUEUE_NAME );

