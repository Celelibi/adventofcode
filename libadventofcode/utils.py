import logging
import time



class Timer:
    def __init__(self, prefix="time", fmt="%f seconds", logger="Timer", loglevel=logging.DEBUG, autoprint=True):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        if prefix is None:
            self._fmt = fmt
        else:
            self._fmt = prefix + ": " + fmt

        self._logger = logger
        self._loglevel = loglevel
        self._autoprint = autoprint

        self._elapsed = 0
        self._stattime = None
        self.start()

    def start(self):
        self._stattime = time.perf_counter()

    def stop(self):
        self._elapsed = time.perf_counter() - self._stattime
        if self._autoprint:
            self.print()

    def print(self):
        self._logger.log(self._loglevel, self._fmt, self._elapsed)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
