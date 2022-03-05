import asyncio
from typing import Any, Awaitable, Callable, Union
from schedule.callbacks import schedule

class Scheduler:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def schedule(self, cb: Union[Callable, Awaitable], after: float = 0) -> asyncio.Future:
        async def wrapper():
            await asyncio.sleep(after)
            if isinstance(cb, Awaitable):
                await cb
            else:
                cb()
        
        return asyncio.ensure_future(wrapper(), loop=self.loop)
    
        
    def remove(self, task: asyncio.Future) -> bool:
        return task.cancel()
    
    def schedule_cb(self, cb: Callable[[], Any], after: float = 0) -> asyncio.Future:
        return self.schedule(schedule.once(cb)(), after)
    
    def run(self):
        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
