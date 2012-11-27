#==============================================================================
# rpc_flush_datastack.py
# Python script that flushes a dataport for a device
#
# IMPORTANT NOTE!!: This will remove all data in a dataport (data source)
# USE AT YOUR OWN RISK
#
#
#==============================================================================
## Tested with python 2.6.5
##
## Copyright (c) 2010, Exosite LLC
## All rights reserved.
##
## For License see LICENSE file

import socket
import sys
from time import time

try:
  if sys.version_info < (2 , 6):
    json_module= 'python-simplejson'
    import simplejson as json
  else:
    json_module= 'python-json'
    import json
except ImportError:
  print "The package '%s' is required." % json_module
  sys.exit(1)


HOST = 'm2.exosite.com'
PORT = 80
DEVICECIK = 'YOUR CIK HERE'
ALIAS = 'YOUR DATA SOURCE ALIAS HERE'
RESOURCEID = {"alias":ALIAS}
ENTRIES = [[int(time()), 52],[int(time())+1, 36],[int(time())+ 2, 44],[int(time())+ 3, 44]] # Example log data
OPTIONS = {}
#RESOURCEID = 'DATA STACK RID' # Use instead of ALIAS

ARGUMENTS = [RESOURCEID,ENTRIES,OPTIONS]
PROCEDURE = "record"
CALLREQUEST1 = {"procedure":PROCEDURE, "arguments":ARGUMENTS}
CALLS = [CALLREQUEST1]
AUTH = { "cik" : DEVICECIK }
RPC = { "auth" : AUTH, "calls":CALLS}

json_rpc = json.dumps(RPC)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print '\r\n\r\n----- MESSAGE -----\r\n\r\n'
s.send('POST /api:v1/rpc/process HTTP/1.1\r\n')
print 'POST /api:v1/rpc/process HTTP/1.1'
s.send('Host: m2.exosite.com\r\n')
print 'Host: m2.exosite.com\r\n'
s.send('Content-Type: application/json; charset=utf-8\r\n')
print 'Content-Type: application/json; charset=utf-8\r\n'
body = json_rpc
s.send('Content-Length: '+ str(len(body)) +'\r\n\r\n')
print 'Content-Length: '+ str(len(body)) +'\r\n'
s.send(body)
print body
print '\r\n\r\n----- RESPONSE -----\r\n\r\n'

data = s.recv(1024)
s.close()
print 'Received: \r\n', str(data)

