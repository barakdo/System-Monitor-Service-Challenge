from .base_service import BaseService
from .helpers.collection_helper import extract_relevant_parameters
from .helpers.json_helper import dict_to_json
from .helpers.psutil_helper import psutil_dict
from preferences import sampling_interval, sliding_window_size
import time
import datetime

class CollectionService(BaseService):

  def __init__(self, requested_parameters:dict, sampling_interval:float = 1.0):
    super().__init__()
    self.__requested_parameters = extract_relevant_parameters(requested_parameters)
    self._sampling_interval = sampling_interval

################################################
#Executable methods by CollectionService thread
################################################
  def collect_system_data(self) -> dict:
    data_dict = {}
    if sampling_interval >= 1:
      data_dict["Time"] = datetime.datetime.now().strftime("%H:%M:%S")
    else:
      data_dict["Time"] = datetime.datetime.now().strftime("%H:%M:%S:%f")[:-5]
    if sliding_window_size > 15:
       data_dict["Time"] = data_dict["Time"][3:]

    for item in self.__requested_parameters:
          item_value = psutil_dict[item]()
          if not isinstance(item_value,(float, int)):
             raise TypeError("Mertric value must be a number")
          if item_value < 0:
             raise ValueError(f"All relevant metrics values must be non negative. Current value: [{item_value}]")
          data_dict[item] = item_value
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
