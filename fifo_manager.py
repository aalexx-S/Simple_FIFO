import os
import errno
import multiprocessing
import time

"""
FIFO Manager.
Manage blocking read/write of named pipes.
"""
class FIFOManager:
    def __init__(self, fifo_name, mode):
        """
        Input:
            fifo_name: The name of the named pipe.
                It is actually a path to file.
            mode: The mode of the fifo.
                Only accept values 'r' for read, and 'w' for write.
                It can only be read or write. (Named pipes are unidirectional).

        Raise:
            ValueError, when receiving undefined 'mode' (only accept 'r' and 'w').
        """
        if mode not in ('r', 'w'):
            raise ValueError('Unknown mode: {0}.'.format(mode))

        self.fifo_name = fifo_name
        self.mode = mode

        # mkfifo, catch fifo exist error
        try:
            os.mkfifo(self.fifo_name)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise

    def read(self):
        """
        Read from named pipe.
        This function will block until writer finsih writing (i.e. close fifo).
        If the direction is incorrect (i.e. mode is write), OSError will be raised.

        Return:
            A string of read data.
            Only return when writers closed the pipe.

        Raise:
            OSError. Raised when mode is write.
        """
        if self.mode == 'w':
            raise OSError('Attempted to read from write only named pipe.')

        # open will be blocked until writer also open
        with open(self.fifo_name, 'r') as fifo:
            # read will be blocked until writer closed the fifo
            ret = fifo.read()
            return ret

    def write(self, string, timeout=-1):
        """
        Write to named pipe.
        This function will block until reader opens the fifo, or, it timeout.
        If the direction is incorrect (i.e. mode is read), OSError will be raised.

        Input:
            string:
                A string to write.
            timeout:
                Stop writing after 'timeout' seconds.
                Set a negative number to wait without a timeout.

        Raise:
            OSError. Raised when mode is read.
        """
        if self.mode == 'r':
            raise OSError('Attempted to write to read only named pipe.')

        # start blocking write
        p = multiprocessing.Process(target=self.__write_blocking, name="FIFOManager Write", args=(string,))
        p.start()

        # wait at most 'timeout' seconds
        if timeout < 0:
            p.join()
        else:
            p.join(timeout)

        if p.is_alive():
            p.terminate()
            p.join()

    def __write_blocking(self, string):
        # open will be blocked until reader also open
        with open(self.fifo_name, 'w') as fifo:
            fifo.write(string)
            fifo.flush()
