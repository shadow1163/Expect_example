
import re

result = '''
root@AP300_30AP027C22651:/# iwconfig
lo        no wireless extensions.

ifb0      no wireless extensions.

ifb1      no wireless extensions.

eth0      no wireless extensions.

br-lan    no wireless extensions.

wifi0     no wireless extensions.

wifi1     no wireless extensions.

ath49     IEEE 802.11b  ESSID:""
          Mode:Master  Frequency:2.412 GHz  Access Point: Not-Associated
          Bit Rate:1.0 Mb/s   Tx-Power:50 dBm
          RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
          Link Quality=94/94  Signal level=-96 dBm  Noise level=-95 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:0   Missed beacon:0

ath99     IEEE 802.11a  ESSID:""
          Mode:Master  Frequency:5.18 GHz  Access Point: Not-Associated
          Bit Rate:6.0 Mb/s   Tx-Power:31 dBm
          RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
          Link Quality=0/94  Signal level=-95 dBm  Noise level=-95 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:0  Invalid misc:0   Missed beacon:0

root@AP300_30AP027C22651:/#
'''
def list_all_dict(dict_a):
	if isinstance(dict_a,dict) :
		for x in range(len(dict_a)):
			temp_key = dict_a.keys()[x]
			temp_value = dict_a[temp_key]
			print"%s : %s" %(temp_key,temp_value)
			list_all_dict(temp_value)
			
def pretty_dict(obj, indent=' '):
    def _pretty(obj, indent):
        for i, tup in enumerate(obj.items()):
            k, v = tup
            #如果是字符串则拼上""
            if isinstance(k, basestring): k = '"%s"'% k
            if isinstance(v, basestring): v = '"%s"'% v
            #如果是字典则递归
            if isinstance(v, dict):
                v = ''.join(_pretty(v, indent + ' '* len(str(k) + ': {')))#计算下一层的indent
            #case,根据(k,v)对在哪个位置确定拼接什么
            if i == 0:#开头,拼左花括号
                if len(obj) == 1:
                    yield '{%s: %s}'% (k, v)
                else:
                    yield '{%s: %s,\n'% (k, v)
            elif i == len(obj) - 1:#结尾,拼右花括号
                yield '%s%s: %s}'% (indent, k, v)
            else:#中间
                yield '%s%s: %s,\n'% (indent, k, v)
    print ''.join(_pretty(obj, indent))

rc = re.compile('ath\d+.*?\n\s*\n',re.I|re.S)
aths = rc.findall(result)
rt = {}
for ath in aths:
	rt['result'] = result
	ath_match = re.match(r'(ath\d+).*?ESSID:"(.*?)".*?Frequency:([\d.]+) GHz.*?Tx-Power:([\d+]).*?Encryption key:([\w]+)', ath, re.M|re.I|re.S)
	if ath_match:
		ath_name = ath_match.group(1)
		#print(ath_name)
		rt[ath_name] = {}
		rt[ath_name]['result'] = ath
		#print(rt[ath_name]['result'])
		rt[ath_name]['ESSID'] = ath_match.group(2)
		rt[ath_name]['Frequency'] = ath_match.group(3)
		rt[ath_name]['Tx-Power'] = ath_match.group(4)
		rt[ath_name]['Encryption-key'] = ath_match.group(5)
	else:
		print("Error to find")

list_all_dict(rt)
#print(rt['ath49']['result'])
