#==============================================================================
# rpc_list_client_datarules.py
# Python script that finds datarules for a client and finds state
# It then polls in a loop to look for state changes.
#
# To Do: optimize sending RPC function calls to send multiple RPCs in
# one HTTP request and response.  That would run faster instead of
# asking for each RPC via one HTTP request.  
#
# To Do: Check what happens when it encounters a Script data rule
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

class ExositeEvent:
    def __init__(self, RID, name,ruletype):
        self.rid = RID
        self.name = name
        self.ruletype = ruletype
    state = 0
    firstTime = 1



HOST = 'm2.exosite.com'
PORT = 80
DEVICECIK = 'YOUR CIK HERE'  #get from your device (https://portals.exosite.com/manage/devices)

#
# First get all datarules for the client device (DEVICECIK)
#

if DEVICECIK =='YOUR CIK HERE' or len(DEVICECIK) is not 40:
    print 'THIS SCRIPT WILL NOT WORK WITHOUT VALID CIK'
    print 'Exiting...'
    sys.exit(1)

ARGUMENTS = [["datarule"]]
PROCEDURE = "listing"
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
s.send('Connection: Close \r\n')
body = json_rpc
s.send('Content-Length: '+ str(len(body)) +'\r\n\r\n')
s.send(body)

data = s.recv(1024)
#print 'Received Http Packet: \r\n', str(data)
response = data.split('\r\n\r\n')
#print 'Response Message:', response[1]
objs = json.loads(response[1])
currentDatarules = objs[0]["result"][0]

DataRuleList = []

#
# Now get each event's information
#
print ''
print 'Client Data Rule (Event) List'
for o in currentDatarules:
    ARGUMENTS = [o,["basic","description"]]
    PROCEDURE = "info"
    CALLREQUEST1 = {"id" : 1, "procedure":PROCEDURE, "arguments":ARGUMENTS}
    CALLS = [CALLREQUEST1]
    AUTH = { "cik" : DEVICECIK }
    RPC = { "auth" : AUTH, "calls":CALLS}

    json_rpc = json.dumps(RPC)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send('POST /api:v1/rpc/process HTTP/1.1\r\n')
    s.send('Host: m2.exosite.com\r\n')
    s.send('Connection: Close \r\n')
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
        if any (k in objs[0]["result"]["description"]["rule"] for k in ("duration","interval","timeout","count")):
            ruletype = 'logic'
        elif "script" in objs[0]["result"]["description"]["rule"]:
            ruletype = 'script'
        else:
            ruletype = 'unknown'
        DataRuleList.append(ExositeEvent(rid,name,ruletype))
        print 'Event (RID:',o,') Name:',name,', [Type:',ruletype,']'
    except:
        print 'Exception creating array of Events'
print ''
#
# Now find state of event
#
print 'Data Rule (Logical only) Current States:'
for event in DataRuleList:
    if event.ruletype == "logic":
        ARGUMENTS = [event.rid,[]]
        PROCEDURE = "read"
        CALLREQUEST1 = {"id" : 1, "procedure":PROCEDURE, "arguments":ARGUMENTS}
        CALLS = [CALLREQUEST1]
        AUTH = { "cik" : DEVICECIK }
        RPC = { "auth" : AUTH, "calls":CALLS}

        json_rpc = json.dumps(RPC)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send('POST /api:v1/rpc/process HTTP/1.1\r\n')
        s.send('Host: m2.exosite.com\r\n')
        s.send('Connection: Close \r\n')
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
            if len(objs[0]["result"]) > 0:
                newState = (objs[0]["result"][0][1])
                
                if event.firstTime == 1:
                    event.state = newState
                    event.firstTime = 0   
                else:
                    if event.state != newState:
                        if(newState == 1):
                            message = event.name + " Event is active"
                        else:
                            message = event.name + " Event is has become unactive"
                        event.state = newState
                        print message
                    else:
                        #print "same state"
                        pass
                print 'Event:',event.name, ': Current State:',event.state
            else:
                print 'Event:',event.name, ': Current State: * Data Rule does not have state'
        except:
            print 'Exception getting initial Event status'
print ''

#
# Optional - Run while loop that prints out event state changes
#
loop=True
if loop==True:
    print 'Run loop to poll for changes to the event states (default 5 second poll interval)'
    print 'Use Python keyboard command to end script (Ctrl-c for example)'
while loop==True:
    try:
        for event in DataRuleList:
            if event.ruletype == "logic":
                ARGUMENTS = [event.rid,[]]
                PROCEDURE = "read"
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
                s.send('Connection: Close \r\n')
                body = json_rpc
                s.send('Content-Length: '+ str(len(body)) +'\r\n\r\n')
                s.send(body)

                data = s.recv(1024)
                #print 'Received Http Packet: \r\n', str(data)
                response = data.split('\r\n\r\n')
                #print 'Response Message:', response[1]

                objs = json.loads(response[1])
                try:
                    if len(objs[0]["result"]) > 0:
                        newState = (objs[0]["result"][0][1])
                        
                        if event.firstTime == 1:
                            event.state = newState
                            event.firstTime = 0
                            if(newState == 1):
                                message = event.name + ": Event is now active"
                            else:
                                message = event.name + ": Event is has become unactive"
                            event.state = newState
                            print message
                        else:
                            if event.state != newState:
                                if(newState == 1):
                                    message = event.name + ": Event is now active"
                                else:
                                    message = event.name + ": Event is has become unactive"
                                event.state = newState
                                print message
                            else:
                                #print "same state"
                                pass
                        #print 'Event:',event.name, ': Current State:',event.state
                    else:
                        #print 'Event:',event.name, ': Current State: * Data Rule does not have state'
                        pass
                except:
                    print 'Exception getting Event status'
    except:
        print 'Loop exception, quiting'
        loop=False
    time.sleep(5)
    
print 'Done. Ending Application.'
s.close()


