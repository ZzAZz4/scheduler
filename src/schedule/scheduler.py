import asyncio
from typing import Callable
from schedule.callbacks import BaseCallback

class Scheduler:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def schedule(self, delay: float, cb: Callable) -> asyncio.TimerHandle:
        return self.loop.call_later(delay, cb)
        
    def deschedule(self, task: asyncio.TimerHandle) -> None:
        task.cancel()
        
    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
