##parameters -- which_executable("./atype.exe -s <x>", or "./btype.exe --niter <x>")
import subprocess as sp 
import shlex 
import boto3 
import time 


def main(event, context):
   start_time=time.time()
   sp.check_output(shlex.split(str(event["key1"])), timeout=850) #
   end_time=time.time()
   return start_time, end_time

