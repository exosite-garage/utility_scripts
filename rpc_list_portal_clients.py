#==============================================================================
# rpc_list_portal_clients.py
# Python script that uses Portal account CIK and lists all owned device clients
# and description information.
#
# Uses JSON RPC API, specifically 'list' and 'info' RPC functions.
#
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
import time

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

class ExositeDevice:
    def __init__(self, RID, name):
        self.rid = RID
        self.name = name
    cik = ""



HOST = 'm2.exosite.com'
PORT = 80
PORTALCIK = 'YOURPORTALCIKHERE' #Get from: https://portals.exosite.com/account/portals

#
# First get all clients for the portal account client (PORTALCIK)
#

ARGUMENTS = [["client"]]
PROCEDURE = "listing"
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

data = s.recv(2048)
#print 'Received Http Packet: \r\n', str(data)
response = data.split('\r\n\r\n')
#print 'Response Message:', response[1]
objs = json.loads(response[1])
deviceList = objs[0]["result"][0]

DeviceList = []
print ''
print '-----------------'
print 'Device Client List of RIDs'
print deviceList
print '-----------------'

print 'Now get information on each client'
#
# Now get each devices' name and CIK
#
print ''
print 'Account Device List'
for o in deviceList:
    ARGUMENTS = [o,["basic","description"]] #You can add other options here 
    PROCEDURE = "info"
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
    #print 'Received Http Packet: \r\n', str(data)
    response = data.split('\r\n\r\n')
    #print 'Response Message:', response[1]

    objs = json.loads(response[1])
    try:
        rid = str(o)
        name = str(objs[0]["result"]["description"]["name"])
        desc = str(objs[0]["result"]["description"])
        basicinfo = str(objs[0]["result"]["basic"])
        print ''
        print '-----------------'
        print 'Device Name:',name
        print '(RID:',o,')'
        print ''
        print 'Full Description:', desc
        print ''
        print 'Full Basic Information:', basicinfo
    except:
        print 'Exception creating array of devices'
    print '-----------------'
print ''

 
s.close()


