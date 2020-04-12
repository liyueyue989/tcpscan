# TCP端口扫描 #

TCP/IP协议族中使用16bit的端口号，所以TCP和UDP协议一共可使用65536个端口号来传送数据，有一部分有标准功能定义。常见的TCP/IP实现所提供的的服务都用知名的1~1023之间的端口号。这些知名端口号由IANA来管理。
 
常见的tcp端口扫描是基于TCP三次握手或者四次挥手过程，常见的常见的端口扫描是基于TCP三次握手或者是四次挥手过程，常见的是发送一个TCP syn包到指定主机的指定端口，根据返回的结果判断该端口是否开放。



## 1. TCP端口扫描： ##

 （**1）TCP SYN扫描：**也称半开放扫描，该扫描类型发送一个SYN的TCP链接数据包等待响应，当返回RST数据包表示端口关闭，返回ACK表示端口开放。

 **（2）TCP NULL扫描：**TCP空扫描设置TCP的标志头为零，如果返回一个RST数据包则表示这个端口是关闭的。

 **（3）TCP FIN扫描：**TCP FIN扫描发送一个FIN数据包，请求关闭链接，等待一个个圆满的终止，如果返回RST数据包则表示该端口是关闭的。

 **（4）TCP XMAS扫描：**TCP XSMAS扫描设置PSH，FIN和URG TCP的标志位，如果返回RST数据包则表示这个端口是关闭的。
##2.实验要求##

 （1）扫描原理：

   扫描主机通过TCP/IP协议的三次握手与目标主机的指定端口建立一次完整的连接。连接由系统调用connect()开始。如果端口开放，则连接将建立成功；否则，若返回-1则表示端口关闭。

（2）设计程序满足：

    a、输入目的IP地址以及端口范围；
    
    b、设置获取的用户输入IP地址为远程IP地址
    
    c、从开始端口到结束端口依次扫描，每扫描一个端口创建一个新的套接字
    
    d、设置一个远程地址信息中的端口号为需要扫描的当前端口号
    
    e、连接到当前端口号的目的地址
    
    f、若链接成功，则输出该端口为开启状态否则关闭
    
    g、关闭套接字

    **h、采用半连接**
    
    **i、多线程提高效率**
## 3.实验代码 ##

>      import time, sys
>      import socket
>      import queue
>      import threading
>      
>      '''类PortScaner用于封装端口扫描器所具有的基本方法'''
>      
>      class PortScaner(object):
> 
>     #mulThread_PortScan 继承父类threading.Thread,主要通过重写run()方法实现多线程扫描端口
>     class mulThread_PortScan(threading.Thread):
>         def __init__(self, port_queue, ip, timeout = 3):
>             threading.Thread.__init__(self)
>             self.port_queue = port_queue#线程队列
>             self.ip = ip
>             self.timeout = timeout
>         #重写thread模块的run()方法，每一个线程用来扫描一个端口
>         def run(self):
>             #如果端口队列不为空，循环执行
>             while True:
>                 if self.port_queue.empty():
>                     break
>                 #初始化参数
>                 port = self.port_queue.get()
>                 ip  = self.ip
>                 timeout = self.timeout
>                 #创建套接字
>                 try:
>                     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
>                     s.settimeout(timeout)
>                     result_code = s.connect_ex((ip, port)) #若该端口开放则返回0
>                     if result_code == 0:
>                         sys.stdout.write( "% 6d [OPEN]\n" % port)#打印扫描结果
>                     #else:
>                         #sys.stdout.write("% 6d [CLOSED]\n" % port)#若端口关闭则不需要扫描了
>                 except Exception as e:
>                     print(e)
>                 finally:
>                     s.close()
>     #类PortScaner的一个方法用于获取带扫描的端口列表
>     def get_port_lists(self,start_port = 1, end_port = 65535):
>         if start_port >= 1 and end_port <= 65535 and start_port <= end_port:
>             return list(range(start_port, end_port+1))
>         else:
>             return list(range(1, 65535+1))
>     #提供域名转ip的功能，利用socket.gethostbyname，返回str
>     def get_ip_by_host(self, domain):
>         try:
>             return socket.gethostbyname(domain)
>         except Exception as e:
>             print("%s:%s"%(domain, e))
>        
> 
>      def main():
>         start_time = time.time() # 脚本开始执行的时间
>         myscner = PortScaner()
>     	port_queue = queue.Queue() # 使用queue模块, 线程专用
>     	thread_num = 100 # 线程数量
>     	threads = [] # 保存新线程
>     	top = None # 取端口top数
>     	#ip = "127.0.0.1" # 扫描的ip
>     	#domain="www.baidu.com"
>     	#ip=myscnerget_ip_by_host(domain)
>     	ip="117.136.22.183"
>     	port_list = myscner.get_port_lists(1,1024) # 端口列表
>     	print("开始扫描 [%s]"% ip)
>     	#print("开始扫描 %s [%s]"% (domain,ip))
>     	for port in port_list:
>     	port_queue.put(port)
>     	for t in range(thread_num):
>     	threads.append(myscner.mulThread_PortScan(port_queue, ip, timeout = 3))
>     	# 启动线程
>     	for thread in threads:
>     	thread.start()
>     	# 阻塞线程
>     	for thread in threads:
>     	thread.join()
>     	end_time = time.time() # 脚本结束执行的时间
>     	print("共扫描[%d]个端口,运行了 %3ss"%(len(port_list)-1,end_time-start_time,))
>     if __name__ == '__main__':
>     	main()

