import threading
from collection_service import CollectionService
from presentation_service import PresentationService

def main():
  #main thread

  requested_parameters = {}
  event = threading.Event()

  #Initialze Collection Service
  cs = CollectionService(requested_parameters)

  #Initialze Presentation Service
  ps = PresentationService()

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
    print("All threads stopped")

if __name__ == '__main__':
  main()