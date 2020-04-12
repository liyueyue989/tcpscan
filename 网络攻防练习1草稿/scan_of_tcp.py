import socket
import time
import threading
import queue
import sys
#这是一个简单的扫描器
'''s=socket.socket()
s.settimeout(3)
port=int(input("请输入端口号："))
try:
    s.connect((220.181.38-150,port))
    print(s.recv(1024))#socket对象中的方法-recv():可以得到socket连接的输出信息。
    s.close()
except Exception as e:
    print("Scan Error!",e)'''
'''
#Q1:在使用域名连接远程服务器端口时出现错误，
  s.connect(('huabanta.com',22))
socket.gaierror: [Errno 11001] getaddrinfo failed
#A1:用ip地址就不会错误了。
'''
class myThread(threading.Thread):
   def __init__(self, host,port):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.host = host
      self.port = port
   def run(self):
       try:
           self.s = socket(AF_INET, SOCK_STREAM) #建立套接字
       except:
           print("Socket Error!")
           sys.exit(1)
       
       try:
           self.s.connect((self.host, self.port)) #尝试同目标端口建立正常的TCP连接
       except:  #建立连接失败 说明该端口未开放则无操作
            pass
        else:  #建立连接成功 说明该端口开放则输出端口开放的提示
            #print("%s\t%d OPEN %s" % (ctime(time()),self.port, getservbyport(self.port)))
            print("\t%d  is OPEN \tThe port's service is %s" % (self.port, getservbyport(self.port)))
            self.sk.close() #关闭套接字
#域名转ip
def get_ip_by_name(domain):
    try:
        return socket.gethostbyname()
    except Exception as e:
        print("%s:%s"%(domain, e))
#端口扫描
def Scaner(ip, port_list, timeout):
    START_MSG = ""
    result_list = list()
    for port in port_list:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s=<socket.socket fd=784, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>,socket.AF_INET=2,socket.SOCK_STREAM=1
            s.settimeout(timeout)
            result_code = s.connect_ex((ip, port)) #若该端口开放则返回0
            if result_code == 0:
                #print(OPEN_MSG % port)
                print("\t%d  is OPEN " % port)
                result_list.append(port)
            else:
                continue
        except Exception as e:
            print(e)
        finally:
            s.close()
    return result_list

#扫描的全部的端口列表,(1-65535)，返回一个包含所有开放的端口list
def allPortScan(ip, start_port = 1, end_port = 65535, timeout=3):
    port_list = range(start_port,end_port+1)
    result_list =Scaner(ip, port_list, timeout)
    return result_list
def main():
    allPortScan("127.0.0.1",1,1024)
    

    
if __name__ == '__main__':
    main()
