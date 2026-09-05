from preferences import *


#set <task> parameter to 1 or 2
_task_number = task_number

#set system data sampling rate in seconds
_sampling_interval = sampling_interval

#setting <sliding_window_size> to a non positive number will display all sampled historical data, while setting to a positive number will display the last <sliding_window_size> sampled timestamps data
_sliding_window_size=sliding_window_size

#sampling parameters
_parameters_dict= parameters_dict


def validate_user_preferences():
  if _task_number not in [1,2]:
    raise ValueError("<task_number> must be set to 1 or 2")
  if not isinstance(_sampling_interval,(int, float)) or _sampling_interval <=0:
    raise ValueError("<ampling_interval> must be a positive number")
  if not isinstance(_sliding_window_size,(int)):
      raise ValueError("<sliding_window_size> must be an integer number")
  if not isinstance(parameters_dict,dict):
     raise ValueError("<parameters_dict> must be a dict")
  
