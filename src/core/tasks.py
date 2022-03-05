from abc import ABC
import asyncio
from typing import Callable


class BaseTask(ABC):
    def __init__(self, fn):
        pass

    def __call__(self):
        raise NotImplemented()

    @classmethod
    def from_callable(cls, *args, **kwargs):
        def inner(fn: Callable):
            return cls(fn, *args, **kwargs)
        return inner


class SimpleTask(BaseTask):
    def __init__(self, fn: Callable):
        super().__init__(fn)
        self.fn = fn

    def __call__(self, *args, **kwargs):
        self.fn(*args, **kwargs)


class PeriodicTask(BaseTask):
    def __init__(self, fn: Callable, period: float, times=None):
        super().__init__(fn)
        self.fn = fn
        self.period = period
        if times is None:
            self._bind_func = self._bind_forever
        else:
            self.times = times
            self._bind_func = self._bind_n

    def bind(self, loop: asyncio.AbstractEventLoop):
        return self._bind_func(loop)
    
    def _bind_n(self, loop: asyncio.AbstractEventLoop):
        def counter(n):
            def inner(*args, **kwargs):
                def func():
                    if n < self.times:
                        self.fn(*args, **kwargs)
                        loop.call_later(self.period, lambda: counter(n + 1)(*args, **kwargs))
                return func()
            return inner
        return SimpleTask(counter(0))
    
    def _bind_forever(self, loop: asyncio.AbstractEventLoop):
        def inner(*args, **kwargs):
            def func():
                self.fn(*args, **kwargs)
                loop.call_later(self.period, func)
            return func()
        return SimpleTask(inner)
    