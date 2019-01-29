import random
import time
import curses
import ast

# 3rd party modules
#   https://github.com/osvenskan/posix_ipc/
#   https://github.com/osvenskan/posix_ipc/blob/master/posix_ipc_module.c
import posix_ipc

# Utils for this demo
import utils

itop = 0

def show_lines ( lineno ):
	global scr, hw, lines, nlines, itop
	h = hw[0] - 4
	w = hw[1]
	h2 = h // 2;
	h4 = h // 4;

	lowbnd = h - h4;	#	lowest (in the view) highlighted line

	if lineno - itop <= 0:
		start = itop = lineno - h2
		if start < 0:
			start = itop = 0;
	else:
		if (lineno - itop) > lowbnd:
			#start = lineno - lowbnd
			start = itop = lineno - h2
		else:
			#start = 0
			start = itop

	for i in range ( start, nlines ):
		y = i - start
		if y >= h:
			break;
		if (i + 1) == lineno:
			s = f"{i+1:{4}} > " + lines[i][0:w-8].strip('\n');
			scr.addstr ( y, 0, s, curses.A_STANDOUT );
		else:
			s = f"{i+1:{4}}   " + lines[i][0:w-8].strip('\n');
			scr.addstr ( y, 0, s );
		scr.clrtoeol();


# Create the message queue.
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME, posix_ipc.O_CREX)

def main(win):
	global hw, mq, file_name, lines, nlines;
	h = hw[0]
	w = hw[1]
	curses.curs_set ( 0 );		#	hide the blinking cursor
	win.addstr( h - 4, 0, '-' * (w - 1) );
	nLoops = 0;
	while 1:          
		try:                 
			win.timeout ( 100 )
			key = win.getkey()         
			if key == 'q':
				break           
		except Exception as e:
			pass         
		try:
			message, priority = mq.receive ( timeout = 0.100 )
			msg = message.decode();
			win.addstr( h - 2, 0, "msg: " + msg  );
			win.clrtoeol();
			d = ast.literal_eval ( msg );
			if d['filename'] != file_name:
				file_name = d['filename'];
				fo = open ( file_name, 'r' );
				lines = list ( fo );
				nlines = len ( lines );
			lineno = d['lineno'];
			show_lines ( lineno );
		except posix_ipc.BusyError:
			pass;
		nLoops += 1;
		win.addstr ( h - 3, 0, str ( nLoops ) );


scr = curses.initscr();		#	the whole screen, same as win passed to main()
curses.start_color();

hw = scr.getmaxyx()

file_name = '';
lines = [];
nlines = 0;

curses.wrapper(main)

print ( "Destroying the message queue." );
mq.close();
posix_ipc.unlink_message_queue ( utils.QUEUE_NAME );

