from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Optional, Protocol

@dataclass
class BaseCallbackSettings:
    period: Optional[float] = None
    times: Optional[int] = None

class Loop(Protocol):
    def call_later(self, delay: float, callback: Callable[[], None]) -> asyncio.TimerHandle:
        ...
class Context(Protocol):
    loop: Loop
        

class BaseCallback(ABC):
    def __init__(self, fn, settings: BaseCallbackSettings, *args, **kwargs):
        self.fn = fn
        self.settings = settings
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def __call__(self, context):
        """Calls the function with the stored arguments"""

    @classmethod
    def callback(cls, **sargs):
        settings = BaseCallbackSettings(**sargs)
        def decorator(func) -> Callable[..., 'BaseCallback']:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return cls(func, settings, *args, **kwargs)
            return wrapper
        return decorator


class SimpleCallback(BaseCallback):
    def __init__(self, fn: Callable, settings, *args, **kwargs):
        super().__init__(fn, settings, *args, **kwargs)

    def __call__(self, context: Context):
        self.fn(*self.args, **self.kwargs)


class PeriodicCallback(BaseCallback):
    def __init__(self, fn: Callable, settings, *args, **kwargs):
        super().__init__(fn, settings, *args, **kwargs)


    def __call__(self, context: Context):
        if self.settings.times is None:
            self._call_forever(context)
        else:
            self._call_times(context)


    def _call_times(self, context: Context) -> None:
        def counter(n) -> Callable:
            def func() -> None:
                if n < self.settings.times:
                    self.fn(*self.args, *self.kwargs)
                    assert self.settings.period is not None
                    context.loop.call_later(self.settings.period, counter(n + 1))
            return func
        return counter(0)()

    def _call_forever(self, context: Context) -> None:
        def func():
            self.fn(*self.args, *self.kwargs)
            assert self.settings.period is not None
            context.loop.call_later(self.settings.period, func)
        return func()

