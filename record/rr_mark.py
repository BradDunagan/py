
class mark:
    __init__ ( self, count ):
        self.count = count;


def set_mark ( value ):
    if type ( value ).find ( 'rr_' ) >= 0:
        value.mark.count++;
        return;
    value.mark = mark ( 1 );

    # If value is a list, for example, and it's items are likewise lists
    # then those items must be marked as well, recursively.  I.e., each such 
    # item is being referenced.


def unset_mark ( value ):
    value.mark.count--;
    if value.mark.count > 0:
        return;

    # Return list, for example, to a normal list?
    # No. When count reaches 0 it means that no record is referencing the
    # value. It will be garbage collected.

    # But if the list, for example, contains items that are themselves
    # marked then they must be unset, recursively.
    # Is that right?
    # It seems so because its like those items are being removed from the
    # list.
