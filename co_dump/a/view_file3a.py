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
stack_width = 20

thds  = {}
thdId = 0
nthds = 0

def show_stack ( stack ):	#	a list of dicts
	global scr, hw, lines, nlines, itop, stack_width, thdId, thds, nthds
	h = hw[0] - 4
	w = stack_width - 1
	#	Get the thread number. Add thread if necessary.
	try:
		thd  = thds[thdId]
		nthd = thd[0]
	except Exception as e:
		nthds += 1
		nthd   = nthds
		thds[thdId] = thd = [nthd, '']
	#	Unhighlight the top of stack of other threads.
	for k, v in thds.items():
		if k == thdId:
			continue
		X = (stack_width + 1) * (v[0] - 1)
		co = v[1]
		nc = len ( co )
		if nc < w:
			co += (' ' * (w - nc))
		scr.addstr ( 0, X, co )
	#	Show the stack of thdId.
	X = (stack_width + 1) * (nthd - 1)
	y = 0
	for d in stack:
		if y >= h:
			return
		co = d['co'][0:w]
		if y == 0:
			thd[1] = co				#	remember the top 
		nc = len ( co )
		if nc < w:
			co += (' ' * (w - nc))
		if y == 0:
			scr.addstr ( y, X, co, curses.A_STANDOUT )
		else:
			scr.addstr ( y, X, co )
		scr.addstr ( y, X + w, '| ' )
		y += 1
	for y in range ( y, h):
		scr.addstr ( y, X, (' ' * w) + '| ' )


def show_lines ( lineno ):
	global scr, hw, lines, nlines, itop, stack_width, thds
	X = (stack_width + 1) * len ( thds )
	h = hw[0] - 4
	w = hw[1] - X
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

	y = 0
	for i in range ( start, nlines ):
		y = i - start
		if y >= h:
			break;
		if (i + 1) == lineno:
			s = f"{i+1:{4}} > " + lines[i][0:w-8].strip('\n');
			scr.addstr ( y, X, s, curses.A_STANDOUT );
		else:
			s = f"{i+1:{4}}   " + lines[i][0:w-8].strip('\n');
			scr.addstr ( y, X, s );
		scr.clrtoeol();

	for y in range (y, h):
		scr.addstr ( y, X, ' ' * w )


# Create the message queue.
mq = posix_ipc.MessageQueue(utils.QUEUE_NAME, posix_ipc.O_CREX)

recordSrc = ''

def main(win):
	global hw, mq, file_name, lines, nlines, thdId, recordSrc;
	h = hw[0]
	w = hw[1]
	curses.curs_set ( 0 );		#	hide the blinking cursor
	curses.mousemask ( curses.KEY_MOUSE )
	win.addstr( h - 4, 0, '-' * (w - 1) )
	nLoops = 0;
	while 1:          
		try:                 
			win.timeout ( 100 )
			key = win.getch()
			if key == curses.KEY_MOUSE:
				ms = curses.getmouse()
				x = ms[1]
				y = ms[2]
				win.addstr ( h - 1, 0, f"y: {y}  x: {x}" )
				win.clrtoeol()
			if key == ord ( 'q' ):
				break           
		except Exception as e:
			pass         
		try:
			message, priority = mq.receive ( timeout = 0.100 )
			msg = message.decode();
			#win.addstr( h - 2, 0, "msg: " + msg  );
			#win.clrtoeol();
			m = ast.literal_eval ( msg );
			thdId = m['thread'];
			stack = m['stack']		#	list of dicts
			win.addstr ( h - 2, 0, f"{len ( stack )} frames" )
			win.clrtoeol()
			if thdId == 0:
				#	must be the record
				frame = stack[0];
				if frame['fn'] == '<record>':
					recordSrc = frame['src'];
					lines = recordSrc.split ( '\n' )
					nlines = len ( lines )
					lineno = frame['ln']
					show_lines ( lineno )
			else:
				show_stack ( stack )
				frame = stack[0];
				fn = frame['fn']
				if fn == '<record>':
					file_name = fn;
					lines = recordSrc.split ( '\n' )
					nlines = len ( lines )
					lineno = frame['ln']
					show_lines ( lineno )
				else:
					if fn != file_name:
						file_name = fn;
						fo = open ( file_name, 'r' );
						lines = list ( fo );
						nlines = len ( lines );
					lineno = frame['ln'];
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

#print ( "Destroying the message queue." );
mq.close();
posix_ipc.unlink_message_queue ( utils.QUEUE_NAME );

