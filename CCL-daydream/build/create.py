## python3 create.py <function_name>  (function_name can be 1_he or 1_le, note no sudo while calling python)
import subprocess as sp
import shlex
import sys
import os
FNULL = open(os.devnull, 'w')

function_name = sys.argv[1]
if "he" in function_name:
	command = "aws lambda create-function --function-name "+function_name+" --role arn:aws:iam::499754144859:role/lambdarole-s3 --handler test.main --memory-size 10000 --runtime python3.6 --timeout 900 --zip-file fileb://test.zip"
	sp.check_output(shlex.split(command))
if "le" in function_name:
	command = "aws lambda create-function --function-name "+function_name+" --role arn:aws:iam::499754144859:role/lambdarole-s3 --handler test.main --memory-size 5000 --runtime python3.6 --timeout 900 --zip-file fileb://test.zip"
	sp.check_output(shlex.split(command))

