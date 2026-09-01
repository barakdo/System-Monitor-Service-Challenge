from base_service import BaseService

class CollectionService(BaseService):

  def __init__(self, requested_parameters:dict):
    pass

  def define_requested_parameters(self, para:dict):
    pass

  def collect_system_data(self):
    pass

  def convert_to_json(self, system_data) -> str:
    pass

  def send_to_queue(self, json_data:str):
    pass

  def run_service(self):
    pass
