#==============================================================================
# http_https_data_interface_read_write.py
# Python script that tests https and http socket level calls
# for basic data interface API to Exosite One Platform
#
#==============================================================================
## Tested with python 2.6.5
##
## Copyright (c) 2012, Exosite LLC
## All rights reserved.
##
##
## Redistribution and use in source and binary forms, with or without 
## modification, are permitted provided that the following conditions are met:
##
##    * Redistributions of source code must retain the above copyright notice,
##      this list of conditions and the following disclaimer.
##    * Redistributions in binary form must reproduce the above copyright 
##      notice, this list of conditions and the following disclaimer in the
##      documentation and/or other materials provided with the distribution.
##    * Neither the name of Exosite LLC nor the names of its contributors may
##      be used to endorse or promote products derived from this software 
##      without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
## POSSIBILITY OF SUCH DAMAGE.

""" 
  Exosite HTTP and HTTPS POST/GET REST API example (HELLO WORLD!) using http
  level calls
"""

""" 
  Directions:
  1) Have an Exosite Portals account
  2) Add a new Device client to your portal.  Click on it to get it's CIK (KEY)
  3) Add the CIK below where it says 'PUTYOURCIKHERE'. (inside of the quotes)
  4) On your portal, add two data sources.  This script does not auto-create the data sources.
      Data Source 1 should be called 'message', type is string, resource is 'message'
      Data Source 2 should be called 'number', type is integer, resource is 'number'
  5) Run this python script in Python 2.6.5 or higher.
  6) Assuming your computer has an active network connection, you should see data sent to
      these data sources on your portal.  The script runs only once.  It should also print out
      what it sent, since it is doing a 'read' after the 'write'.
  
"""

import urllib 
import httplib

cik = 'PUTYOURCIKHERE'
server = 'm2.exosite.com'
SHOW_DEBUG = 0 #Set to 1 for verbose debug output of connection or set to 0 to disable

print '========================================================================'
print 'HTTP REST API DEMO. Using CIK ', cik
if SHOW_DEBUG == 1:
  print 'DEBUG CONNECTION OUTPUT ENABLED'
print '========================================================================'
print '\r\n'

http_port = 80
url = '/api:v1/stack/alias' 
params = urllib.urlencode({'message': 'hello world!', 'number': 1 })  #Dataport have alias 'message' and 'number'
headers = {'X-Exosite-CIK': cik, 'content-type': 'application/x-www-form-urlencoded; charset=utf-8'}


print '=================='
print 'POST'
print '=================='
print 'Server:', server
print 'Port:', http_port
print 'URL: ', url
print 'Data: ', params
print ' '
conn = httplib.HTTPConnection(server,http_port) 

if SHOW_DEBUG == 1:
  conn.set_debuglevel(1)
  print 'DEBUG OUTPUT:'
  print '------------------------'
  print '--DEBUG MESSAGE OUTPUT--'

conn.request("POST",url,params,headers)

if SHOW_DEBUG == 1:
  print '--DEBUG RESPONSE OUTPUT--'
  
response = conn.getresponse();

if SHOW_DEBUG == 1:
  print '------------------------'
  
print 'response: ',response.status,response.reason 
data = response.read()  #Expected Resposne is 204 No Content (since you are writing data, nothing to return)
end = data.find('<')
if -1 == end: end = len(data)
print '(Note: You should see a response of "204 No Content" if this works correctly)'
conn.close()

print '\r\n\r\n'
url = '/api:v1/stack/alias?message&number'
headers = {'Accept':'application/x-www-form-urlencoded; charset=utf-8','X-Exosite-CIK':cik}
print '=================='
print 'GET'
print '=================='
print 'Server:', server
print 'Port:', http_port
print 'URL: ', url
print ' '

conn = httplib.HTTPConnection(server,http_port)

if SHOW_DEBUG == 1:
  conn.set_debuglevel(1)
  print 'DEBUG OUTPUT:'
  print '------------------------'
  print '--DEBUG MESSAGE OUTPUT--'

conn.request("GET",url,"",headers)

if SHOW_DEBUG == 1:
  print '--DEBUG RESPONSE OUTPUT--'

response = conn.getresponse();

if SHOW_DEBUG == 1:
  print '------------------------'
  
print 'response: ',response.status,response.reason
data = response.read()
print 'response data:', urllib.unquote(data)


conn.close()

print '\r\n'
print '\r\n'

print '========================================================================'
print 'HTTPS REST API DEMO. Using CIK ', cik
if SHOW_DEBUG == 1:
  print 'DEBUG CONNECTION OUTPUT ENABLED'
print '========================================================================'
print '\r\n'

https_port = 443
url = '/api:v1/stack/alias' 
params = urllib.urlencode({'message': 'hello world!', 'number': 1 })  #Dataport have alias 'message' and 'number'
headers = {'X-Exosite-CIK': cik, 'content-type': 'application/x-www-form-urlencoded; charset=utf-8'}


print '=================='
print 'POST'
print '=================='
print 'Server:', server
print 'Port:', https_port
print 'URL: ', url
print 'Data: ', params
print ' '
conn = httplib.HTTPSConnection(server,https_port)

if SHOW_DEBUG == 1:
  conn.set_debuglevel(1)
  print 'DEBUG OUTPUT:'
  print '------------------------'
  print '--DEBUG MESSAGE OUTPUT--'

conn.request("POST",url,params,headers)

if SHOW_DEBUG == 1:
  print '--DEBUG RESPONSE OUTPUT--'
  
response = conn.getresponse();

if SHOW_DEBUG == 1:
  print '------------------------'
  
print 'response: ',response.status,response.reason 
data = response.read() #Expected Resposne is 204 No Content (since you are writing data, nothing to return)
end = data.find('<')
if -1 == end: end = len(data)
print '(Note: You should see a response of "204 No Content" if this works correctly)'

conn.close()

print '\r\n\r\n'
url = '/api:v1/stack/alias?message&number'
headers = {'Accept':'application/x-www-form-urlencoded; charset=utf-8','X-Exosite-CIK':cik}
print '=================='
print 'GET'
print '=================='
print 'Server:', server
print 'Port:', https_port
print 'URL: ', url
print ' '

conn = httplib.HTTPSConnection(server,https_port)

if SHOW_DEBUG == 1:
  conn.set_debuglevel(1)
  print 'DEBUG OUTPUT:'
  print '------------------------'
  print '--DEBUG MESSAGE OUTPUT--'

conn.request("GET",url,"",headers)

if SHOW_DEBUG == 1:
  print '--DEBUG RESPONSE OUTPUT--'

response = conn.getresponse();

if SHOW_DEBUG == 1:
  print '------------------------'
  
print 'response: ',response.status,response.reason
data = response.read()
print 'response data:', urllib.unquote(data)


conn.close()

