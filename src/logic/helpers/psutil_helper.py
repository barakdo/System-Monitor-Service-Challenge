import psutil

KB = 1024 #in Bytes

#sample system data using "psutil" moudle
def sample_cpu() -> float:
  return psutil.cpu_percent()

def sample_ram() -> float:
  return psutil.virtual_memory().percent

def network_kb_sent() ->int:
  return psutil.net_io_counters().bytes_sent / KB

def network_kb_recv() ->int:
  return psutil.net_io_counters().bytes_recv / KB


######################
#psutil functions router

psutil_dict = {
  "CPU usage": sample_cpu,
  "RAM usage" : sample_ram,
  "Network sent": network_kb_sent,
  "Network received" : network_kb_recv
}

unit_dict ={
  "CPU usage": "%",
  "RAM usage" :" GB",
  "Network sent" : " KB",
  "Network received" : " KB"
}