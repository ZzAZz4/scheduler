from abc import ABC, abstractmethod
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
    def __init__(self, fn: Callable, _=None, *args, **kwargs):
        super().__init__(fn, *args, **kwargs)

    async def __call__(self):
        self.fn(*self.args, **self.kwargs)



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