## 4.函数说明 ##

 主要框架就是**类PortScaner**，其中封装了端口扫描器所具有的基本方法和属性。其中：
**（1）类mulThread_PortScan：**

  继承父类threading.Thread,主要通过重写run()方法实现多线程扫描端口。其中，重写了run()方法，用于实100个线程同步扫描端口的功能。

**（2）方法 get_port_lists(self,start_port=1,end_port=65535):**

用于获取待扫描的端口列表，默认范围是1~65535；本次实验使用1~1023。

**（3）方法get_ip_by_host(self, domain)：**

提供域名转ip的功能，利用socket.gethostbyname，返回str
        

## 5、结果说明 ##
  由于常见的TCP/IP实现所提供的的服务都用知名的1~1023之间的端口号，故在实验时仅扫描了1~1023共1023个端口。

  依次进行了三次扫描：

**（1）对本机[127.0.0.1]进行扫描**

    结果如下：
    开始扫描[127. 0.0.1]
    135 [OPEN] 
    443 [OPEN]
    445 [OPEN]
    902 [OPEN]
    912 [OPEN]
    共扫描[1023]个端口,运行了22. 06021991958618s

**（2）对百度服务器[www.baidu.com]进行扫描**

    结果如下：
    开始扫描 www.baidu.com [220.181.38.149]
    80 [OPEN]
    443 [OPEN]
    共扫描[1023]个端口,运行了 33.275307178497314s

**(3)对本人手机设备进行扫描**

    结果如下：
    开始扫描 [117.136.22.183]
    共扫描[1023]个端口,运行了 33.11001801490784s


显然，本机开放的端口不多，其中

（1）**135端口：**主要用于使用RPC（Remote Procedure Call，远程过程调用）协议并提供DCOM（分布式组件对象模型）服务，通过RPC可以保证在一台计算机上运行的程序可以顺利地执行远程计算机上的代码；使用DCOM可以通过网络直接进行通信，能够跨包括HTTP协议在内的多种网络传输。135端口开启是存在风险的，攻击者利用RPC漏洞来攻击计算机，会导致个人信息的泄露。  

（2）**443端口**实际上就是网页浏览的端口，这个端口主要是针对HTTPS服务的。从本质上来说https服务就是能够提供加密以及通过相关的安全端口进行信息传输的HTTP。我们知道有一些网站是对安全性要求特别高的，比如涉及到银行与证券、还有购物等这些信息一般都采用HTTPS这个服务。这些网站相应的交换信息是可以防止其他人看到的，从而对交易有很好的安全性。一般情况下，都建议开启，它可以保证安全性网页的正常访问。

（3）**445端口：**445端口是一个毁誉参半的端口，有了它我们可以在局域网中轻松访问各种共享文件夹或共享打印机，但也正是因为有了它，黑客们才有了可乘之机，他们能通过该端口偷偷共享你的硬盘，甚至会在悄无声息中将你的硬盘格式化掉！我们所能做的就是想办法不让黑客有机可乘，封堵住445端口漏洞。

（4）**902端口：**用于提供VMware服务器控制台服务。

（5）**912端口：**服务未知。

另外，百度服务器开启的端口只有两个，其中**80端口号**，提供HTTP服务，主要用于上网冲浪。
