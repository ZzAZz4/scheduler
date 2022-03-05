from schedule.scheduler import Scheduler
from schedule.tasks import PeriodicCallback


@PeriodicCallback.callback(period=1, times=5)
def display(args):
    print(args)

class App(Scheduler):
    def __init__(self):
        super().__init__()
        self.schedule(0, display("Hello"))
        

if __name__ == "__main__":
    app = App()
    app.run()