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
    print("usage:python main.py <director ip> <epi1 fabric ip> <OG> <OR>") 
    exit(0)
print("director_ip :%s, fabric_ip_ep1 : %s, OG:%s, OR:%s" % (sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]))
director_ip = sys.argv[1]
try:
    ep1_fip = sys.argv[2]
except:
    ep1_fip = '192.168.0.42'
try:
    OG = sys.argv[3]
except:
    OG = 50

try:
    OR = sys.argv[4]
except:
    OR = 51

dut = director(director_ip)
dut.connect()
result = dut.normal('show chassis epi')
ep1_str = '([\w-]+)\s+([\w-]+)\s+([\d-]+)\*?\s+([\w-]+)\s+(%s/\d+)\s+(\d+\.\d+\.\d+\.\d+/\d+)' % ep1_fip
ep1_re = re.search(ep1_str,result)
if ep1_re is None:
    print("don't find ep1")
    exit(0)
ep1_id = ep1_re.group(3)
if (ep1_id == '2-5') :
    ep2_id = '3-5'
else :
    ep2_id = '2-5'

cmds = []
cmds.append('set policy name test from Intc to Intc')
cmds.append('set policy name test match source-address Any')
cmds.append('set policy name test match destination-address Any')
cmds.append('set policy name test match service ICMP-ANY')
cmds.append('set policy name test match service SSH')
cmds.append('set policy name test match service TELNET')
cmds.append('set policy name test match service TFTP')
cmds.append('set policy name test match service HTTP')
cmds.append('set policy name test match service HTTPS')
cmds.append('set policy name test match service FTP')
cmds.append('set policy name test match service DNS')
cmds.append('set policy name test match app-group VA::Any')
cmds.append('set policy name test action permit')
cmds.append('set chassis epi %s operation-mode inline' % ep1_id)
cmds.append('set chassis epi %s operation-mode inline' % ep2_id)
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1001' % (ep1_id,OG))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1002' % (ep1_id,OG))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1003' % (ep1_id,OG))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1005' % (ep1_id,OR))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1004' % (ep1_id,OR))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1005' % (ep2_id,OR))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1003' % (ep2_id,OG))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1004' % (ep2_id,OR))
cmds.append('set micro-segmentation epi %s segment %s micro-vlan 1002' % (ep2_id,OG))
cmds.append('commit')
dut.config(cmds)

dut.disconnect()
