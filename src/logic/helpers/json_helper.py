import json

def json_to_dict(json_data:str) -> dict:
   return json.loads(json_data)

def dict_to_json(system_data:dict) -> str:
  return json.dumps(system_data)