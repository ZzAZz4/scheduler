from schedule.scheduler import Scheduler
from schedule.callbacks import PeriodicCallback


@PeriodicCallback.create(period=2, times=5)
def display(args):
    print(args)

class App(Scheduler):
    def __init__(self):
        super().__init__()
        hello_handle = self.schedule(0, display("Hello"))
        self.schedule(1, lambda: hello_handle.cancel())
        

if __name__ == "__main__":
    app = App()
    app.run()