import threading
from .logic.collection_service import CollectionService
from .logic.presentation_service import PresentationService
from .logic.ui_service import UIService
from .logic.helpers.user_preferences import task_number, sliding_window_size, sampling_interval, parameters_dict, validate_user_preferences
import time


def task():
  validate_user_preferences()

  requested_parameters = parameters_dict
  event = threading.Event()

  #Initialze Collection Service
  cs = CollectionService(requested_parameters, sampling_interval=sampling_interval)

  #Initialze Presentation Service
  if task_number==1:
    ps = PresentationService()
  else:
    ps = UIService(sliding_window_size)

  # starting threads
  cs.start()
  ps.start()

  #running until user press ctrl+c
  try:
    if task_number == 2:
      ps.display_graphs()
    event.wait()
  except KeyboardInterrupt:
    #stopping threads
    cs.stop()
    ps.stop()
    cs.join()
    ps.join()
    print("\nAll threads stopped")

