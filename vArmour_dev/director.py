#import vArmour_dev
from vArmour_dev import *
from userlog import *
import traceback

class director(vArmour_dev):
    def __init__(self, ip, user="varmour", passwd="vArmour123", timeout=10):
        #(filename,line_number,function_name,text)=traceback.extract_stack()[-2]
        #self.name = text[:text.find('=')].strip()
        #print(self.name)
        vArmour_dev.__init__(self,ip,user,passwd,timeout)

    def get_session(self,*args,**kwargs):
        userlog('DEBUG','enter get_session function...')
        result = self.normal('show session detailed-info')
        userlog('DEBUG','===========%s===============' % result)
        return(result)

    def clear_session(self,*args,**kwargs):
        userlog('DEBUG','enter clear_session function...')
        try:
            self.normal('clear session')
        except:
            userlog("ERROR","Error to clear session!!")
            return(0)
        return(1)

    ######################################################
    # @brief check session
    #
    # @param     : data : dict
    #        data = {
    #            'dev_id' : device id, for example: director id is 1
    #            'session' : session_val,
    #            'vsys_id' : vsys id, default is 1
    #            'pol':   policy name,
    #            'proto': protocol, for example : 1, 6 ,default is \d
    #            'offload': the value of offload,for example : N, default is N
    #            'app': application name, for example: icmp/ssh
    #            'int_in' : ingre interface name
    #            'int_in_ai' : alias name of ingre interface,
    #            'in_src_ip' :  src ip ,
    #            'in_src_port': src port
    #            'in_dst_ip' : dst ip,
    #            'in_dst_port' : dst port,
    #            'in_packets' : the number of packets
    #            'int_out' : out interface name
    #            'int_out_ai' : alias name of out interface
    #            'out_dst_ip' : dst ip
    #            'out_dst_port' : dst port
    #            'out_src_ip' : src ip
    #            'out_src_port': src port,
    #            'out_packets': the number of packets
    #            }    
    #    example :
    #            data = {
    #                'dev_id' : 3,
    #                'session' : session_val,
    #                'vsys_id' : 1,
    #                'pol':   'vw_pol',
    #                'proto': 1,
    #                'offload': 'N',
    #                'app': 'icmp',
    #                'int_in' : 'vw1-1.1',
    #                'int_in_ai' : 'ge-3/0/2',
    #                'in_src_ip' : '1.1.1.2',
    #                'in_src_port': 3,
    #                'in_dst_ip' : '1.1.1.3',
    #                'in_dst_port' : '55085',
    #                'in_packets' : 1,
    #                'int_out' : 'vw1-2.1',
    #                'int_out_ai' : 'ge-3/0/3',
    #                'out_dst_ip' : '1.1.1.2',
    #                'out_dst_port' : 3,
    #                'out_src_ip' : '1.1.1.3',
    #                'out_src_port': 55085,
    #                'out_packets': 1
    #                
    # @example  : check_session(data)
    # @return: 
    #          Fail   : 0
    #          Sucess : 1
    #######################################################
    def check_session (self, data, *args, **kwargs) :
        userlog("INFO","check_session")
        
        if not 'session' in data :
            userlog("ERROR","Please input session information")
            return(0)
        
        if not 'vsys_id' in data :
            vsys_id = '\d'
        else :
            vsys_id = data['vsys_id']
    
        if not 'pol' in data :
            pol = '\w+'
        else :
            pol = data['pol']
    
        if not 'offload' in data :
            offload = 'N'
        else :
            offload = data['offload']
        
        if not 'app' in data :
            app = '[\w-]+'
        else :
            app    = data['app']
        
        if not 'int_in' in data :
            int_in = '[\/\w\-\.]+'
        else :
            int_in = data['int_in']
        
        if not 'int_in_ai' in data :
            int_in_ai = '[\/\w\-\.]+'
        else :
            int_in_ai = data['int_in_ai']
    
        if not 'in_src_ip' in data :
            in_src_ip = '[\d\.]+'
        else :
            in_src_ip = data['in_src_ip']
        
        if not 'in_src_port' in data :
            in_src_port = '\d+'
        else :
            in_src_port = data['in_src_port']
        
        if not 'in_dst_ip' in data :
            in_dst_ip = '[\d\.]+'
        else :
            in_dst_ip = data['in_dst_ip']
        
        if not 'in_dst_port' in data :
            in_dst_port = '\d+'
        else :
            in_dst_port = data['in_dst_port']
        
        if not 'in_packets' in data :
            in_packets = '\d+'
        else :
            in_packets = data['in_packets']
        
        if not 'int_out' in data :
            int_out = '[\/\w\-\.]+'
        else :
            int_out = data['int_out']
        
        if not 'int_out_ai' in data :
            int_out_ai = '[\/\w\-\.]+'
        else :
            int_out_ai = data['int_out_ai']
    
        if not 'out_dst_ip' in data :
            out_dst_ip = '[\d\.]+'
        else :
            out_dst_ip = data['out_dst_ip']
        
        if not 'out_dst_port' in data :
            out_dst_port = '\d+'
        else :
            out_dst_port = data['out_dst_port']
        
        if not 'out_src_ip' in data :
            out_src_ip = '[\d\.]+'
        else :
            out_src_ip = data['out_src_ip']
        
        if not 'out_src_port' in data :
            out_src_port = '\d+'
        else :
            out_src_port = data['out_src_port']
        
        if not 'proto' in data :
            proto = '\d+'
        else :
            proto = data['proto']
            proto = proto.upper()
            if proto == 'ICMP':
                proto = 1
            elif proto == 'SSH':
                proto = 6
                in_dst_port = 22
                out_src_port = 22
            elif proto == 'FTP':
                proto = 6
                in_dst_port = 21
                out_src_port = 21
            elif proto == 'TFTP':
                proto = 17
                in_dst_port = 69
                out_src_port = 69
            elif proto == 'HTTP':
                proto = 6
                in_dst_port = 80
                out_src_port = 80
            elif proto == 'TELNET':
                proto = 6
                in_dst_port = 23
                out_src_port = 23
            elif proto == 'DHCP':
                proto = 17
                in_dst_port = 67
                out_src_port = 67
            elif proto == 'DNS':
                proto = 17
                in_dst_port = 53
                out_src_port = 53

        if not 'out_packets' in data :
            out_packets = '\d+'
        else :
            out_packets = data['out_packets']
        
        if 'dev_id' in data :
            dev_id = data['dev_id']
            result = re.search(r"Active Sessions \(DEV: %s(.*)<Dev ID:" % dev_id, \
                data['session'], re.I|re.M|re.S)
            if result is None :
                result = re.search(r"Active Sessions \(DEV: %s(.*)varmour@vArmour" % dev_id, \
                    data['session'], re.I|re.M|re.S)
            session_bef = result.group(0)
        else :
            session_bef = data['session']
        
        # handle 'press any key to continue'
        session = re.sub(r'\n<press any key to continue, "q" to quit>','',session_bef)
    
        match_session_head = 'vsys id\s+%s,\s+policy id\s+\d+\s+\(%s\),\s+flag\s+\w+\s*proto\s+%s\s+time\s+\d+\s+offload:\s+%s\s+App:\s+%s' \
                                % (str(vsys_id), pol, proto, offload, app)
        match_session_in = '\s*i:\s+%s\s+((\(%s\)\s+)|)%s,\s+%s\s+->\s+%s,\s+%s\s+pkts:\s+%s' % \
            (int_in,int_in_ai,in_src_ip, in_src_port, in_dst_ip, in_dst_port, in_packets)
        match_session_out = '\s*o:\s+%s\s+((\(%s\)\s+)|)%s,\s+%s\s+<-\s+%s,\s+%s\s+pkts:\s+%s' % \
            (int_out,int_out_ai,out_dst_ip, out_dst_port, out_src_ip, out_src_port, out_packets)
        match_all = '%s%s%s' % (match_session_head,match_session_in,match_session_out)
    
        #check session
        userlog("DEBUG","current session is %s\n" % session)
        userlog("DEBUG","Expect session is as below \n match_all = %s" % match_all)
        
        result = re.search(r'%s%s%s' % \
            (match_session_head, match_session_in, match_session_out), \
            session, re.I|re.M|re.S)

        if result is None :
            userlog("ERROR", "Failed to check session")
            return(0)
        else :
            userlog("INFO", "Succeed to check session")
            return(1)
    
        

