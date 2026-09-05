from .psutil_helper import unit_dict

def print_to_console(system_data:dict):
    for key,value in system_data.items():
      if key == "Time":
        print(f"{key}: {value}")
      else:
        print(f"{key}: {value}{unit_dict[key]}")

