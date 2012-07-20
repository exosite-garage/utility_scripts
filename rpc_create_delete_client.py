#==============================================================================
# create_datarule_event.py
# Python script that creates a datarule for a device
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
PORTALCIK = 'YOURPORTALCIKHERE' #Get from: https://portals.exosite.com/account/portals
DEVICENAME = "TEST DEVICE"

print ''
print '-----------------'
print 'Create a New Device '
print 'Device Name:',DEVICENAME
print '-----------------'

LIMITS = {
      "client":"infinity" 
     ,"dataport":"infinity"
     ,"datarule":"infinity"
     ,"disk":"infinity"
     ,"dispatch":"infinity"
     ,"email":"infinity"
     ,"http":"infinity"
     ,"io":"infinity"
     ,"share":"infinity"
     ,"sms":"infinity"
     ,"xmpp":"infinity"
    }
META = {"device": {"type":"generic"},"timezone": "America/Chicago","location":"here"}
META_STRING = json.dumps(META)

DESCRIPTION = {"limits":LIMITS, "name":DEVICENAME,"meta":META_STRING, "locked":False, "visilibility":"parent", "writeinterval":0}
TYPE = "client"
ARGUMENTS = [TYPE,DESCRIPTION]
PROCEDURE = "create"
CALLREQUEST1 = {"id" : 1, "procedure":PROCEDURE, "arguments":ARGUMENTS}
CALLS = [CALLREQUEST1]
AUTH = { "cik" : PORTALCIK }
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
print 'Received: \r\n', str(data)
response = data.split('\r\n\r\n')

objs = json.loads(response[1])
#print objs
rid = objs[0]["result"]
print rid

print ''
print '-----------------'
print 'Now lets delete that New Device '
print 'Device Name:',DEVICENAME
print '-----------------'

RESOURCEID = rid
ARGUMENTS = [RESOURCEID]
PROCEDURE = "drop"
CALLREQUEST1 = {"id" : 1, "procedure":PROCEDURE, "arguments":ARGUMENTS}
CALLS = [CALLREQUEST1]
AUTH = { "cik" : PORTALCIK }
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
print 'Received: \r\n', str(data)



s.close()
