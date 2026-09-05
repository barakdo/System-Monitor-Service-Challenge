from .psutil_helper import psutil_dict

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

def init_network()->dict:
  return {
       "Network sent": [],
       "Network received": []
    }
