import json

def print_to_console(system_data:str):
    for key,value in json.loads(system_data).items():
      print(f"{key}: {value}%")