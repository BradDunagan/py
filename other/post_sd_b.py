#   post_sd_b.py
#
#   This consolidates all dumps where call is made from _PyEval_EvalFrameDefault.
#
#   The assumption is, for now, we are not concerned with what calls 
#   _PyEval_EvalFrameDefault.

import subprocess;

cnsFnc = '_PyEval_EvalFrameDefault';

file_name = 'stack-dumps-2.txt';        #   Work on what was produed by post_sd.py

lines = list ( open ( file_name, 'r' ) );

fo = open ( 'stack-dumps-b.txt', 'w' );

#   First scan it all in.
sds = [];	#	stack dumps
cns = [];	#	the consolidation
i = 0;		nLines = len ( lines );
while ( i < nLines ):
	line = lines[i].strip();
	if len ( line ) == 0:
		i += 1;
		continue;
	j = line.find ( 'atFnc: ' );
	if j < 0:
		i += 1;
		continue;
	fnc = line[j + len ( 'atFnc: ' ) : 30].strip();
	j = line.find ( 'count: ' );
	cnt = int ( line[j + len ( 'count: ' ) : ].strip() );

	i += 1;
	line = lines[i].strip();
	if line == cnsFnc:
		#	Got this dump yet?
		gotit = False;
		for j in range ( 0, len ( cns ) ):
			if cns[j]['atFnc'] == fnc:
				cns[j]['count'] += cnt;
				gotit = True;
				break;
		if gotit == False:
			d = {'atFnc': fnc, 'count': cnt, 'dmp': [cnsFnc]};
			cns.append ( d );
			sds.append ( d );
		#	Skip (ignore) the remaining lines of this dump.
		while len ( line ) > 0:
			i += 1;		line = lines[i].strip();
		continue;

	#	Add the dump to sds[].
	dmp = [];
	while len ( line ) > 0:
		dmp.append ( line );
		i += 1;		line = lines[i].strip();
	d = {'atFnc': fnc, 'count': cnt, 'dmp': dmp};
	sds.append ( d );

#	Now write the new dump.
for i in range ( 0, len ( sds ) ):
	d = sds[i];
	fo.write ( f"atFnc: {d['atFnc']}      count: {d['count']}\n" );
	dmp = d['dmp'];
	for j in range ( 0, len ( dmp ) ):
		fo.write ( f"    {dmp[j]}\n" );
	fo.write ( "\n" );

fo.close();



