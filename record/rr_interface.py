
callback = False;

#	What is called? The app? In general, how does the "app" know what to do 
#	with any particular variable value change?
#
#	Should not the callback be set per variable? -
#
#		dev cb:
#			#	call the app, or whatever
#
#		x = rr_int ( 0, cb );
#
#	Probably not that. Instead - the callback is called when another instance 
#	changes the value -
#
#		dev cb:
#			#	do whatever here
#
#		x = rr_int ( 0, cb );
#	or
#		x = 0;
#		x.__callback__ = cb;
#
#	Subclassing and this kind of thing is common in Python.
#
#	The purpose is to keep multiple instances of the same record in sync.
#
#	That means, on all changes, a message is sent to other processes -
#
#		msg: recId, varId, value

#	A frame has -
#
#		A process pane - CPython running command records.
#
#		A UDUI (Controls) pane.
#
#	The UDUI pane is notified when control properties change.
#
#		Is the UDUI pane a CPython process running a command record containing
#		the control variables? Damn it!