#25(or more), 15
import random
import os
import shlex
import subprocess as sp
import time
import sys
import statistics as st
import threading
import psutil
random.seed(1234)

number_of_phase = int(sys.argv[1])
max_in_each_phase = int(sys.argv[2])
#number_of_phase=100
#max_in_each_phase=100

profile_interval=0.1 ##
command="sudo docker run jblaschke/cctbx:n10-workflow ./run_tests_docker.sh 1 1" ##

cpu_utilization=[]
memory_used=[]
io_time=[]

def run_main_command(string):
    os.system(string)

def run_command(m):
    i=1
    string=''
    while i<=m:
        if i != m:
            string+=command+" & "
        else:
            string+=command
        i+=1
    threads=[]
    t1=threading.Thread(target=run_main_command, args=[string])
    t1.start()
    threads.append(t1)
    while True:
        if t1.is_alive():
            cpu_utilization.append(psutil.cpu_percent(interval=profile_interval)) 
            memory_used.append(psutil.virtual_memory().used)
            io_time.append(psutil.disk_io_counters().read_bytes + psutil.disk_io_counters().write_bytes)
        else:
            break

l_list=[]
for i in range(number_of_phase):
    l_list.append(random.weibullvariate(10, 3.2)) ##
ll_list=[]
for l in l_list:
    ll_list.append(((l-min(l_list))/(max(l_list)-min(l_list)))*max_in_each_phase)
lll_list=[]
for l in ll_list:
    if l<=1:
        lll_list.append(1)
    else:
        lll_list.append(int(l))
main_list=[]
for ll in lll_list:
    inner_list=[]
    val_seen=[]
    for val in lll_list:
        if val < ll + 0.63*st.stdev(lll_list) and val > ll - 0.63*st.stdev(lll_list):
            inner_list.append(val)
            val_seen.append(val)
    main_list.append(inner_list)
    for item in val_seen:
        try:
            lll_list.remove(item)
        except:
            pass
random.shuffle(main_list)
concurrency_list=[]
for item in main_list:
    for i in item:
        concurrency_list.append(i)
for m in concurrency_list:
    run_command(m)
    time.sleep(0.5)
    os.system("sudo docker rm $(sudo docker ps --filter status=exited -q)")

textfile = open("concurrency_per_phase.txt", "w")
for element in concurrency_list:
    textfile.write(str(element) + "\n")
textfile = open("cpu_utilization.txt", "w")
for element in cpu_utilization:
    textfile.write(str(element) + "\n")
textfile = open("memory_used.txt", "w")
for element in memory_used:
    textfile.write(str(element) + "\n")
io=[]
i=1
while i < len(io_time):
    io.append(io_time[i]-io_time[i-1])
    i+=1
textfile = open("io_bytes.txt", "w")
for element in io:
    textfile.write(str(element) + "\n")
textfile.close()
