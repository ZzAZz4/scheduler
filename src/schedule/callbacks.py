import functools
from typing import Awaitable, Callable, Optional
import asyncio


def executor_for(fn):
    awaitable = asyncio.iscoroutinefunction(fn)
    if awaitable:
        async def awaiter(*args, **kwargs):
            await fn(*args, **kwargs)
        return awaiter
    else:
        async def awaiter(*args, **kwargs):
            fn(*args, **kwargs)
        return awaiter


ConditionFunc = Callable[[], bool]
ScheduleFunc = Callable[..., Awaitable]


class schedule:
    @staticmethod
    def times(num: int) -> ConditionFunc:
        def inner():
            nonlocal num
            if num > 0:
                num -= 1
                return True
            return False
        return inner

    @staticmethod
    def forever() -> ConditionFunc:
        return lambda: True

    @staticmethod
    def call(cond: Optional[ConditionFunc] = None) -> Callable[[Callable], ScheduleFunc]:
        if cond is None:
            return schedule.once

        def decorator(fn) -> Callable[..., Awaitable]:
            executor = executor_for(fn)

            @functools.wraps(fn)
            async def wrapper(*args, **kwargs) -> None:
                while cond():
                    await executor(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def once(fn) -> Callable[..., Awaitable]:
        executor = executor_for(fn)

        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> None:
            await executor(*args, **kwargs)
        return wrapper
