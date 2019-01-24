import keyboard
import time

qhit = False;

def onKey ( evt ):
    global qhit;
    print ( str ( evt ) );
    print ( 'evt.name: ' + evt.name );
    if evt.name == 'q':
        print ( 'exiting ...' );
        qhit = True
        exit();

keyboard.hook ( onKey );

print ( 'looping ...' );

#keyboard.wait ( 'esc', True );
while True:
    time.sleep ( 1 );
    if qhit:
        exit();

