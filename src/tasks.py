import threading
from .logic.collection_service import CollectionService
from .logic.presentation_service import PresentationService
from .logic.ui_service import UIService
from .logic.helpers.user_preferences import parameters_dict, sampling_interval

def task(task=1):

  requested_parameters = parameters_dict
  event = threading.Event()

  #Initialze Collection Service
  cs = CollectionService(requested_parameters, sampling_interval=sampling_interval)

  #Initialze Presentation Service
  if task==1:
    ps = PresentationService()
  else:
    ps = UIService()

  # starting threads
  cs.start()
  ps.start()

  #running until user press ctrl+c
  try:
    event.wait()
  except KeyboardInterrupt:
    #stopping threads
    
    cs.stop()
    ps.stop()
    cs.join()
    ps.join()
    print("\nAll threads stopped")
