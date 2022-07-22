## python3 delete.py <function_name>  (function_name can be 1_he or 1_le, note no sudo while calling python)
import subprocess as sp
import shlex
import sys
import os
FNULL = open(os.devnull, 'w')

function_name = sys.argv[1]
command = "aws lambda delete-function --function-name "+function_name
try:
    sp.check_output(shlex.split(command))
except:
    pass

