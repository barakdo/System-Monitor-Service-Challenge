from .presentation_service import PresentationService
from .base_service import BaseService
from .helpers.psutil_helper import unit_dict
import time
import threading
import matplotlib.pyplot as plt

class UIService(PresentationService):
  def __init__(self,sliding_window_size=15):
    super().__init__()
    self.__system_data = {}
    self.__sliding_window_size = sliding_window_size
    self._condition_ui = threading.Condition() #ensures access to _system_data dict is safe


  def __process_history_data(self,system_data:dict):
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

  def get_system_data(self) -> dict:
    return self.__system_data
  
  def stop(self):
    plt.close()
    BaseService.stop(self)

  def run_service(self): 
    system_data = self.get_process_data()
    self.__process_history_data(system_data)

  def __close(self, event):
    BaseService.stop(self)

  def init_graph(self):
    self._received_sample_first_time.wait()
    parameters_count = len(self.__system_data) - 1 # Time is part of dict
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
    plt.ion()
    self.__fig, self.__axs = plt.subplots(parameters_count,1, figsize=(25,parameters_count*5))
    self.__fig.suptitle('System Monitor',fontsize= 30)

    plt.subplots_adjust(hspace=0.5)

    plt.rc('font', size=16) 
    self.__fig.canvas.mpl_connect('close_event', self.__close)
    plt.show()

  def print_graphs(self):
    self.init_graph()
    while True:
      if self._stop_event.is_set():
        raise KeyboardInterrupt
      
      count = 0
      with self._condition_ui: #safe iteration over a shared resourse
        self._condition_ui.wait()
        for key,value in self.__system_data.items():
          if key != "Time":
            self.__axs[count].clear()
            self.__axs[count].set_title(key)
            self.__axs[count].set_xlabel('Time', fontsize=16)   
            self.__axs[count].plot(self.__system_data["Time"], value)
            y_label = self.__axs[count].get_yticklabels()
            float_values = [label.get_position()[1] for label in y_label]
            modified_y_labels = [label.get_text() + unit_dict[key] for label in y_label]
            self.__axs[count].set_yticks(float_values)
            self.__axs[count].set_yticklabels(modified_y_labels)
            count+=1
        plt.pause(0.1)
     
    