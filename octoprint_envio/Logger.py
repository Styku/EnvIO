import time
import os

class FileLogger:
    def __init__(self):
        pass

    def log(self, name, value):
        now = time.strftime("%x %X")
        with open(os.path.expanduser('~/logs/'+name+'.log'), 'a') as f:
            f.write('{};{};\n'.format(now, value))

