# Python modules
import time
import signal

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils



# I could call simply mq.unlink() here but in order to demonstrate
# unlinking at the module level I'll do it that way.
posix_ipc.unlink_message_queue(utils.QUEUE_NAME)
