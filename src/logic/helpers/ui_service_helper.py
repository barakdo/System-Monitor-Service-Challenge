import matplotlib.pyplot as plt
from .psutil_helper import unit_dict
import threading


################################################
#System data related functions
################################################


def update_system_data(old_system_data:dict,new_system_data, received_sample_first_time:threading.Event,sliding_window_size:int):
  if not isinstance(new_system_data,dict):
    raise TypeError(f"<new_system_data> must be a dict, currently {type(new_system_data)}")
  if old_system_data == {}:
    old_system_data = init_system_data(new_system_data) 
  remove_first_item = False
  if len(old_system_data["Time"]) >= sliding_window_size and sliding_window_size > 0:
    remove_first_item = True 
  for key,value in new_system_data.items():
    old_system_data[key].append(value)
    if remove_first_item:
      old_system_data[key].pop(0)
  if not received_sample_first_time.is_set():
    received_sample_first_time.set()
  return old_system_data

def init_system_data(system_data:dict):
    new_system_data = {}
    for key,_ in system_data.items():
      new_system_data[key] = []
    return new_system_data




################################################
#Graph related functions
################################################

def create_graph(system_data:dict):
  parameters_count = len(system_data) - 1 # Time is part of dict
  plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
  plt.ion()
  fig, axs = plt.subplots(parameters_count,1, figsize=(25,parameters_count*5))
  fig.canvas.manager.set_window_title('System Monitor')
  plt.subplots_adjust(hspace=0.5)
  plt.rc('font', size=16) 
  plt.show()
  return fig, axs


def update_graph(system_data, axs):
  count = 0
  for key,value in system_data.items():
    if key != "Time":
      if len(system_data) == 2:
        ax = axs
      else:
        ax = axs[count]
      ax.clear()
      ax.set_title(key)
      ax.set_xlabel('Time', fontsize=16)   
      ax.plot(system_data["Time"], value)
      y_label = ax.get_yticklabels()
      float_values = [label.get_position()[1] for label in y_label]
      modified_y_labels = [label.get_text() + unit_dict[key] for label in y_label]
      ax.set_yticks(float_values)
      ax.set_yticklabels(modified_y_labels)
      count+=1
  plt.pause(0.1)