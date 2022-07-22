import statistics as st
import numpy as np
import scipy.stats as s
import random
import os
import threading
import time
import subprocess as sp
import shlex
random.seed(1234)

def define_application(appname):
    test_list=["run-"+str(i+1) for i in range(50)]
    file_nil=['components_original.txt', 'concurrency_original.txt']
    exe_list_per_run=[[] for i in range(50)]
    range_list_per_run=[[] for i in range(50)]
    app_index=[]
    for test in test_list:
        #base_path="./"+appname+"/"+test+"/"
        base_path="../"+test+"/"
        txt_file = open(base_path+"/"+file_nil[0], "r")
        file_content=txt_file.read()
        file_content=file_content.split("\n")
        index_outer=[]
        for s in range(len(file_content)-1):
            file_c=file_content[s][1:-1].split(",")
            index_inner=[]
            for f in file_c:
                try:
                    index_inner.append(int(f))
                except:
                    pass
            index_outer.append(index_inner)
        app_index.append(index_outer)
    min_max_list=[]
    for j in app_index:
        for jj in j:
            for jjj in jj:
                min_max_list.append(jjj)
    lookup_exe=[]
    lookup_range=[]
    lookup_number=[]
    for j in range(min(min_max_list), max(min_max_list)+1):
        lookup_number.append(j)
        r=random.choice(exe_choice_list)
        lookup_exe.append(r)
        rr=random.uniform(min(range_choice_list[exe_choice_list.index(r)]), max(range_choice_list[exe_choice_list.index(r)]))
        lookup_range.append(int(rr))
    for i in range(len(app_index)):
        app_now=app_index[i]
        for j in app_now:
            exe_inner=[]
            ran_inner=[]
            for jj in j:
                exe=lookup_exe[lookup_number.index(jj)]
                ran=lookup_range[lookup_number.index(jj)]
                exe_inner.append(exe)
                ran_inner.append(ran)  
            exe_list_per_run[i].append(exe_inner)
            range_list_per_run[i].append(ran_inner) 
    return (exe_list_per_run, range_list_per_run)

def predict_hot_start(components_per_phase, max_num):
    if len(components_per_phase) >=1:
        data=np.array(components_per_phase)
        (loc, scale) = s.exponweib.fit_loc_scale(data, 2, 2)
        choice=[]
        for i in range(100):
            choice.append(random.weibullvariate(loc, scale))
        choice_list=[]
        for i in choice:
            choice_list.append((i-min(choice))/(max(choice)-min(choice))*max_num)
        final_choice=random.choice(choice_list)
    else:
        choice=[]
        for i in range(100):
            choice.append(random.weibullvariate(2,2))
        choice_list=[]
        for i in choice:
            choice_list.append((i-min(choice))/(max(choice)-min(choice))*max_num)
        final_choice=random.choice(choice_list)
    return final_choice

def get_he_le_number(predicted_components):
    if len(he_per_phase)<2:
        return int(predicted_components/2)
    else:
        if phase_time[len(phase_time)-1]>phase_time[len(phase_time)-2]:
            return int((predicted_components/2)*1.1)
        else:
            return int((predicted_components/2)*0.9)
        
def hot_start(num_he,num_le):
    #os.chdir("./"+appname+"/build/")
    for i in range(num_he):
        j=1
        while True:
            name=str(j)+"_he"
            if name not in function_pool:
                break
            j+=1
        try:
            command="python3 create.py "+name
            sp.check_output(shlex.split(command))
            function_pool.append(name)
        except:
            name=str(int(random.uniform(1,100000000)))+"_he"
            command="python3 create.py "+name
            sp.check_output(shlex.split(command))
            function_pool.append(name)
    for i in range(num_le):
        j=1
        while True:
            name=str(j)+"_le"
            if name not in function_pool:
                break
            j+=1
        try:
            command="python3 create.py "+name
            sp.check_output(shlex.split(command))
            function_pool.append(name)
        except:
            name=str(int(random.uniform(1,100000000)))+"_le"
            command="python3 create.py "+name
            sp.check_output(shlex.split(command))
            function_pool.append(name)
    #os.chdir("../..")
    
def execute_thread(exe,ran, func_name):
    t=time.time()
    if "a" in exe:
        #os.chdir("./"+appname+"/build/")
        command="python3 invoke.py "+func_name+" ./atype.exe -s "+str(ran)
        sp.check_output(shlex.split(command))
        #os.chdir("../..")
    if "b" in exe:
        #os.chdir("./"+appname+"/build/")
        command="python3 invoke.py "+func_name+" ./btype.exe --niter "+str(ran)
        sp.check_output(shlex.split(command))
        #os.chdir("../..")
    execution_time.append(time.time()-t)
    execution_time_function.append(func_name)
    
