#! /usr/bin/env python

import sys
import pexpect
import logging
import re

formatter = 'WatchGuard AP %(levelname)s %(module)s:%(pathname)s:%(funcName)s:%(lineno)d - %(message)s'
logging.basicConfig(format = formatter, level=logging.INFO)
logger = logging.getLogger()

class WatchGuard_AP:
	HostIP = None
	SNIP = None
	SNPort = None
	Name = None
	Model = None
	Timeout = 30,
	CLIMode = 'telnet'

	spawn = None
	shell_prompt = r'[\w\-\_]+@[^ ]+[#][ \t]*$'
	def __init__(self,HostIP = None,\
			  SNIP = None,\
			  SNPort = None,\
			  Name = None,\
			  Model = None,\
			  Timeout = 30,\
			  CLIMode='telnet'):
		self.HostIP = HostIP
		self.SNIP = SNIP
		self.SNPort = SNPort
		self.Name = Name
		self.Model = Model
		self.Timeout = Timeout
		self.CLIMode = CLIMode

	def __del__(self):
		self.disconnect()
	def connect_cli(self):
		conn_cmd = ''
		if self.CLIMode == 'telnet':
			logger.debug("using \"telnet\" to connect WatchGuard AP")
			conn_cmd = 'telnet '
			if self.SNIP == None or self.SNPort == None:
				logger.error("Please transfer SNIP and SNPort!!!")
				return("Nok")
			conn_cmd += ("%s %s" %(self.SNIP,self.SNPort))
		elif self.CLIMode == 'ssh':
			logger.debug("using \"ssh\" to connect WatchGuard AP")
			conn_cmd = 'ssh'
			if self.HostIP == None:
				logger.error("Please transfer HostIP!!!")
				return("Nok")
			conn_cmd += ("%s %s" %(self.HostIP))
		else:
			logger.warning("So far, AP just support telnet, Please using telnet to connect AP, Thanks.")
			return("Nok")
		self.spawn = pexpect.spawn(conn_cmd,timeout = self.Timeout)
		self.spawn.logfile_read = sys.stdout
		#self.spawn.logfile_send = sys.stdout

		while True:
			index = self.spawn.expect([self.shell_prompt,'go to the Suspend Menu',pexpect.TIMEOUT,pexpect.EOF])
			if index == 0:
				break
			elif index == 1:
				self.spawn.sendline('\r\r\r')
			elif index >= 2:
				logger.error("Failed to login to AP %s using cmd \"%s\"" % (self.Name, conn_cmd))
		logger.debug("login to %s successfully" % self.Name)

	def shell_cmd(self,cmd):
		if self.spawn == None:
			self.connect_cli()
		result = ''
		if type(cmd) == type(""):
			try:
				self.spawn.sendline(cmd)
			except pexpect.TIMEOUT or pexpect.EOF:
				logger.error("execute \"%s\" timeout" % cmd)
				return(result)
			self.spawn.expect(cmd)
			self.spawn.expect(self.shell_prompt)
			result += self.spawn.after
			result += cmd
			result += self.spawn.before
		elif type(cmd) == type([]):
			for cmd_line in cmd:
				try:
					self.spawn.sendline(cmd_line)
				except pexpect.TIMEOUT or pexpect.EOF:
					logger.error("execute \"%s\" timeout" % cmd_line)
					return(result)
				self.spawn.expect(cmd)
				self.spawn.expect(self.shell_prompt)
				result += self.spawn.after
				result += cmd_line
				result += self.spawn.before
		#logger.debug("run cmd \"%s\"\nresult:\"%s\"" %(cmd,result))
		return(result)
		
	def disconnect(self):
		if self.spawn == None:
			return('')
		if self.spawn.isalive():
			logger.debug("disconnect %s" % self.Name)
			self.spawn.close()
			
	def iwconfig(self):
		rt = {}
		result = self.shell_cmd('iwconfig')
		rc = re.compile('ath\d+.*?\n\s*\n',re.I|re.S)
		aths = rc.findall(result)
		for ath in aths:
			ath_match = re.match(r'(ath\d+).*?ESSID:"(.*?)".*?Frequency:([\d.]+) GHz.*?Tx-Power:([\d+]).*?Encryption key:([\w]+)', ath, re.M|re.I|re.S)
			if ath_match:
				ath_name = ath_match.group(1)
				rt[ath_name] = {}
				rt[ath_name]['result'] = ath
				rt[ath_name]['ESSID'] = ath_match.group(2)
				rt[ath_name]['Frequency'] = ath_match.group(3)
                rt[ath_name]['Tx-Power'] = ath_match.group(4)
                rt[ath_name]['Encryption-key'] = ath_match.group(5)
			else:
				print("Error to find")

if __name__ == "__main__":
	AP1 = WatchGuard_AP(SNIP = '10.138.255.77',SNPort = '5015')
	AP1.connect_cli()
	AP1.shell_cmd(["ls","ifconfig"])
	AP1.disconnect()
