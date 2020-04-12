# nmap模块常用方法说明 #
####选中一行的快捷键home-shift+end;选中多行的快捷键 home-+Ctrl+shift+end####
## 1、PortScanner()类常用方法 ##
**（1）scan()方法**

 **scan(self, hosts='127.0.0.1', ports=None, arguments='-sV')方法，**

  实现指定主机、端口、namp命令行参数的扫描。参数hosts为字符串类型，表示扫描的主机地址，格式可以用"scanme.nmap.org"、"192.116.0-255.1-127"、"216.163.128.20/20"表示; 参数ports为字符串类型，表示扫描的端口,可以用"22,53,110,143-4564"表示;参数namp命令行参数，格式为"-sU -sX -sC"，例如：

> nm = nmap.PortScanner()
>  
> nm.scan('192.168.209.121-122', '22,80')

**(2)command_line()方法**

**command_line(self)方法,返回的扫描方法映射到具体的nmap命令行，如：**
>nm.command_line()
>
>u'nmap -oX - -p 22,80 -sV 192.168.209.121-122

**(3)scaninfo()方法**

**scaninfo(self)方法，返回nmap扫描信息，格式为字典类型，如：**
> nm.scanninfo()
> 
> {'tcp':{'services':'22,80', 'method':'syn'}}

**（4）all_hosts()方法**

**all_hosts(self)方法，返回nmap扫描的主机清单，格式为列表类型，例如：**

> ['192.168.209.121', '192.168.209.122']
## 2、PortScannerHostDict()类常用方法 ##
**（1）hostname()方法**


**hostname(self)方法，返回扫描对象的主机名，如：**
> nm['192.168.209.121'].hostname()
> 
> liuyazhuang'


**（2）state()方法**

**state(self)方法,返回扫描对象的状态，包括4中状态(up、down、unknown、skipped)，如：**
>  nm['192.168.209.121'].state()
>  
> 'up'

**（3）all_protocols()方法**
**all_protocols(self)方法，返回扫描的协议，如:**
> nm['192.168.209.121'].all_protocols()
> 
> ['tcp']

**（4）all_tcp()方法**
**all_tcp(self)方法，返回TCP协议扫描的端口，如：**
> nm['192.168.209.121'].all_tcp()
> 
> [22,80]

**（5）tcp()方法**

**tcp(self, port)方法，返回扫描TCP协议port(端口)的信息,如:**

> nm['192.168.209.121'].tcp(22)
> 
> {'state':'open', 'reason':'syn-ack', 'name':'ssh'}
> 
