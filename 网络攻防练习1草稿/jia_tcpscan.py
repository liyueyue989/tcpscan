import getopt
import threading
import sys
#from time import time,ctime
from socket import *

max_thread = 10  #设置同时在运行的线程数最多为10个

#打印正确的输入格式
def useage():
    print()
    print("Useage:")
    print("    python myscan.py -s <开始扫描端口号> -e <结束扫描端口号> -h <目的ip>")
    print()
    
class scan(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self) #实例化一个线程对象
        self.host = host
        self.port = port
        try:
            self.sk = socket(AF_INET, SOCK_STREAM) #建立套接字
        except:
            print("socket error")
            sys.exit(1)
        self.sk.settimeout(0.1) #设置超时的时间限制为0.1秒

    def run(self): #定义线程的具体操作
        try:
            self.sk.connect((self.host, self.port)) #尝试同目标端口建立正常的TCP连接
        except:  #建立连接失败 说明该端口未开放则无操作
            pass
        else:  #建立连接成功 说明该端口开放则输出端口开放的提示
            #print("%s\t%d OPEN %s" % (ctime(time()),self.port, getservbyport(self.port)))
            print("\t%d  is OPEN \tThe port's service is %s" % (self.port, getservbyport(self.port)))
            self.sk.close() #关闭套接字

class Scanner:
    def __init__(self):
        try:
            #列表sys.argv[]存储输入的参数
            opts, argvs = getopt.getopt(sys.argv[1:],"s:e:h:")
            #opts 为分析出的格式信息,是带-选项的参数
            #argvs 为不属于格式信息的剩余的命令行参数
        except getopt.GetoptError: #输入错误参数的处理
            useage()
            sys.exit(1)
                
        for opt, argv in opts:
            if opt == '-s': #-s后面的参数为开始扫描的端口号
                try:
                    self.start = int(argv)
                except ValueError: #若参数错误则打印错误信息和格式提示信息
                    print("Invaild option: -s"+argv)
                    useage()
                    sys.exit(1)
                        
            elif opt == "-e": #-e后面的参数为结束扫描的端口号
                try:
                    self.end = int(argv)
                except ValueError:
                    print("Invaild option: -e "+argv)
                    useage()
                    sys.exit(1)                        
            elif opt == "-h": #-h后面的参数为扫描目标的ip地址
                self.host = argv
        
        if self.start > self.end: #检查端口号范围是否合理
            print("Port range error")
            useage()
            sys.exit(1)

        try:
            gethostbyname(self.host)
            #返回的是 主机名（host） 的IPv4 的地址格式
            #如果传入的参数是IPv4 的地址格式，则返回值跟参数一样
            #这个函数不支持IPv6 的域名解析
        except: #无法解析则输出错误信息
            print("Hostname '%s' unknown" % self.host)
                
        self.do_scan(self.host, self.start, self.end)

    def do_scan(self, host, start, end):
        self.port = start
        while self.port <= end:
            #保证正在运行的进程数量不超过设定的最大值
            while threading.activeCount() < max_thread: 
                scan(host, self.port).start() #开始执行该线程
                self.port += 1

Scanner()
