from core.scheduler import Scheduler
from core.tasks import SimpleCallback, PeriodicCallback


@PeriodicCallback.callback(period=1, times=5)
def display(args):
    print(args)

class App(Scheduler):
    def __init__(self):
        super().__init__()
        self.schedule(0, display("Hello"))
        

if __name__ == "__main__":
    display("Hello")
    app = App()
    app.run()