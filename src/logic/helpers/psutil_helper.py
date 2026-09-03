import psutil

#sample system data using "psutil" moudle
def sample_cpu() -> float:
  return psutil.cpu_percent()

def sample_ram() -> float:
  return psutil.virtual_memory().percent

######################
#psutil functions router

psutil_dict = {
  "CPU_usage": sample_cpu,
  "RAM_usage" : sample_ram
}