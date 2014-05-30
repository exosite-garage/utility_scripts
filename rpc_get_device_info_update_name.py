#==============================================================================
# rpc_get_device_info_update_name.py
# Python script that gets the description of a device client and then 
# updates the name for it using proper owner client (portal)
#
#==============================================================================
## Tested with python 2.6.5
##
## Copyright (c) 2014, Exosite LLC
## All rights reserved.
##
## For License see LICENSE file

import socket
import sys
import json

HOST = 'm2.exosite.com'
PORT = 80

# NOTE: A device can get it's description but can not change it, only it's ownwer can change it's description

PORTAL_CIK = 'PORTALS_OWNER_CIK_HERE' #Get from: https://portals.exosite.com/account/portals
DEVICE_CIK = 'DEVICE_CIK_HERE' #Get from: https://portals.exosite.com/account/devices
DEVICE_ALIAS = 'device_to_change'
DEVICENAME = "NEW DEVICE NAME" #New Device Name


print ''
print '-----------------'
print 'Get Device Info'
print 'Device Name:',DEVICENAME
print '-----------------'


CALLS = [{"id" : 1, "procedure":"info", "arguments":[{"alias":""},{"description":True}]}]

RPC = { "auth" : {"cik" : DEVICE_CIK}, "calls" : CALLS }

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
#print 'Received: \r\n', str(data)
response = data.split('\r\n\r\n')

objs = json.loads(response[1])

# ASSUME NO ISSUES / NO ERROR CHECKING

description = objs[0]["result"]["description"] #this should be a json object

print "Description:"
print description

print ''
print '-----------------'
print 'Now lets change the name of the device '
print 'Only the owner client of the device can update it'
print 'Current Device Name:',description["name"]
print 'Change to: ', DEVICENAME
print '-----------------'

description['name'] = DEVICENAME #change the name in the description object

#Note, if device alias not available, use list and info RPCs to find the device's RID or Alias under your Portal Client
CALLS = [{"id" : 1, "procedure":"update", "arguments":[{"alias":DEVICE_ALIAS},description]}]  #Use device alias 

RPC = { "auth" : {"cik" : PORTAL_CIK}, "calls" : CALLS }

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

