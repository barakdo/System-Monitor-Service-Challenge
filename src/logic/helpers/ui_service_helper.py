import matplotlib.pyplot as plt

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
