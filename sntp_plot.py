#!/usr/bin/env python

import re
import matplotlib.pyplot as plt
import seaborn as sns

# class to match the data patterns
class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
        self.rematch = re.match(regexp, self.matchstring)
        return bool(self.rematch)

    def group(self,i):
        return self.rematch.group(i)
        
# arrays to store the different data
timestamp_array = []
rtt_array = []
offset_array = []
success_timeout_array = []

# read file parsing the content
lineList = list()
with open("sntp_result.txt") as file:
  for line in file:
    m = REMatcher(line)
    
    if m.match(r"^timestamps:\s(.+)"):
      timestamp_array.append(m.group(1).split())

    elif m.match(r"^\(rtt, off\):\s(.+)"):
      rtt_offset = m.group(1).split()
      rtt_array.append(float(rtt_offset[0]))
      offset_array.append(float(rtt_offset[1]))
    
    if m.match(r"^(timestamps|timed out)"):
      success_timeout_array.append(m.group(1))

#print(*offset_array, sep = ", ")

# Offset histogram
sns.distplot(offset_array, hist = True, kde = False)
plt.title('SNTP offset histogram')
plt.xlabel('offset')
plt.show()
#plt.savefig('offset_hist.png')

# RTT and Offset
plt.title('RTT and Offset')
plt.plot(rtt_array, marker='', color='blue', linewidth=1, label="RTT")
plt.plot(offset_array, marker='', color='olive', linewidth=1, label="Offset")
plt.show()
#plt.savefig('rtt_offset.png')

# Timeout
labels = 'Success', 'Timeout'
values = [success_timeout_array.count('timestamps'), success_timeout_array.count('timed out')]
plt.title('Success Rate')
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
#plt.savefig('timeout_pie.png')