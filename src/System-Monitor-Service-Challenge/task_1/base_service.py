import threading
from queue import Queue

class BaseService(threading.Thread):
  __condition = threading.Condition()
  __q = Queue()

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

  def read_from_queue(self):
    with self.__condition:
      self.__condition.wait_for(not self.__q.empty())
      return self.__q.get()

  def write_to_queue(self, item):
      with self.__condition:
        self.__q.put(item)
        self.__condition.notify()

  #abstract method
  def run_service(self): 
    raise NotImplementedError("run_service method does not implemented for this sub service")

