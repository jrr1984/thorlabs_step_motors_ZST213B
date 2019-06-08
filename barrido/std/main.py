import logging,threading,time
from logging.handlers import SocketHandler
from std.StageAndSpec import System
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)
import numpy as np
import time, threading
initial_time=time.time()
syst = System()
syst.connect()
num_avg=5
dx = 100.0
dy=100.0
x_array_scan = np.arange(0.0,dx*(50+1),dx)
y_array_scan = np.arange(0.0,dy*(50+1),dy)
BE_thread = threading.Thread(target=syst.scan_meander, args=(x_array_scan,y_array_scan,num_avg))
BE_thread.start()
storage_thread = threading.Thread(target = syst.storage_thread, args=(BE_thread,))
storage_thread.start()
BE_thread.join()
BE_total_time = time.time() - initial_time
log.info('MEASUREMENT Thread done, it took: {}.'.format(BE_total_time))
storage_thread.join()
storage_total_time = time.time() - initial_time
log.info('STORAGE Thread done, it took: {}.'.format(storage_total_time))
syst.disconnect()
elapsed_time = time.time() - initial_time
log.info('TOTAL TIME: {}'.format(elapsed_time))