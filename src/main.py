from schedule.scheduler import Scheduler, schedule
import _thread


@schedule.periodic(period=2)
def display(arg):
    print("Hello", arg)


@schedule.once()
def kill():
    _thread.interrupt_main()


class ExampleApp(Scheduler):
    def __init__(self):
        super().__init__()
        hello_fut = self.schedule(display('A'), delay=0)
        # desch_fut = self.schedule(lambda: self.remove(hello_fut), 5)
        killp_fut = self.schedule(kill(), 5)


def main():
    app = ExampleApp()
    app.run()


if __name__ == "__main__":
    main()
