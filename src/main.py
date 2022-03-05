from core.scheduler import Scheduler
from core.tasks import PeriodicTask, SimpleTask

@PeriodicTask.from_callable(period=1, times=6)
def display(string):
    print(string)

class App(Scheduler):
    def __init__(self):
        super().__init__()
        self.schedule(0, display, "Hello, world!")
        

if __name__ == "__main__":
    app = App()
    app.run()