from base_service import BaseService
from helpers.collection_helper import psutil_dict, extract_relevant_parameters, convert_to_json
import time

class CollectionService(BaseService):

  def __init__(self, requested_parameters:dict, sampling_interval:float = 1.0):
    super().__init__()
    self.__requested_parameters = extract_relevant_parameters(requested_parameters)
    self.__sampling_interval = sampling_interval

    
  def collect_system_data(self) -> dict:
    data_dict = {}
    for item in self.__requested_parameters:
          data_dict[item] = psutil_dict[item]()
    return data_dict


  def run_service(self):
    system_data = self.collect_system_data()
    system_data_json = convert_to_json(system_data)
    self.write_to_queue(system_data_json)
    time.sleep(self.__sampling_interval)
