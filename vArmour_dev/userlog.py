#!/usr/bin/python3.3

def userlog__(level, msg, newline=True, stdout=False, *args):

    length = 80

    if stdout:
        if newline:
            msg_len = len(msg)
            times = int(msg_len/length)
            start = 0
            end   = length
            newMsg = ''
            for i in range(1, times+1):
                globals()['msg%s' % i] = msg[start:end] + '\n'
                start += length
                end += length
                newMsg += globals()['msg%s' % i]
            if end != msg_len:
                newMsg += msg[end-length:]
            msg = newMsg
            length = 88

        #Green
        if level == 'INFO':
            print('\033[1;32;40m')
            print('*' * length)
            print('%s    %s' % (level, msg))
            print('*' * length)
            print('\033[0m') 
        #Blue
            #Soon: comment out debug from printing on screen
        #elif level == 'DEBUG':
        #    print('\033[1;34;40m')
        #    print('*' * length)
        #    print('%s    %s' % (level, msg))
        #    print('*' * length)
        #    print('\033[0m') 
        #White
        elif level == 'NOTICE':
            print('\033[1;37;40m')
            print('*' * length)
            print('%s    %s' % (level, msg))
            print('*' * length)
            print('\033[0m') 
        #Yellow
        elif level == 'WARNING':
            print('\033[1;33;40m')
            print('*' * length)
            print('%s    %s' % (level, msg))
            print('*' * length)
            print('\033[0m') 
        #Red
        elif level == 'ERROR':
            print('\033[1;31;40m')
            print('*' * length)
            print('%s    %s' % (level, msg))
            print('*' * length)
            print('\033[0m')
    
    #Write log into file
    writeLog(level, msg)
global debug
debug = 0
global info
info = 0
def userlog(level, msg):
    if level.lower() == 'debug' and debug == 0:
        return(1)
    print("%s --> %s" %(level, msg))
