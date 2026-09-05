from .base_service import BaseService
from .helpers.presentation_helper import print_to_console
from .helpers.json_helper import json_to_dict

class PresentationService(BaseService):

  def __init__(self):
    super().__init__()

################################################
#Executable methods by PresentationService thread
################################################
  def __read_from_queue(self)->str:
      with self._q_not_empty_condition:
        self._q_not_empty_condition.wait()
        if self._stop_event.is_set():
          return "{}"
        if self._q.empty():
          raise ValueError("cannot read item from an empty queue")
        return self._q.get()

  def get_process_data(self) -> dict:
    system_data_json = self.__read_from_queue()
    if not isinstance(system_data_json,str):
      raise TypeError(f"System data read from queue must be a string, given [{system_data_json}]")
    return json_to_dict(system_data_json)
      
  def run_service(self):
    system_data = self.get_process_data()
    if not self._stop_event.is_set():
      print_to_console(system_data)
    
