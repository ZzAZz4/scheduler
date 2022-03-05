from schedule.scheduler import Scheduler
from schedule.callbacks import PeriodicCallback, SimpleCallback
import _thread

@PeriodicCallback.create(period=2, times=5)
def display(args):
    print(args)
    
@SimpleCallback.create()
def kill():
    _thread.interrupt_main()

class App(Scheduler):
    def __init__(self):
        super().__init__()
        hello_key = self.schedule(0, display("Hello"))
        
        desch_key = self.schedule(5, SimpleCallback(lambda: self.remove(hello_key)))
        
        kill_key = self.schedule(8, kill())
        
def main():
    app = App()
    app.run()
     

if __name__ == "__main__":
    main()