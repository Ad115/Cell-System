"""
Core logging classes
====================

The fundamental interfaces for logging.

"""
from .log import Log
from .weak import WeakLog
from .multi import MultiLog

__all__ = ['Log', 'WeakLog', 'MultiLog']
