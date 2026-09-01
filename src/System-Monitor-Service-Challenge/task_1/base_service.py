import threading
from queue import Queue

class BaseService(threading.Thread):
  _condition = threading.Condition()
  _q = Queue()

  def __init__(self):
    pass

  def run(self):
    pass

  def stop(self):
    pass

  #abstract method
  def run_service(): 
    raise NotImplementedError("run_service method does not implemented for this sub service")

