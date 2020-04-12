import time, sys
import socket
import queue
import threading

#类PortScaner用于封装端口扫描器所具有的基本方法
class PortScaner(object):
    #mulThread_PortScan 继承父类threading.Thread,主要通过重写run()方法实现多线程扫描端口
    class mulThread_PortScan(threading.Thread):
        def __init__(self, port_queue, ip, timeout = 3):
            threading.Thread.__init__(self)
            self.port_queue = port_queue#线程队列
            self.ip = ip
            self.timeout = timeout
        #重写thread模块的run()方法，每一个线程用来扫描一个端口
        def run(self):
            #如果端口队列不为空，循环执行
            while True:
                if self.port_queue.empty():
                    break
                #初始化参数
                port = self.port_queue.get()
                ip  = self.ip
                timeout = self.timeout
                #创建套接字
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(timeout)
                    result_code = s.connect_ex((ip, port)) #若该端口开放则返回0
                    if result_code == 0:
                        sys.stdout.write( "% 6d [OPEN]\n" % port)#打印扫描结果
                    #else:
                        #sys.stdout.write("% 6d [CLOSED]\n" % port)#若端口关闭则不需要扫描了
                except Exception as e:
                    print(e)
                finally:
                    s.close()
    #类PortScaner的一个方法用于获取带扫描的端口列表
    def get_port_lists(self,start_port = 1, end_port = 65535):
        if start_port >= 1 and end_port <= 65535 and start_port <= end_port:
            return list(range(start_port, end_port+1))
        else:
            return list(range(1, 65535+1))
    #提供域名转ip的功能，利用socket.gethostbyname，返回str
    def get_ip_by_host(self, domain):
        try:
            return socket.gethostbyname(domain)
        except Exception as e:
            print("%s:%s"%(domain, e))

def main():
    start_time = time.time() # 脚本开始执行的时间
    myscner = PortScaner()
    port_queue = queue.Queue() # 使用queue模块, 线程专用
    thread_num = 100 # 线程数量
    threads = [] # 保存新线程
    top = None # 取端口top数
    #ip = "127.0.0.1" # 扫描的ip
    #domain="www.baidu.com"
    #ip=myscnerget_ip_by_host(domain)
    ip="117.136.22.183"
    port_list = myscner.get_port_lists(1,1024) # 端口列表
    print("开始扫描 [%s]"% ip)
    #print("开始扫描 %s [%s]"% (domain,ip))
    for port in port_list:
        port_queue.put(port)
    for t in range(thread_num):
        threads.append(myscner.mulThread_PortScan(port_queue, ip, timeout = 3))
    # 启动线程
    for thread in threads:
        thread.start()
    # 阻塞线程
    for thread in threads:
        thread.join()
    end_time = time.time() # 脚本结束执行的时间
    print("共扫描[%d]个端口,运行了 %3ss"%(len(port_list),end_time-start_time,))
if __name__ == '__main__':
    main()

