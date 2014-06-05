#==============================================================================
# post_client_model_content_example.py
# Python script that tests creating and posting content files under a client model
# using Exosite's provision device management system.
#
#==============================================================================
## Tested with python 2.6.5
##
## Copyright (c) 2014, Exosite LLC
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
  Directions:
  1) Have an Exosite Whitelabel / Vendor account (<vendor>.exosite.com)
  2) Add a Client Model using whitelabel admin tools or API
  3) Add the Vendor Token below where it says 'VENDOR_TOKEN_HERE'. 
  4) Add Client Model id where is says 'CLIENT_MODEL_ID_HERE'.
  5) Run this python script in Python 2.6.5 or higher.
  6) Assuming your computer has an active network connection, you should see new 
    content posted under your client model.
  
"""

import socket
import sys
import ssl
import urllib
import time


CLIENT_MODEL = 'CLIENT_MODEL_ID_HERE'
VENDOR_TOKEN = 'VENDOR_TOKEN_HERE'


CONTENT_ID = 'testfile' + str(int(time.time())) #create new file each time for debug purposes
CONTENT_META = 'Test File'  #a description of the file, has no specific use or function
CONTENT_BLOB = 'content of testfile.\r\n' #actual content


print '========================================================================'
print 'POST CONTENT TO EXOSITE CLIENT MODEL  - VENDOR DEVICE MANAGEMENT DEMO'
print '========================================================================'
print '\r\n'

print '=================='
print 'GET CONTENT FOR THIS CLIENT MODEL: ' + CLIENT_MODEL
print '=================='

request_packet = ''
request_packet += 'GET /provision/manage/content/' + CLIENT_MODEL +'/' + ' HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-Token: '+VENDOR_TOKEN+'\r\n'
request_packet += 'Connection: Close \r\n'
request_packet += '\r\n' # Must have blank line here

print '--REQUEST:-----------------------'
print str(request_packet)
print '---------------------------------\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect(('m2.exosite.com', 443))
ssl_s.send(request_packet)
data = ssl_s.recv(1024)
ssl_s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data),
print '---------------------------------'

print '=================='
print 'CREATE CONTENT ID: ' + CONTENT_ID
print '=================='

content = 'id='+ urllib.quote_plus(CONTENT_ID) +'&meta=' + urllib.quote_plus(CONTENT_META) + '&protected=false'

request_packet = ''
request_packet += 'POST /provision/manage/content/' + CLIENT_MODEL +'/' + ' HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-Token: '+VENDOR_TOKEN+'\r\n'
request_packet += 'Connection: Close \r\n'
request_packet += 'Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n'
request_packet += 'Content-Length: '+ str(len(content)) +'\r\n'
request_packet += '\r\n' # Must have blank line here
request_packet += content

print '--REQUEST:-----------------------'
print str(request_packet)
print '---------------------------------\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect(('m2.exosite.com', 443))
ssl_s.send(request_packet)
data = ssl_s.recv(1024)
ssl_s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data),
print '---------------------------------'
print '(Note: You should see a response of "HTTP/1.1 205 Reset Content" if this works correctly)'


print '=================='
print 'UPLOAD CONTENT BLOB for ' + CONTENT_ID
print '=================='

content = (CONTENT_BLOB)

request_packet = ''
request_packet += 'POST /provision/manage/content/' + CLIENT_MODEL + '/'+ CONTENT_ID  + ' HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-Token: '+VENDOR_TOKEN+'\r\n'
request_packet += 'Connection: Close \r\n'
request_packet += 'Content-Type: text/plain\r\n'
request_packet += 'Content-Length: '+ str(len(content)) +'\r\n'
request_packet += '\r\n' # Must have blank line here
request_packet += content # Must be same size as Content-Length specified

print '--REQUEST:-----------------------'
print str(request_packet)
print '---------------------------------\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect(('m2.exosite.com', 443))
ssl_s.send(request_packet)
data = ssl_s.recv(1024)
ssl_s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data),
print '---------------------------------'
print '(Note: You should see a response of "HTTP/1.1 205 Reset Content" if this works correctly)'
print '\r\n\r\n'


print '=================='
print 'GET CONTENT AGAIN FOR THIS CLIENT MODEL: ' + CLIENT_MODEL
print '=================='

request_packet = ''
request_packet += 'GET /provision/manage/content/' + CLIENT_MODEL +'/' + ' HTTP/1.1\r\n'
request_packet += 'Host: m2.exosite.com\r\n'
request_packet += 'X-Exosite-Token: '+VENDOR_TOKEN+'\r\n'
request_packet += 'Connection: Close \r\n'
request_packet += '\r\n' # Must have blank line here

print '--REQUEST:-----------------------'
print str(request_packet)
print '---------------------------------\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect(('m2.exosite.com', 443))
ssl_s.send(request_packet)
data = ssl_s.recv(1024)
ssl_s.close()

# URL DECODE - If required
data = urllib.unquote_plus(data) # library specific to python
print '--RESPONSE:----------------------'
print str(data),
print '---------------------------------'


