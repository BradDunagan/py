#   post_sd.py
#
#   post-process the stack-dump.txt file

import subprocess;

file_name = 'stack-dumps.txt';

lines = list ( open ( file_name, 'r' ) );

fo = open ( 'stack-dumps-2.txt', 'w' );

#	https://sourceware.org/binutils/docs/binutils/addr2line.html
#
#	http://www.nongnu.org/libunwind/
#
#   /home/brad/dev/myEmbdB/NoStack/NoS(StackDumpCB+0x37) [0x5555555bf4c1]
#   /home/brad/dev/myEmbdB/NoStack/NoS(PyEval_EvalFrameEx+0x15) [0x555555688169]
#	/home/brad/dev/myEmbdB/NoStack/NoS(+0x7ebe5) [0x5555555d2be5]

for line in lines:
	#	don't include StackDumpCB
	i = line.find ( 'StackDumpCB' );
	if i >= 0:
		continue;
	#	do we need to get the function name?
	i = line.find ( '/NoStack/NoS(+0x' );
	if i >= 0:
		i += len ( '/NoStack/NoS(+' );
		offset = line[i : line.find ( ')', i )];
		cp = subprocess.run ( ["addr2line", "-a", offset, "-e", "NoS", "-f"], 
							  stdout=subprocess.PIPE );
		fn = cp.stdout.decode().split ( '\n' )[1];
		fo.write ( f"    {fn}\n" );
		continue;
	#	just the function name
	i = line.find ( '/NoStack/NoS(' );
	if i >= 0:
		i += len ( '/NoStack/NoS(' );
		fn = line[i : line.find ( '+', i )];
		fo.write ( f"    {fn}\n" );
		continue;
	#	the entire line
	fo.write ( line );
