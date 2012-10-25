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
ALIAS = 'YOUR ALIAS HERE'
RESOURCEID = {"alias":ALIAS}
#RESOURCEID = 'DATA STACK RID' # Use instead of ALIAS

ARGUMENTS = [RESOURCEID]
PROCEDURE = "flush"
CALLREQUEST1 = {"id" : 1, "procedure":PROCEDURE, "arguments":ARGUMENTS}
CALLS = [CALLREQUEST1]
AUTH = { "cik" : DEVICECIK }
RPC = { "auth" : AUTH, "calls":CALLS}

json_rpc = json.dumps(RPC)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('POST /api:v1/rpc/process HTTP/1.1\r\n')
s.send('Host: m2.exosite.com\r\n')
s.send('Content-Type: application/json; charset=utf-8\r\n')
body = json_rpc
s.send('Content-Length: '+ str(len(body)) +'\r\n\r\n')
s.send(body)

data = s.recv(1024)
s.close()
print 'Received: \r\n', str(data)

