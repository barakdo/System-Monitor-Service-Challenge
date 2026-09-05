from preferences import *

def validate_user_preferences():
  if task_number not in [1,2]:
    raise ValueError("<task_number> must be set to 1 or 2")
  if not isinstance(sampling_interval,(int, float)) or sampling_interval <=0:
    raise ValueError("<ampling_interval> must be a positive number")
  if not isinstance(sliding_window_size,(int)):
      raise ValueError("<sliding_window_size> must be an integer number")
  if not isinstance(parameters_dict,dict):
     raise ValueError("<parameters_dict> must be a dict")
  if parameters_dict == {}:
     raise ValueError("<parameters_dict> must contains at least one parameter")
  if points_value_label not in [True, False]:
     raise ValueError("<points_value_label> must be a bool")
  
