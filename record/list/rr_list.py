
import rr_interface as app;
import rr_mark		as mark;

diags = False;

class rr_list ( list ):
	def __new__ ( cls, modId ):
		global diags;
		if diags:
			print ( f'rr_list.__new__()' );
		return super().__new__ ( cls, modId );
	def __init__ ( self, modId ):
		global diags;
		if diags:
			print ( f'rr_list.__init__()' );
		self.modId = modId;
		super().__init__();
	def append ( self, value ):
		global diags;
		if diags:
			print ( f'rr_list.append() value: {value}' );
		super().append ( value );
		app.callback ( self, f'append() value: {value}' );
	def __setitem__ ( self, key, value ):
		global diags;
		if diags:
			print ( f'rr_list.__setitem__() key: {key}  value: {value}' );

		# Mutable and marked? To detect changes made by, for example, 
		# functions. That is, a function's local variable could be set
		# as a reference to the value. We want to detect any changes the 
		# function makes using that reference.

		# What if a function's reference becomes the last reference? When 
		# the variables goes out of scope is it detectable? Does it matter?
		# -> Wait. When a function's variable is set to reference a makred
		# value the mark count is not incremented. It may become 0 and that 
		# would simply mean that any change should be ignored because no 
		# record references the value any longer.

		# First, unmark the current value.
		mark.unset_mark ( self.__getitem__ ( key ) );
		
		# Now mark the new value.
		value = mark.set_mark ( value );
		super().__setitem__ ( key, value );
		app.callback ( self, f'__setitem__() key: {key}  value: {value}' );


def test():
	global diags;
	diags = True;
	l = rr_list ( 904 );
	print ( f'modId: {l.modId}' );
	l.append ( 'hello' );
	print ( l );
	l[0] = 'yo';
	print ( l );

if __name__ == "__main__":
	test();
