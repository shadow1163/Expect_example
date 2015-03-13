#! /usr/bin/env python
## chocolate main

import sys,os
import re


path = os.path.dirname(__file__)
sys.path.insert(0,path + '/vArmour_dev')

from director import *

print("==================================\nvArmour chocolate configure tool\n==================================")
print(len(sys.argv))
if len(sys.argv) < 3:
    print("usage:python main.py <director ip> <epi fabric ip>") 
    exit(0)
print("director_ip :%s, fabric_ip_ep : %s" % (sys.argv[1],sys.argv[2]))
director_ip = sys.argv[1]
ep1_fip = sys.argv[2]

#ssh to device
dut = director(director_ip)
dut.connect()

#get ep_id of epi fabric ip
result = dut.normal('show chassis epi')
ep1_str = '([\w-]+)\s+([\w-]+)\s+([\d-]+)\s+\*?\s+([\w-]+)\s+(%s/\d+)\s+(\d+\.\d+\.\d+\.\d+/\d+)' % ep1_fip
ep1_re = re.search(ep1_str,result)
if ep1_re is None:
    print("don't find ep1")
    exit(0)
ep1_id = ep1_re.group(3)
print('\n=====================')
print("EP id is %s" % ep1_id)
print('=====================')
dut.disconnect()
