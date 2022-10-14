""" Simple singleton base class. """
# Needed for double-checked locking
from threading import RLock


class Singleton(type):
    __instance = None
    __rlock = None
    __uuid = None

    def __init__(cls, *args, **kwargs):
        super(Singleton, cls).__init__(*args, **kwargs)
        __instance = None
        __rlock = None
        __uuid = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            with RLock() as rlock:
                cls.__instance = super(Singleton, cls).__call__(cls)
                cls.__instance.__rlock = rlock
                cls.__instance.__uuid = hex(id(cls.__instance))
        return cls.__instance
