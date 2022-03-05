from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Optional
from asyncio import AbstractEventLoop, new_event_loop


@dataclass
class PeriodicCallbackSettings:
    period: float
    loop: AbstractEventLoop
    times: Optional[int] = None


class Params:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class BaseCallback(ABC):
    def __init__(self, fn, *args, **kwargs) -> None:
        super().__init__()
        self.fn, self.args, self.kwargs = fn, args, kwargs

    @abstractmethod
    def __call__(self):
        ...

    @classmethod
    def create(cls, *cargs, **ckwargs):
        params = Params(*cargs, **ckwargs)

        def decorator(func) -> Callable[..., 'BaseCallback']:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return cls(func, params, *args, **kwargs)
            return wrapper
        return decorator


class SimpleCallback(BaseCallback):
    def __init__(self, fn: Callable, *args, **kwargs):
        super().__init__(fn, *args, **kwargs)

    def __call__(self):
        self.fn(*self.args, **self.kwargs)


class PeriodicCallback(BaseCallback):
    def __init__(self, fn: Callable, params: Params, *args, **kwargs):
        super().__init__(fn, *args, **kwargs)
        self.__subinit(*params.args, **params.kwargs)

    def __call__(self):
        self.__schedule_runs()

    def __subinit(self, period, times=None, loop=None):
        loop = loop if loop is not None else new_event_loop()
        self.period, self.loop, self.times = period, loop, times

    def __schedule_runs(self):
        if self.__decrease_times():
            self.fn(*self.args, **self.kwargs)
            self.loop.call_later(self.period, lambda: self.__schedule_runs())

    def __decrease_times(self):
        if self.times is None:
            return True

        if self.times > 0:
            self.times -= 1
            return True

        return False
