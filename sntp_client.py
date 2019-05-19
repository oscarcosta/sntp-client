#!/usr/bin/env python
# SNTP-Client adapted from 'Writing an SNTP client' 
# https://subscription.packtpub.com/book/networking_and_servers/9781786463999/1/ch01lvl1sec22/writing-an-sntp-client

import socket
import struct
import sys
import time

NTP_SERVER = "0.uk.pool.ntp.org"
TIME1970 = 2208988800 # 1970-01-01 00:00:00

rtt_off_array = [(1000000, 0)] * 8 # array of recent (RTT,offset) 

def sntp_client(i):
  client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client.settimeout(2.5)
  data = '\x1b' + 47 * '\0'
  try:
    client_t0 = time.time() # client sent time
    client.sendto(data.encode('utf-8'), (NTP_SERVER, 123))
    data, address = client.recvfrom(1024)
    client_t3 = time.time() # client receiv time
    if data:
      data = struct.unpack('!12I', data)
    
      server_t1 = (data[8] - TIME1970)  # server receiv time
      server_t2 = (data[10] - TIME1970) # server sent time
      
      # calculate RTT and offset
      delay = (server_t1 - client_t0) - (server_t2 - client_t3)
      offset = ((server_t1 - client_t0) + (server_t2 - client_t3)) / 2

      # calculate "smoothed offset"
      rtt_off_array[i%8] = (delay, offset)
      min_offset = min(rtt_off_array, key = lambda t:t[0])[1]
      
      # print report
      print('Client Time: %s' % time.ctime(client_t3))
      print('Adjust Time: %s' % time.ctime(client_t3 + offset))
      print('Offset: %s' % min_offset)
      
      # print metadata for graphs
      print('\n(rtt, off): %s %s' % (delay, offset))
      print('timestamps: %s %s %s %s' % (client_t0, server_t1, server_t2, client_t3))
  except socket.timeout as e:
    print(e)

if __name__ == '__main__':
  i = 0
  while True:
    time.sleep(10)
    print('\nIter %s' % i)
    sntp_client(i)
    i += 1
