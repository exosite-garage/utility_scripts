#==============================================================================
# http_https_data_interface_get_ip_socket.py
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
  Exosite HTTP and HTTPS GET IP API example using socket level calls
"""

""" 
  Directions:
  1) Run this code.
  
"""

import socket
import sys
import ssl


host = 'm2.exosite.com'


print '========================================================================'
print 'HTTP REST GET IP DEMO. '
print '========================================================================'
print '\r\n'

http_port = 80
url = "/ip"

print '=================='
print 'GET'
print '=================='
print 'Server:', host
print 'Port:',http_port
print 'URL:',url
print ' '

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, http_port))
s.send('GET '+url+' HTTP/1.1\r\n')
s.send('Host: '+host+'\r\n')
s.send('Connection: Close \r\n')
s.send('Accept: application/x-www-form-urlencoded; charset=utf-8\r\n')
s.send('\r\n')
data = s.recv(1024)
s.close()
print 'Received: \r\n', str(data)

print '\r\n\r\n'

print '\r\n'
print '\r\n'


print '========================================================================'
print 'HTTPS REST GET IP DEMO.'
print '========================================================================'
print '\r\n'

https_port = 443
url = '/ip' 

print '=================='
print 'GET'
print '=================='
print 'Server:', host
print 'Port:',https_port
print 'URL:',url
print ' '

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_s = ssl.wrap_socket(s)
ssl_s.connect((host, https_port))
ssl_s.send('GET '+url+' HTTP/1.1\r\n')
ssl_s.send('Host: '+host+'\r\n')
ssl_s.send('Connection: Close \r\n')
ssl_s.send('Accept: application/x-www-form-urlencoded; charset=utf-8\r\n')
ssl_s.send('\r\n')
data = ssl_s.recv(1024)
ssl_s.close()
print 'Received: \r\n', str(data)

print '\r\n\r\n'

print '\r\n'
print '\r\n'
