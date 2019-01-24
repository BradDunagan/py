import datetime;
import rr_interface as rr;

def countdown ( n ):
	while n > 0:
		n -= 1;

count = 10000000;
print ( 'count: ' + str ( count ) );
ts = datetime.datetime.now();
rr.releaseGIL();
countdown ( count );
te = datetime.datetime.now();
dt = te - ts;
print ( dt.total_seconds() );
