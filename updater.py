"""
A class that handles running a function 'every N seconds'. This will be used
whenever any data needs to be updated every N seconds, or if the form is to
be saved every N seconds, etc.

example usage:

def foo(x):
    print(sum(x))
tmr = Updater(3, foo, [1,2,3])
// this will 6 every 3 seconds

tmr.stop()
// this will stop the udpater
"""

__author__ = "Max Chan, Nick Chua"

from threading import Timer

class Updater:
    """
    TODO: Documentation (Only remove when documentation is complete)
    """
    def __init__(self, interval, func, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.func(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.daemon = True
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

