#import vArmour_dev
from vArmour_dev import *
from userlog import *
import traceback

class ep(vArmour_dev):
    def __init__(self, ip, user="varmour", passwd="vArmour123", timeout=10):
        #(filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        #self.name = text[:text.find('=')].strip()
        #print(self.name)
        vArmour_dev.__init__(self,ip,user,passwd,timeout)

    def config(self,cmds):
        userlog("DEBUG","EP don't support config mode!, exit...")
        return(1)

if __name__ == "__main__":
    import userlog
    userlog.debug = 1
    from userlog import *
    userlog("INFO","vArmour dircetor")
    dut2 = ep("10.11.120.63")

    dut2.config("")

    #dut.connect()
    #dut.disconnect()
