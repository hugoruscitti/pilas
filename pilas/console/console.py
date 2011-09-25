# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
from code import InteractiveConsole


class Cache(object):
    """Replace stdout and stderr behavior in order to collect outputs."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Clean the cache."""
        self.out = []

    def write(self, line):
        """Collect the output into cache to be accesed later."""
        self.out.append(line)

    def flush(self):
        """Join together all the outputs and return it to be displayed."""
        if len(self.out) > 1:
            output = ''.join(self.out)[:-1]
            self.reset()
            return output


class Console(InteractiveConsole):
    """Work as a Python Console."""

    def __init__(self, locals):
        InteractiveConsole.__init__(self, locals)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self._cache = Cache()
        self.output = ''

    def get_output(self):
        """Replace out and error channels with cache."""
        sys.stdout = self._cache
        sys.stderr = self._cache

    def return_output(self):
        """Reassign the proper values to output and error channel."""
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def push(self, line):
        """Insert a command into the console."""
        if line in ('exit()', 'help()'):
            return
        self.get_output()
        val = InteractiveConsole.push(self, line)
        self.return_output()
        self.output = self._cache.flush()
        return val
