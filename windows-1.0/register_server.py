#!/usr/local/bin/python
#!-*- coding:utf-8 -
import socket
import select
import time
import os

# host = socket.gethostbyname(socket.gethostname())
host = "192.168.212.130"
port = 9000
addr = (host, port)

inputs = []
fd_name = {}


def who_in_group(w):
    name_list = []
    for k in w:
        name_list.append(w[k])
    return name_list


def connect():
    ss = socket.socket()
    ss.bind(addr)
    ss.listen(5)
    print 'The Register server is running'
    return ss


def new_comming(ss):
    client, add = ss.accept()
    print 'welcome %s %s' % (add, time.ctime()) 
    wel = 'Welcome to the manage group. Please input your name:'
    try:
        client.send(wel.encode())
        recstr = client.recv(1024)
        if recstr == "quit":
	    client.send("quit")
	    client.close()
	    ss.close()
        name = recstr.decode()
        inputs.append(client)
        fd_name[client] = name
        print fd_name
        namelist = 'Some client are in the group, these are %s' % (who_in_group(fd_name))
        server_log(time.ctime()+" "+namelist+"\n")
        client.send(namelist.encode())
        for i in (who_in_group(fd_name)):
            print i
        print namelist
    except Exception as e:
        print '1'
        print e


def server_log(data_format):
    log_file = open("./register_log.txt", 'a')
    log_file.writelines(data_format)
    log_file.close()


def server_run():
    ss = connect()
    inputs.append(ss)
    while True:
        readable, writeable, exceptional = select.select(inputs, [], [])
        for temp in readable:
            if temp is ss:
                new_comming(ss)
            else:
                disconnect = False
                try:
                    recvstr = temp.recv(1024)
		    if recvstr == "quit":
		        ss.send("quit")
                        ss.close()
                    data = recvstr.decode()
                    if recvstr.decode() == '1':
                        os.system("python tcp_client_run.py")
                        print "the tcp_client_run is running! "
                    else:
                        data = time.ctime()+" "+fd_name[temp] + ' say:' + data
                        server_log(data+"\n")
                except socket.error:
                    data = time.ctime()+" "+fd_name[temp] + ' leave the group! '
                    server_log(data+"\n")
                    disconnect = True

                if disconnect:
                    inputs.remove(temp)
                    print(data)
                    for other in inputs:
                        if other != ss and other != temp:
                            try:
                                other.send(data.encode())
                            except Exception as e:
                                print '2'
                                print e
                    del fd_name[temp]
                else:
                    print(data)
                    for other in inputs:
                        if other != ss and other != temp:
                            try:
                                other.send(data.encode())
                            except Exception as e:
                                print '3'
                                print e


if __name__ == '__main__':
    server_run()
