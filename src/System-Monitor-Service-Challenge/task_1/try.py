import time
import psutil
import os

for i in range(10000):
  print("CPU usage: ",psutil.cpu_percent(interval=2),"%")
  print("RAM usage: ", psutil.virtual_memory().percent,"%")

