from base_service import BaseService
from helpers.presentation_helper import print_to_console

class PresentationService(BaseService):

  def __init__(self):
    super().__init__()
    

  def run_service(self):
    system_data_json = self.read_from_queue()
    if system_data_json is None:
      return
    if not isinstance(system_data_json,str):
      raise TypeError("System data read from queue must be string")
    print_to_console(system_data_json)
    
