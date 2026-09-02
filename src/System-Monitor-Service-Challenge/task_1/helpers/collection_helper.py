import psutil
import json


#sample system data using "psutil" moudle
def sample_cpu() -> float:
  return psutil.cpu_percent()

def sample_ram() -> float:
  return psutil.virtual_memory().percent

######################
#sample router

psutil_dict = {
  "CPU_usage": sample_cpu,
  "RAM_usage" : sample_ram
}

######################
#helper functions

def validate_parameters(requested_parameters:list):
  for item in requested_parameters:
    if item not in psutil_dict:
      raise Exception(f"Requested parameter [{item}] is not supported yet!")

def extract_relevant_parameters(parameters:dict) -> list:
    requested_parameters_list = []
    for key, value in parameters.items():
      if value == True:
        requested_parameters_list.append(key)
    validate_parameters(requested_parameters_list)
    return requested_parameters_list

def convert_to_json(system_data:dict) -> str:
  return json.dumps(system_data)