def delete_container(del_list):
    #os.chdir("./"+appname+"/build/")
    for func in del_list:
        command="python3 delete.py "+func
        sp.check_output(shlex.split(command))
    #os.chdir("../..")
           
def execute(exe_l, range_l):
    #hot starts
    exe_iter=[]
    range_iter=[]
    function_iter=[]
    ##cold starts
    exe_new_iter=[]
    range_new_iter=[]
    function_new_iter=[]
    ####
    function_new_pool=[]
    remove_list=[]
    #####
    for i in range(len(exe_l)):
        if len(function_pool)>0:
            func=random.choice(function_pool)
            exe_iter.append(exe_l[i])
            range_iter.append(range_l[i])
            function_iter.append(func)
            function_pool.remove(func)
            cold_start_time.append(0)
            cold_start_time_function.append(func)
            remove_list.append(func)
            time.sleep(1)
        else:
            t=time.time()
            #os.chdir("./"+appname+"/build/")
            j=999999
            while True:
                name=str(j)+"_he"
                if name not in function_new_pool:
                    break
                j+=1
            command="python3 create.py "+name
            sp.check_output(shlex.split(command))
            function_new_pool.append(name)
            #os.chdir("../..")
            cold_start_time.append(time.time()-t)
            cold_start_time_function.append(name)
            exe_new_iter.append(exe_l[i])
            range_new_iter.append(range_l[i])
            function_new_iter.append(name)
            remove_list.append(name)
            time.sleep(1)
    thread=[]
    for i in range(len(exe_iter)):
        thread.append(threading.Thread(target=execute_thread, args=(exe_iter[i],range_iter[i], function_iter[i],)))
    for i in range(len(exe_new_iter)):
        thread.append(threading.Thread(target=execute_thread, args=(exe_new_iter[i],range_new_iter[i], function_new_iter[i],)))
    for t in thread:
        t.start()
    for t in thread:
        t.join()
    delete_container(remove_list)

def generate_output(components):
    time=[]
    for t in cold_start_time:
        time.append(t)
    for i in range(len(execution_time)):
        ind=cold_start_time_function.index(execution_time_function[i])
        time[ind]+=execution_time[i]
    l=components-(num_he+num_le)
    if l>0:
        l=l
    else:
        l=0
    cost=sum(time)*((num_he+l)/(num_he+num_le+l))*per_sec_high + sum(time)*(num_le/(num_he+num_le+l))*per_sec_low
    return time, cost
    
if __name__ == "__main__":
    appname="CCL-daydream" ##
    exe_choice_list=["atype.exe", 'btype.exe'] ##
    range_choice_list=[[12,25], [10,100]] ##
    app_exe_list,app_range_list=define_application(appname) ##list of list of list
    per_sec_low=0.0000667 ##
    per_sec_high=0.0001667 ##
    execution_time=[]
    for run in range(50):
        components_per_phase=[]
        he_per_phase=[]
        function_pool=[]
        app_exe=app_exe_list[run] ## list of list
        app_range=app_range_list[run] ## list of list
        len_list=[]
        for phase in app_exe:
            len_list.append(len(phase))
        phase_index=0
        all_time=[]
        phase_time=[]
        execution_cost=[]
        for phase in app_exe:
            ####
            cold_start_time=[]
            cold_start_time_function=[]
            execution_time=[]
            execution_time_function=[]
            ####
            predicted_components=predict_hot_start(components_per_phase,max(len_list))
            predicted_components=int(predicted_components)
            num_he=get_he_le_number(predicted_components)
            num_le=predicted_components-num_he
            p=time.time()
            print(num_he,num_le)
            hot_start(num_he, num_le)
            execute(app_exe_list[run][phase_index], app_range_list[run][phase_index])
            tt,c=generate_output(len(phase))
            for t in tt:
                all_time.append(t)
            phase_time.append(time.time()-p)
            he_per_phase.append(num_he)
            execution_cost.append(c)
            components_per_phase.append(len(phase))
            phase_index+=1
            time.sleep(1)
        delete_container(function_pool)
        with open('../'+"./run-"+str(run+1)+"/function_service_time-baseline.txt", 'w') as f:
            for item in all_time:
                f.write("%s\n" % item)
        with open('../'+"./run-"+str(run+1)+"/phase_time-baseline.txt", 'w') as f:
            for item in phase_time:
                f.write("%s\n" % item)
        with open('../'+"./run-"+str(run+1)+"/execution_cost-baseline.txt", 'w') as f:
            for item in execution_cost:
                f.write("%s\n" % item)
