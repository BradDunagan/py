
#   https://stackoverflow.com/questions/24072790/detect-key-press-in-python

import curses

def main(win):
    hw = win.getmaxyx()
    win.addstr ( 'hw: ' + str ( hw ) + '\n' )
    #win.nodelay(True)
    win.timeout ( 100 )
    key=""
    #win.clear()                
    win.addstr("Detected key:")
    while 1:          
        try:                 
            key = win.getkey()         
            #win.clear()                
            win.addstr("Detected key:")
            win.addstr(str(key)) 
            #if key == os.linesep:
            if key == 'q':
                win.addstr ( 'q?' )
                break           
        except Exception as e:
            # No input   
            pass         
    win.clear()
    win.addstr ( 'after while' )

curses.wrapper(main)

