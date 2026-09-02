import threading
from queue import Queue

class BaseService(threading.Thread):
  _condition = threading.Condition()
  _q = Queue()

  def __init__(self):
    super().__init__()
    self.__stop = threading.Event()

  def run(self):
    while True:
      if self.__stop.is_set():
        break
      self.run_service()

  def stop(self):
    self.__stop.set()

  #abstract method
  def run_service(self): 
    raise NotImplementedError("run_service method does not implemented for this sub service")