if __name__ == "__main__":
    import userlog
    userlog.debug = 0
    from userlog import *
    userlog("INFO","vArmour dircetor")
    dut = director("10.11.120.71")
    
    session_rt = '''
varmour@vArmour#ROOT> show session detailed-info
<Dev ID: 1>
Active Sessions (DEV: 1) : 0
-----------------------------------------------------------

------------------------vm table---------------------------


-------------------------total 0---------------------------
 <Dev ID: 2>
Active Sessions (DEV: 2) : 2
-----------------------------------------------------------
id 0x5000000000177, vsys id 1, policy id 1 (test_pol), flag 0x01c000a4
  proto 6   time    1  offload: N   App: --
  i: xe-2/0/2.2  1.1.1.2, 22 -> 2.2.2.2, 22  pkts: 1
  o: xe-3/0/2.1  1.1.1.2, 22 <- 2.2.2.2, 22  pkts: 1
id 0x5000000000178, vsys id 1, policy id 1 (test_pol), flag 0x01c000a4
  proto 6   time    1  offload: N   App: --
  i: xe-2/0/2.2  1.1.1.2, 22 -> 2.2.2.2, 22  pkts: 1
  o: xe-3/0/2.1  1.1.1.2, 22 <- 2.2.2.2, 22  pkts: 1

------------------------vm table---------------------------


-------------------------total 0---------------------------
 <Dev ID: 3>
Active Sessions (DEV: 3) : 0
-----------------------------------------------------------

------------------------vm table---------------------------


-------------------------total 0---------------------------
 <Dev ID: 4>
Active Sessions (DEV: 4) : 0
-----------------------------------------------------------

------------------------vm table---------------------------


-------------------------total 0---------------------------

varmour@vArmour#ROOT>
'''

    dut.connect()
    #session_rt = dut.get_session()
    print("\n============" + session_rt)
    print(dut.check_session({"session":session_rt,'proto':'ssh'}))
    #print(dut.check_session({"session":dut.get_session()}))
    dut.clear_session()
    dut.disconnect()
