import socket
import select
import threading

# host = input('请输入服务器地址：')
host = '192.168.212.1'
addr = (host, 9000)


def conn():
    s = socket.socket()
    s.connect(addr)
    return s


def host_list(s):
    my = [s]
    while True:
        readable, writeable, exceptional = select.select(my, [], [])
        if s in readable:
            try:
                recvstr = s.recv(1024)
                print(recvstr.decode())
            except socket.error:
                print('socket is error')
                exit()


def host_talk(s):
    while True:
        try:
            info = input('>')
        except Exception as e:
            print('can not input')
            exit()
        try:
            s.send(info.encode())
        except Exception as e:
            print(e)
            exit()


def main():
    ss = conn()
    t = threading.Thread(target=host_list, args=(ss,))
    t.start()
    t1 = threading.Thread(target=host_talk, args=(ss,))
    t1.start()


if __name__ == '__main__':
    main()
