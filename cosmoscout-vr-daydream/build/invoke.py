## python3 invoke.py <function_name> <val1> <val2> <val3> (val1 = "./atype.exe", or "./btype.exe") (val2='-s', or '--niter') (val3=<x>)
import subprocess as sp
import shlex
import sys
import os
FNULL = open(os.devnull, 'w')

function_name = sys.argv[1]
val = sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4]
command= "aws lambda invoke --function-name "+function_name+" --payload \'{\"key1\":\""+str(val)+"\"}\' "+function_name+"_response.txt"
p=sp.check_output(shlex.split(command))


