from abc import ABC, abstractmethod, abstractclassmethod
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Optional
import asyncio


class Params:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class BaseCallback(ABC):
    def __init__(self, fn: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.fn, self.args, self.kwargs = fn, args, kwargs

    @abstractmethod
    async def __call__(self):
        ...

    @abstractclassmethod
    def create(cls, *clargs, **ckwargs)\
        -> Callable[..., Callable[..., 'BaseCallback']]:
        ...

class SimpleCallback(BaseCallback):
    def __init__(self, fn: Callable, _=None, *args, **kwargs):
        super().__init__(fn, *args, **kwargs)

    async def __call__(self):
        self.fn(*self.args, **self.kwargs)
        
    
    @classmethod
    def create(cls, *cargs, **ckwargs):
        def decorator(func) -> Callable[..., 'SimpleCallback']:
            def wrapper(*args, **kwargs):
                return cls(func, *args, **kwargs)
            return wrapper
        return decorator


@dataclass
class PeriodicCallbackSettings:
    period: float
    times: Optional[int] = None


class PeriodicCallback(BaseCallback):
    def __init__(self, fn: Callable, params: Params, *args, **kwargs):
        super().__init__(fn, *args, **kwargs)
        self.__subinit(*params.args, **params.kwargs)

    async def __call__(self):
        await self.__schedule_runs()

    @classmethod
    def create(cls, period, times=None, *cargs, **ckwargs):
        params = Params(period, times)
        def decorator(func) -> Callable[..., 'PeriodicCallback']:
            def wrapper(*args, **kwargs):
                return cls(func, params, *args, **kwargs)
            return wrapper
        return decorator

    async def __schedule_runs(self):
        while self.__decrease_times():
            self.fn(*self.args, **self.kwargs)
            await asyncio.sleep(self.period)

    def __subinit(self, period, times=None):
        self.period, self.times = period, times

    def __decrease_times(self):
        if self.times is None:
            return True

        if self.times > 0:
            self.times -= 1
            return True

        return False
