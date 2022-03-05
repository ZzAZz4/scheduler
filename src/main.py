import asyncio
from schedule.scheduler import Scheduler
from schedule.callbacks import schedule
import _thread


@schedule.call(schedule.times(5))
async def display(arg):
    print("Hello", arg)
    await asyncio.sleep(1)


@schedule.call()
def kill():
    _thread.interrupt_main()


class ExampleApp(Scheduler):
    def __init__(self):
        super().__init__()
        hello_fut = self.schedule(display('A'), after=0)
        desch_fut = self.schedule(lambda: self.remove(hello_fut), after=3)


def main():
    app = ExampleApp()
    app.run()


if __name__ == "__main__":
    main()
