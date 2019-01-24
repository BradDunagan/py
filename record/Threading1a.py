import threading;
import datetime;

def countdown ( n ):
	while n > 0:
		n -= 1;

count = 100000000;
print ( 'One thread ...' );
ts = datetime.datetime.now();
countdown ( count );
te = datetime.datetime.now();
dt = te - ts;
print ( dt.total_seconds() );

print ( 'Two threads ...' );
t1 = threading.Thread ( target = countdown, args = (count//2,) );
t2 = threading.Thread ( target = countdown, args = (count//2,) );
ts = datetime.datetime.now();
t1.start();
t2.start();
t1.join();  t2.join();
te = datetime.datetime.now();
dt = te - ts;
print ( dt.total_seconds() );

print ( 'Four threads ...' );
t1 = threading.Thread ( target = countdown, args = (count//4,) );
t2 = threading.Thread ( target = countdown, args = (count//4,) );
t3 = threading.Thread ( target = countdown, args = (count//4,) );
t4 = threading.Thread ( target = countdown, args = (count//4,) );
ts = datetime.datetime.now();
t1.start();
t2.start();
t3.start();
t4.start();
t1.join();  t2.join(); t3.join();  t4.join();
te = datetime.datetime.now();
dt = te - ts;
print ( dt.total_seconds() );
