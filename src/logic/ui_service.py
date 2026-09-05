from .presentation_service import PresentationService
from .base_service import BaseService
from .helpers.psutil_helper import unit_dict
from .helpers.ui_service_helper import create_graph
from .helpers.user_preferences import sampling_interval
import threading
import matplotlib.pyplot as plt

class UIService(PresentationService):
  def __init__(self,sliding_window_size=15):
    super().__init__()
    self.__system_data = {}
    self.__sliding_window_size = sliding_window_size
    self._condition_ui = threading.Condition() #ensures access to _system_data dict is safe

################################################
#Executable methods by UIService thread
################################################
  def __process_history_data(self,system_data:dict):
    if not isinstance(system_data,dict):
      raise TypeError(f"<system_data> must be a dict, currently {type(system_data)}")
    with self._condition_ui:
      if self.__system_data == {}:
        self.__init_system_data(system_data) 
      remove_first_item = False
      if len(self.__system_data["Time"]) >= self.__sliding_window_size and self.__sliding_window_size > 0:
        remove_first_item = True 
      for key,value in system_data.items():
        self.__system_data[key].append(value)
        if remove_first_item:
          self.__system_data[key].pop(0)
      if not self._received_sample_first_time.is_set():
        self._received_sample_first_time.set()
      self._condition_ui.notify()

  def __init_system_data(self, system_data:dict):
    for key,_ in system_data.items():
      self.__system_data[key] = []

  def run_service(self): 
    system_data = self.get_process_data()
    self.__process_history_data(system_data)

  def stop(self):
    plt.close()
    BaseService.stop(self)

################################################
#Executable methods by main thread
################################################
  def __user_closed_graph(self, event):
    BaseService.stop(self)

  def __init_graph(self):
    self._received_sample_first_time.wait()
    self.__fig, self.__axs = create_graph(self.__system_data)
    self.__fig.canvas.mpl_connect('close_event', self.__user_closed_graph) #trigger <self.__user_closed_graph> when user close system monitor window

  def __print_graphs(self):
    self.__init_graph()
    while True:
      count = 0
      with self._condition_ui: #safe iteration over a shared resourse
        self._condition_ui.wait()
        for key,value in self.__system_data.items():
          if key != "Time":
            if len(self.__system_data) == 2:
              ax = self.__axs
            else:
              ax = self.__axs[count]
            ax.clear()
            ax.set_title(key)
            ax.set_xlabel('Time', fontsize=16)   
            ax.plot(self.__system_data["Time"], value)
            y_label = ax.get_yticklabels()
            float_values = [label.get_position()[1] for label in y_label]
            modified_y_labels = [label.get_text() + unit_dict[key] for label in y_label]
            ax.set_yticks(float_values)
            ax.set_yticklabels(modified_y_labels)
            count+=1
        plt.pause(sampling_interval - 0.05)
  
  def display_graphs(self):
    self.__print_graphs()
   
    