# coding=utf-8

import socket
from operate_file import *
from operate_cpu import *
from operate_disk import *
from http_server import *

# 定义字典输出的指令与可调用函数相应的关系

com_operate_cpu = {'cputime': 'cpu_time', 'cpucount': 'cpu_count',
                   'cpucountl': 'cpu_count_logical', 'virmem': 'virtual_memory',
                   'swapmem': 'swap_memory', 'users': 'users', 'boottime': 'boot_time'}

com_operate_file = {'cd': 'create_dir', 'dd': 'delete_dir', 'af': 'attrib_file',
                    'cf': 'create_file', 'df': 'delete_file'}

com_operate_disk = {'du': 'du_disk', 'df': 'df_disk'}

http_server = {'al': 'access_log', 'el': 'error_log', 'config': 'config_file',
               'hr': 'http_root', 'status': 'check_status', 'start': 'start_server',
               'stop': 'stop_server'}


# 处理服务器收到的消息的格式
def data_progress(data_in):
    data_no_blank = []
    raw_data = []
    command_list = []

    # 去除字符串中的空格
    for i in list(data_in):
        if i != ' ':
            data_no_blank.append(i)
    # print(data_no_blank)
    # print("".join(data_no_blank))

    # $字符的位置序列
    for i in range(len(list(data_no_blank))):
        if list(data_no_blank)[i] == '$':
            raw_data.append(i)
    # print(raw_data)

    # 存储所有的指令
    raw_data_start = 0
    for i in range(len(raw_data)):
        command = list(data_no_blank)[raw_data_start + 2:raw_data[i]]
        raw_data_start = raw_data[i]
        command_list.append("".join(command))
    # print(command_list)
    return data_no_blank[0], command_list


# 判断给出的操作类型，根据类型进行操作
def judge_type(date_type, command_process_list):
    if command_process_list == [''] or command_process_list == []:
        return "Command not found. "
    if int(date_type) == 1:
        print(command_process_list)
        if command_process_list[1] not in com_operate_file:
            return "Your input is illegality"
        else:
            operate_status = eval(com_operate_file[command_process_list[1]])(command_process_list)
            return operate_status
    elif int(date_type) == 2:
        print(command_process_list)
        # print(com_operate_cpu)
        if command_process_list[1] not in com_operate_cpu:
            return "Your input is illegality"
        else:
            cpu_status = eval(com_operate_cpu[command_process_list[1]])()
            return cpu_status
    elif int(date_type) == 3:
        print(command_process_list)
        # print(com_operate_disk)
        if command_process_list[1] not in com_operate_disk:
            return "Your input is illegality"
        else:
            disk_info = eval(com_operate_disk[command_process_list[1]])(command_process_list)
            return disk_info
    elif int(date_type) == 4:
        print(command_process_list)
        # print(http_server)
        if command_process_list[1] not in http_server:
            return "Your input is illegality"
        else:
            http_info = eval(http_server[command_process_list[1]])()
            return http_info
    else:
        print("wait a minute!")
        return


# 连接程序
def tcp_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('192.168.212.1', 8000))
    serversocket.listen(5)
    print("The manager server is running!")
    clientsocket, clientaddress = serversocket.accept()
    print('Connection from ', clientaddress)
    while 1:
        data = clientsocket.recv(1024)
        if not data:
            break
        if data.decode() == "quit":
            clientsocket.send(data)
            break
        print('Received from client: ', data.decode())
        data_type, command_process_list = data_progress(data.decode())
        # print('Echo: ', data_type)
        if data_type != '0':
            status_return = judge_type(data_type, command_process_list)
            status = str(status_return)
            clientsocket.send(status.encode())
        else:
            while 1:
                print("to:" + str(list(clientaddress)[0]) + " >>>")
                response_data = input()
                if response_data == "quit":
                    clientsocket.send(response_data.encode())
                    break
                clientsocket.send(response_data.encode())
                data_new = clientsocket.recv(1024)
                print("Received from client: ", data_new.decode())
                if data_new == "quit":
                    break
    clientsocket.close()
    serversocket.close()


if __name__ == "__main__":
    tcp_server()
