#! /usr/bin/env python


import sys,re
import pexpect
import copy
import traceback
from userlog import *

class vArmour_dev:

    mode_index = ["shell","config","normal"]
    mode_change = {"normal->config":"configure","normal->shell":"debug shell","config->normal":"exit","config->shell":"do debug shell","shell->normal":"cli","shell->config":"cli"};
    except_list = ['<press any key to continue, "q" to quit>','Error: Illegal parameter.','\[sudo\] password for %self.user%:']
    except_action = ['','control c','%self.passwd%']

    def __init__(self, ip, user="varmour", passwd="vArmour123", timeout=200):
        # get device name
        try:
            (filename,line_number,function_name,text)=traceback.extract_stack()[-3]
        except:
            text = ""
        if re.search(".*=.*",text) is None:
            (filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        self.__name__ = text[:text.find('=')].strip()
        print(self.__name__)

        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.timeout = timeout
        self.normal_prompt = r'[\w\-\_]+@[\w\-\_]+(#ROOT|#)(\(M|\(PB|\(B|)(|\))?>[ \t]*$'
        self.config_prompt = r'[\w\-\_]+@[\w\-\_]+(#ROOT|#)\(config.*\)(\(M\(PB|\(B|)(|\))?>[ \t]*$'
        self.shell_prompt = r'[\w\-\_]+@[^ ]+[#\$][ \t]*$'
        self.__class__.except_action = self.replace_var(self.__class__.except_action)
        userlog("DEBUG","Init vArmour %s successfully." % str(self.__name__))
    
    def connect(self):
        userlog("DEBUG","connect %s" % self.__name__)
        try:
            if int(sys.version_info[0]) == 3:
                self.spawn = pexpect.spawnu("ssh -l %s %s" % (self.user, self.ip), timeout = self.timeout)
            else:
                self.spawn = pexpect.spawn("ssh -l %s %s" % (self.user, self.ip), timeout = self.timeout)
        except:
            userlog("ERROR","don't connect dev %s using ip %s user %s" % (self.__name__, self.ip, self.user))
            return(0)
        #self.spawn.logfile = sys.stdout
        self.spawn.logfile_read = sys.stdout
        #self.spawn.logfile_send = sys.stdout

        ## login to dev
        while True:
            index = self.spawn.expect([self.normal_prompt,r'\(yes/no\)',r'assword:',pexpect.TIMEOUT,pexpect.EOF])
            if index == 0: 
                break
            elif index == 1: 
                self.spawn.sendline('yes')
            elif index == 2: 
                self.spawn.sendline(self.passwd)
            elif index >= 3:
                userlog('ERROR','Failed to login to dev %s using ip %s user %s' % (self.__name__, self.ip, self.user))
                self.spawn.close()
                return(0)

        userlog("INFO","login successfully")

    def normal(self, cmd):
        if not self.goto_mode("normal"):
            userlog("ERROR","don't input %s on normal" % cmd)
            return(0)
        result = ""
        if type(cmd) == type(""):
            try:
                self.spawn.sendline(cmd)
            except pexpect.TIMEOUT or pexpect.EOF:
                userlog("ERROR","don't configure %s" % cmd)
                return(0)
            self.spawn.expect(cmd)
            result += self.spawn.before
            result += self.spawn.after
            result += self.expect(self.normal_prompt)
        elif type(cmd) == type([]):
            for line in cmd:
                try:
                    self.spawn.sendline(line)
                except pexpect.TIMEOUT or pexpect.EOF:
                    userlog("ERROR","don't configure %s" % cmd)
                    return(0)
                self.spawn.expect(line)
                result += self.spawn.before
                result += self.spawn.after
                result += self.expect(self.normal_prompt)
        #userlog("DEBUG","before: %s" % self.spawn.before)
        #userlog("DBEUG","after: %s" % self.spawn.after)
        return(result)

    def config(self, cmd):
        if not self.goto_mode("config"):
            userlog("ERROR","don't configure %s" % cmd)
            return(0)
        result = ""
        if type(cmd) == type(""):
            try:
                self.spawn.sendline(cmd)
            except pexpect.TIMEOUT or pexpect.EOF:
                userlog("ERROR","don't configure %s" % cmd)
                return(0)
            self.spawn.expect(cmd)
            result += self.spawn.before
            result += self.spawn.after
            result += self.expect(self.config_prompt)
        elif type(cmd) == type([]):
            for line in cmd:
                try:
                    self.spawn.sendline(line)
                except pexpect.TIMEOUT or pexpect.EOF:
                    userlog("ERROR","don't configure %s" % cmd)
                    return(0)
                self.spawn.expect(line)
                result += self.spawn.before
                result += self.spawn.after
                result += self.expect(self.config_prompt) 
        #self.spawn.expect(self.config_prompt)
        #userlog("DEBUG","before: %s" % self.spawn.before)
        #userlog("DBEUG","after: %s" % self.spawn.after)
        return(result)

    def shell(self,cmd):
        if not self.goto_mode("shell"):
            userlog("ERROR","don't enter shell mode")
            return(0)
        try:
            self.spawn.sendline(cmd)
        except pexpect.TIMEOUT or pexpect.EOF:
            userlog("ERROR","don't execute \"%s\"" % cmd)
            return(0)
        result = self.expect(self.shell_prompt)

        return(result)

    def goto_mode(self, mode):
        old_mode = self.get_mode()
        if not old_mode:
            userlog("ERROR","don't goto mode %s" % mode)
            return(0)
        if old_mode != mode:
            for i in range(1,3):
                userlog("DEBUG","change %d time(s)" % i)
                try:
                    self.spawn.sendline(self.__class__.mode_change["%s->%s" % (old_mode,mode)])
                except pexpect.TIMEOUT or pexpect.EOF:
                    userlog("ERROR","don't goto mode %s" % mode)
                    return(0)
                
                index = self.spawn.expect([self.shell_prompt,self.config_prompt,self.normal_prompt,'Input password:'])
                if index == 3:
                    self.spawn.sendline("varmourrock")
                    self.spawn.sendline("\n")
                    index = self.spawn.expect([self.shell_prompt,self.config_prompt,self.normal_prompt])
                if self.__class__.mode_index[index] == mode:
                    break
                b_mode = self.get_mode()
                if b_mode == mode:
                    break
        userlog("DEBUG","goto mode %s successfully" % mode)
        return(1)

    def get_mode(self):
        if not self.spawn.isalive():
            userlog("ERROR","can't get spawn")
            return(0)
        try:
            self.spawn.sendline('\n')
        except pexpect.TIMEOUT or pexpect.EOF:
            userlog("ERROR","don't send enter")
            return(0)
        index = self.spawn.expect([self.shell_prompt,self.config_prompt,self.normal_prompt])
        return(self.__class__.mode_index[index])
    def expect(self,expect_list):
        _expect_list_ = copy.deepcopy(self.__class__.except_list)
        count_sys = len(_expect_list_)
        result = ""
        if expect_list:
            if type(expect_list) == type(""):
                _expect_list_.append(expect_list)
                count_list = 1
            elif type(expect_list) == type([]):
                 _expect_list_ += expect_list
                 count_list = len(expect_list)
        else:
            count_list = 0
        _expect_list_ = self.replace_var(_expect_list_)
        _expect_list_.append(pexpect.TIMEOUT)
        _expect_list_.append(pexpect.EOF)
        userlog("DEBUG","list is %s" % _expect_list_)
        while True:
            index = self.spawn.expect(_expect_list_)
            userlog("DEBUG","count_sys = %d, index = %d, count_list = %s" % (count_sys,index,count_list))
            if index < count_sys:
                result += self.spawn.before
                self.send_action(self.__class__.except_action[index])
            elif index >= (count_list + count_sys):
                userlog("ERROR","Timeout or EOF")
                return(0)
            elif count_sys <= index < (count_list + count_sys):
                #userlog("DBUEG","=================\n%s%s\n==============" % (self.spawn.after,self.spawn.before))
                #return("%s%s" % (self.spawn.after,self.spawn.before))
                result += self.spawn.before
                #return("%s%s" % (self.spawn.after,result))
                return("%s" % (result))
    
    def replace_var(self,expect_list):
        __expect_list__ = copy.deepcopy(expect_list)
        userlog("DEBUG","list is %s" % __expect_list__)
        for i in range(0,len(__expect_list__)):
            #userlog('DEBUG',"item is %s" % __expect_list__[i])
            var_list = re.findall('%(self\.\w+)%',__expect_list__[i],re.I)
            if len(var_list) > 0 :
                for j in range(0,len(var_list)):
                    try:
                        value = eval(var_list[j])
                    except:
                        userlog("ERROR","find var %s error" % re_m.group(1))
                        return(0)
                    __expect_list__[i] = re.sub('%' + var_list[j] + '%',value,__expect_list__[i])
            #userlog('DEBUG',__expect_list__[i])
        userlog('DEBUG',__expect_list__)
        return(__expect_list__)

    def send_action(self,action):
        ## send ctrl + ([a-z]) command
        re_m = re.search('control (\w)',action,re.I)
        if re_m is not None:
            userlog("DEBUG","find control")
            self.spawn.sendcontrol(re_m.group(1))
            self.spawn.sendcontrol('\n')
            self.spawn.sendcontrol('\n')
        else:
            userlog("DEBUG","Not find control")
            self.spawn.sendline(action)

    def disconnect(self):
        userlog("INFO","disconnect %s" % self.__name__)
        if self.spawn.isalive():
            self.spawn.close()
        return(1)


if __name__ == "__main__":
    print("vArmour director")
    
    import userlog
    print(userlog.debug)
    userlog.debug = 0
    from userlog import *
    dut = vArmour_dev("10.11.120.61")
    dut.connect()
    #dut.expect("")
    #print(dut.get_mode())
    #print(dut.goto_mode("config"))
    dut.config("do show running-config")
    print("\n============================" + dut.normal("show running-config") + "======\n")
    #print('111111 %s  222' % dut.config("send error command"))
    #dut.send_action("control c")
    cmds = []
    cmds.append("set zone test type L3")
    cmds.append("set zone test1 type L2")
    #cmds.append("set zone test2")
    cmds.append("commit")
    userlog("INFO",dut.config(cmds))
    uncmds = []
    uncmds.append("unset zone test")
    uncmds.append("unset zone test1")
    uncmds.append("commit")
    userlog("INFO",dut.config(uncmds))
    #dut.normal("show running-config")
    #dut.config("commit")
    #print(dut.goto_mode("shell"))
    #print(dut.shell("ifconfig"))
    #print(dut.shell("sudo cat /opt/varmour/conf/setup.ini"))
    #print(dut.shell("sudo reboot"))
    #print(dut.replace_var(["%self.user%"]))
    #print(dut.replace_var(vArmour_dev.except_list))
    dut.disconnect()



