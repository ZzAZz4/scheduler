import asyncio
from typing import Awaitable, Callable

class Scheduler:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def schedule(self, delay: float, cb: Callable[..., Awaitable]) -> asyncio.Future:
        async def wrapper():
            await asyncio.sleep(delay)
            await cb()
        
        return asyncio.ensure_future(wrapper(), loop=self.loop)
        
        
    def remove(self, task: asyncio.Future) -> None:
        task.cancel()
        
    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
