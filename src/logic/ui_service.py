from .presentation_service import PresentationService
from .base_service import BaseService
from .helpers.ui_service_helper import create_graph, update_graph, update_system_data
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
  def __process_history_data(self,new_system_data:dict):
    with self._condition_ui:
      self.__system_data = update_system_data(self.__system_data,new_system_data,self._received_sample_first_time,self.__sliding_window_size)
      self._condition_ui.notify()

  def run_service(self): 
    new_system_data = self.get_process_data()
    self.__process_history_data(new_system_data)

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

  def display_graphs(self):
    self.__init_graph()
    while True:
      if self._stop_event.is_set():
        raise KeyboardInterrupt
      with self._condition_ui: #safe iteration over a shared resourse
        self._condition_ui.wait()
        update_graph(self.__system_data, self.__axs)
  