from typing import Callable
import asyncio

from core.tasks import BaseTask, PeriodicTask

class Scheduler:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def schedule(self, delay: float, cb: BaseTask, *args, **kwargs) -> asyncio.TimerHandle:
        if isinstance(cb, PeriodicTask):
            cb = cb.bind(self.loop)
        
        cbe = lambda : cb(*args, **kwargs)    
        return self.loop.call_later(delay, cbe)
        
    def deschedule(self, task: asyncio.TimerHandle) -> None:
        task.cancel()
        
    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
