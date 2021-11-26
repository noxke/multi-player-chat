import socket
import threading
import time

class ClientThread():
    def __init__(self):
        recive_thread = Recive()
        send_thread = Send()
        send_thread.start()
        recive_thread.start()
        send_thread.join()
        recive_thread.join()
        
class Send(threading.Thread):
    def run(self):
        while True:
            message = input("\n").encode()
            process.send(message)
class Recive(threading.Thread):
    def run(self):
        while True:
            date = client.recv(1024).decode()
            print("\n",date)

class Process(object):
    '任务处理模块'
    def __init__(self):
        pass

    def login(self):
        '''登录模块'''
        users = client.recv(1024).decode()
        users = users.split(' ')
        users.pop(-1)
        print("当前在线用户：\n", users)
        while True:
            print("=" * 53)
            name = input("请输入您的用户名(禁止使用/和空格)，输入/exit取消连接:\n")
            if name == '/exit':
                self.exit()
            elif ('/' in name) | (' ' in name) | (name == ''):
                print("该用户名不符合规定！请重新输入")
                print("=" * 53)
                continue
            elif name in users:
                print("该用户名已存在！请重新输入")
                print("=" * 53)
                continue
            else :
                client.sendall("{}".format(name).encode())
                time.sleep(0.2)
                print("登录成功")
                print("输入/exit退出，查看更多帮助请输入/help")
                print("=" * 54)
                break
        time.sleep(0.5)
        ClientThread()

    def send(self,date):
        '''数据发送模块'''
        client.sendall(date)
        if date.decode() == '/exit':
            self.exit()

    def exit(self):
        '''退出模块'''
        print("您正在与服务器断开连接")
        time.sleep(0.5)
        client.close()
        print("您已退出连接，即将退出程序")
        time.sleep(0.5)
        exit()

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '127.0.0.1' # 服务器地址
    server_port = 81 # 服务器端口
    client.connect((server_host, server_port))
    print("已成功连接到服务器")
    process = Process()
    process.login()