import random
import time
import curses

file_name = '/home/brad/dev/fork/cpython/Lib/threading.py'

itop = 0

def show_lines ( lineno ):
	global scr, hw, lines, nlines, itop
	h = hw[0]
	w = hw[1]
	h4 = h // 4;

	lowbnd = h - h4;	#	lowest (in the view) highlighted line

	if lineno - itop <= 0:
		start = itop = lineno - h4
		if start < 0:
			start = itop = 0;
	else:
		if (lineno - itop) > lowbnd:
			#start = lineno - lowbnd
			start = itop = lineno - h4
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


def main(win):
	curses.curs_set ( 0 );		#	hide the blinking cursor
	win.nodelay(False)

	#for i in range ( nlines - 10, nlines + 1 ):
	for i in range ( 10, 30+1 ):
		show_lines ( i )
		try:                 
			win.timeout ( 100 )
			key = win.getkey()         
		except Exception as e:
			pass         
		time.sleep ( 0.25 );
	for i in range ( 5, 10+1 ):
		show_lines ( i )
		try:                 
			win.timeout ( 100 )
			key = win.getkey()         
		except Exception as e:
			pass         
		time.sleep ( 0.25 );

	for j in range ( 0, 100 ):
		start = random.randrange ( 1, nlines+1-20 )
		count = random.randrange ( 1, 10+1 )
		for i in range ( start, start+count+1 ):
			show_lines ( i )
			try:                 
				win.timeout ( 100 )
				key = win.getkey()         
			except Exception as e:
				pass         
			time.sleep ( 0.10 );


	win.getkey()


scr = curses.initscr();		#	the whole screen, same as win passed to main()
curses.start_color();

hw = scr.getmaxyx()

fo = open ( file_name, 'r' );
lines = list ( fo );
nlines = len ( lines );

curses.wrapper(main)

