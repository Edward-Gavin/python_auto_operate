# coding = utf-8
import socket
import os
import threading
import time

lived_ip = []


# 判断本网络中的主机存活状况
def live_host(start_ip_host, ip_prefix):
    # 测试主机存活状态
    for i in range(start_ip_host, start_ip_host + 32, 1):
        host_ip = ip_prefix + str(i)
        ping_result = os.popen("ping -n 1 " + host_ip).readlines()
        if len(ping_result) == 8:
            lived_ip.append(host_ip)


def line_host(lin_number, ip_prefix):
    thread = []
    for j in range(lin_number):
        arg1 = j * (int(256 / lin_number)) + 1
        thread_line = threading.Thread(target=live_host, args=(arg1, ip_prefix,))
        thread.append(thread_line)
    for k in thread:
        k.start()


# 日志文件 format: IP  date  operate
def client_log(info_type, ipaddress, input_data):
    if info_type == "2":
        mess_type = "From of"
    elif info_type == "1":
        mess_type = "Send to"
    else:
        mess_type = "Error"
    data_format = mess_type + " " + ipaddress + " " + time.ctime() + " "+input_data + "\n"
    log_file = open("./client.log", 'a')
    log_file.writelines(data_format)
    log_file.close()


# 处理输入的IP地址，使得ip地址格式化
# 返回值：（192.168.212.0/24） 和 网络号：“192.168.212.”
def format_ip_address(ipaddress):
    prefix = '/24'
    # 判断ip地址为172.16--172.31之间的私网地址，并添加网络前缀
    if "".join((list(ipaddress)[0:3])) == "172":
        for i in range(16, 32, 1):
            if i == int("".join((list(ipaddress)[4:6]))):
                ipaddress = "".join(list(ipaddress)[0:-1]) + "0"
                ipaddress += prefix
    # 判断IP地址为192.168的私网地址，并添加网络前缀
    if "".join((list(ipaddress)[0:7])) == "192.168":
        ipaddress = "".join(list(ipaddress)[0:-1]) + "0"
        ipaddress += prefix
    # print(ipaddress)

    # 提取网络号
    raw_data = []
    for i in range(len(list(ipaddress))):
        if list(ipaddress)[i] == '.':
            raw_data.append(i)
    # print(raw_data)
    position = raw_data[-1]
    abc = "".join(list(ipaddress)[0:position + 1])
    # 返回IP地址 添加网络前缀的（192.168.212.0/24） 和 网络号：“192.168.212.”
    return ipaddress, abc


def tcp_client(server_host, server_port):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((server_host, server_port))
    while 1:
        print("Input 'man' for more Command. Input 'quit' end this connection. ")
        data = input("Please input the command:" + "(" + server_host + ")" + '>')
        if data == "man":
            man_file = open("./man.txt")
            context = man_file.readlines()
            for i in context:
                print(''.join(list(i)[0:-1]))
            man_file.close()
            continue
        else:
            clientsocket.send(data.encode())
            client_log("1", server_host, data)
            if not data:
                break
        newdata = clientsocket.recv(1024)
        client_log("2", server_host, newdata.decode())
        if newdata.decode() == "quit":
            break
        print('Received from server:', repr(newdata.decode()))
    clientsocket.close()


if __name__ == "__main__":
    server = input("Please input the server ip address:")
    port = int(input("Please input the server port:"))
    ipaddress_prefix, ipaddress_net = format_ip_address(server)
    line_host(8, ipaddress_net)
    print("Wait one minute, we are test the lived host of this net.")
    time.sleep(60)
    print("This net alive host:")
    for i in lived_ip:
        print("\t"+i)
    tcp_client(server, port)

