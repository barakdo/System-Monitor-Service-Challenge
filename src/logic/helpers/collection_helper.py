from .psutil_helper import psutil_dict, diff_list
from preferences import sliding_window_size, sampling_interval
import datetime

def validate_parameters(requested_parameters:list):
  for item in requested_parameters:
    if item not in psutil_dict:
      raise Exception(f"Requested parameter [{item}] is not supported yet!")

def extract_relevant_parameters(parameters:dict) -> list:
    if not isinstance(parameters,dict):
      raise TypeError("Given parameters need to be in a dict type")
    requested_parameters_list = []
    for key, value in parameters.items():
      if value == True:
        requested_parameters_list.append(key)
    validate_parameters(requested_parameters_list)
    return requested_parameters_list

def network_helper(network_data:list, new_data:float) -> tuple[float,list]:
  if network_data == []:
    last = new_data
  else:
    last = network_data[-1]
  network_data.append(new_data)
  return round(new_data - last,2), network_data

def init_difference_dict(parameter_list:list) -> dict:
  new_dict = {}
  for item in parameter_list:
     new_dict[item] = []
  return new_dict

def sample_time(parameters:list) -> dict:
  data_dict = {}
  if sampling_interval >= 1:
    data_dict["Time"] = datetime.datetime.now().strftime("%H:%M:%S")
  else:
    data_dict["Time"] = datetime.datetime.now().strftime("%H:%M:%S:%f")[:-5]
  if sliding_window_size > 15:
      data_dict["Time"] = data_dict["Time"][3:]
  if len(parameters) > 4:
     data_dict["Time"] = data_dict["Time"][3:]
  return data_dict

def add_sampled_parameters(data_dict:dict, requested_parameters:list, network_data:dict) -> dict:
  for item in requested_parameters:
    item_value = psutil_dict[item]()
    if item in diff_list:
        item_value, network_data[item] = network_helper(network_data[item], item_value)
    if not isinstance(item_value,(float, int)):
        raise TypeError("Mertric value must be a number, psutil library error")
    if item_value < 0:
        raise ValueError(f"All relevant metrics values must be non negative. Current value: [{item_value}]")
    data_dict[item] = item_value
  return data_dict