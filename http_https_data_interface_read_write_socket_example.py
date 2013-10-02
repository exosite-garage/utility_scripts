#==============================================================================
# http_https_data_interface_read_write_socket.py
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
  Exosite HTTP and HTTPS POST/GET REST API example (HELLO WORLD!) using socket
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

import socket
import sys
import ssl
import urllib
import time

cik = 'PUTYOURCIKHERE'


print '========================================================================'
print 'HTTP REST API DEMO. Using CIK ', cik
print '========================================================================'
print '\r\n'

print '=================='
print 'POST - HTTP'
print '=================='

postparams = 'message=hello world!&number=1'  #Dataports have alias's 'message' and 'number'
postparams = urllib.quote(postparams,safe='=&?') #Python specific to encode the content params
content = postparams

# Note: This example is building a large string to send over the socket, this could be done
# instead line by line.  For purposes of printing out the request, it is done this way.

request_packet = ''
request_packet += 'POST /api:v1/stack/alias HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-CIK: '+cik+'\r\n'
request_packet += 'Connection: Close \r\n'
request_packet += 'Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n'
request_packet += 'Content-Length: '+ str(len(content)) +'\r\n'
request_packet += '\r\n' # Must have blank line here
request_packet += content # Must be same size as Content-Length specified

print '--REQUEST:-----------------------'
print str(request_packet)
print '---------------------------------'

# OPEN SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('m2.exosite.com', 80))
# SEND REQUEST
s.send(request_packet)
# RECEIVE RESPONSE
data = s.recv(2048)
# CLOSE SOCKET
s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data),
print '---------------------------------'
print '(Note: You should see a response of "HTTP/1.1 204 No Content" if this works correctly)'
print '\r\n\r\n'


print '=================='
print 'GET - HTTP'
print '=================='

getparams = '?message&number' # Get dataports with alias's 'message' and 'number'
getparams = urllib.quote(getparams,safe='=&?') #Python specific to encode the url params

# Note: This example is building a large string to send over the socket, this could be done
# instead line by line.  For purposes of printing out the request, it is done this way.

request_packet = ''
request_packet += 'GET /api:v1/stack/alias' + getparams +' HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-CIK: '+cik+'\r\n'
request_packet += 'Connection: Close\r\n'
request_packet += 'Accept: application/x-www-form-urlencoded; charset=utf-8\r\n'
request_packet += '\r\n' # Must have blank line

print '--REQUEST:-----------------------'
print str(request_packet),
print '---------------------------------'

# OPEN SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('m2.exosite.com', 80))
# SEND REQUEST
s.send(request_packet)
# RECEIVE RESPONSE
data = s.recv(1024)
# CLOSE SOCKET
s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data)
print '---------------------------------'
print '(Note: You should see a response of "HTTP/1.1 200 OK" if this works correctly)'
print '(Note: Some string data in the response may need formating, it is urlencoded)'
print '\r\n\r\n'


time.sleep(1) # make sure 1 second before writing to the data sources



print '========================================================================'
print 'HTTPS REST API DEMO. Using CIK ', cik
print '========================================================================'
print '\r\n'

print '=================='
print 'POST - HTTPS'
print '=================='

postparams = 'message=hello world!&number=1'  #Dataports have alias's 'message' and 'number'
postparams = urllib.quote(postparams,safe='=&?') #Python specific to encode the content params
content = postparams

# Note: This example is building a large string to send over the socket, this could be done
# instead line by line.  For purposes of printing out the request, it is done this way.

request_packet = ''
request_packet += 'POST /api:v1/stack/alias HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-CIK: '+cik+'\r\n'
request_packet += 'Connection: Close \r\n'
request_packet += 'Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n'
request_packet += 'Content-Length: '+ str(len(content)) +'\r\n'
request_packet += '\r\n' # Must have blank line here
request_packet += content # Must be same size as Content-Length specified

print '--REQUEST:-----------------------'
print str(request_packet)
print '---------------------------------'

# OPEN SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect(('m2.exosite.com', 443))
# SEND REQUEST
ssl_s.send(request_packet)
# RECEIVE RESPONSE
data = ssl_s.recv(1024)
# CLOSE SOCKET
ssl_s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data),
print '---------------------------------'
print '(Note: You should see a response of "HTTP/1.1 204 No Content" if this works correctly)'
print '\r\n\r\n'




print '=================='
print 'GET - HTTPS'
print '=================='
getparams = '?message&number' # Get dataports with alias's 'message' and 'number'
getparams = urllib.quote(getparams,safe='=&?') #Python specific to encode the url params

# Note: This example is building a large string to send over the socket, this could be done
# instead line by line.  For purposes of printing out the request, it is done this way.

request_packet = ''
request_packet += 'GET /api:v1/stack/alias' + getparams +' HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-CIK: '+cik+'\r\n'
request_packet += 'Connection: Close\r\n'
request_packet += 'Accept: application/x-www-form-urlencoded; charset=utf-8\r\n'
request_packet += '\r\n' # Must have blank line

print '--REQUEST:-----------------------'
print str(request_packet),
print '---------------------------------'

# OPEN SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect(('m2.exosite.com', 443))
# SEND REQUEST
ssl_s.send(request_packet)
# RECEIVE RESPONSE
data = ssl_s.recv(1024)
# CLOSE SOCKET
ssl_s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data)
print '---------------------------------'
print '(Note: You should see a response of "HTTP/1.1 200 OK" if this works correctly)'
print '(Note: Some string data in the response may need formating, it is urlencoded)'
print '\r\n\r\n'
