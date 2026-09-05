import threading
from queue import Queue

class BaseService(threading.Thread):
  _q_not_empty_condition = threading.Condition()
  _q = Queue()
  _received_sample_first_time = threading.Event()

  def __init__(self):
    super().__init__()
    self._stop_event = threading.Event()

################################################
#Executable methods by BaseService thread
################################################
  def run(self):
    while True:
      if self._stop_event.is_set():
        break
      self.run_service()

  #abstract method
  def run_service(self): 
    raise NotImplementedError("run_service method is not implemented for this sub service")

################################################
#Executable methods by main thread
################################################
  def stop(self):
    self._stop_event.set()
    with self._q_not_empty_condition:
      self._q_not_empty_condition.notify()