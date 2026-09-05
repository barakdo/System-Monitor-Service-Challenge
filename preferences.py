#set <task> parameter to 1 or 2
task_number = 2

#set system data sampling rate in seconds
sampling_interval = 1

#setting <sliding_window_size> to a non positive number will display all sampled historical data, while setting to a positive number will display the last <sliding_window_size> sampled timestamps data
sliding_window_size=15

#sampling parameters
parameters_dict={
  "CPU_usage":True,
  "RAM_usage":True
}
