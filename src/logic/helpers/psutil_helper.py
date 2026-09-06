import psutil

KB = 1024 #in Bytes

#sample system data using "psutil" moudle
def sample_cpu() -> float:
  return psutil.cpu_percent()

def sample_ram() -> float:
  return psutil.virtual_memory().percent

def network_kb_sent() ->float:
  return psutil.net_io_counters().bytes_sent / KB

def network_kb_recv() ->float:
  return psutil.net_io_counters().bytes_recv / KB

def swap_memory_in()->float:
   return psutil.swap_memory().sin / KB

def swap_memory_out()->float:
   return psutil.swap_memory().sout / KB


######################
#psutil functions router

psutil_dict = {
  "CPU usage": sample_cpu,
  "RAM usage" : sample_ram,
  "Network sent": network_kb_sent,
  "Network received" : network_kb_recv,
  "Swap memory in": swap_memory_in,
  "Swap memory out" : swap_memory_out
}

unit_dict ={
  "CPU usage": "%",
  "RAM usage" :" GB",
  "Network sent" : " KB",
  "Network received" : " KB",
  "Swap memory in": " KB",
  "Swap memory out" : " KB"
}

diff_list = ["Network sent","Network received","Swap memory in","Swap memory out"] #cumulative stats