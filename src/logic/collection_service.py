from .base_service import BaseService
from .helpers.collection_helper import extract_relevant_parameters, init_network, sample_time, add_sampled_parameters
from .helpers.json_helper import dict_to_json
import time

class CollectionService(BaseService):

  def __init__(self, requested_parameters:dict, sampling_interval:float = 1.0):
    super().__init__()
    self.__requested_parameters = extract_relevant_parameters(requested_parameters)
    self._sampling_interval = sampling_interval
    self.__network_data = init_network()

################################################
#CollectionService thread methods
################################################
  def collect_system_data(self) -> dict:
    data_dict = sample_time()
    data_dict = add_sampled_parameters(data_dict, self.__requested_parameters,self.__network_data)
    return data_dict

  def write_to_queue(self, item:str):
        if not isinstance(item, str):
           raise TypeError(f"The queue only accepts strings. [{item}] is not a string")
        with self._q_not_empty_condition:
          self._q.put(item)
          self._q_not_empty_condition.notify()

  def run_service(self):
    system_data = self.collect_system_data()
    system_data_json = dict_to_json(system_data)
    self.write_to_queue(system_data_json)
    time.sleep(self._sampling_interval)
