import threading
import socket
import time

class Server(object):
    '''创建服务器server'''
    def __init__(self, host=socket.gethostname(), port=81): # 设置服务器IP以及端口
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(listen)

class ClientThread(threading.Thread):
    '''启动新的用户线程'''
    def run(self):
        thread_list = [] # 已开启的用户线程列表
        while True:
            mutex.acquire() # 开启互斥锁，防止循环过程中用户字典发生改变
            if clients != {}:
                for name in clients:
                    if name not in thread_list: # 当有用户线程不在线程列表中时开启该线程
                        thread = clients[name][2]
                        thread.start()
                        thread_list.append(name)
                for name in thread_list:
                    if name not in clients: # 当线程列表中有不存在的线程时移除该线程（用户退出）
                        thread_list.remove(name)
            mutex.release() # 解除互斥锁
            time.sleep(0.2)

class ClientProcess(object):
    '''任务处理模块'''
    def __init__(self, name):
        self.name = name
        self.connect = clients[self.name][0]

    def send(self, date):
        '''发送数据'''
        self.connect.sendall(date)
        print("已向{}发送一条数据".format(self.name))

    def recive(self):
        '''接收到数据后处理'''
        date = self.connect.recv(1024)
        print("从{}接收到一条数据".format(self.name))
        if date.decode() == '/exit':
            time.sleep(0.2)
            self.exit()
        else:
            return(date)

    def exit(self):
        '''与客户端断开连接'''
        message = "{},您正在与服务器断开连接".format(self.name).encode()
        self.send(message)
        self.connect.close()
        clients.pop(self.name,print(end='')) # 从用户字典中删除退出的用户
        print("{}断开与服务器连接".format(self.name))
        message = "Server：{}退出聊天".format(self.name)
        group_send(message)

class AcceptClient(threading.Thread):
    '''接受新用户线程'''
    def run(self):
        global clients
        clients = {} # 创建用户字典{用户名：用户连接，IP地址，用户线程}
        while True:
            print("等待客户端连接")
            connect, address = server.accept()
            print("{}已连接".format(address))
            names = ''
            if len(clients) == 0:
                names = "暂无在线用户 "
            else:
                for name in clients:
                    name = str(name)
                    names = names + name + ' '
            connect.sendall(names.encode())
            name = connect.recv(1024).decode()
            if name == '':
                print("{}未连接".format(address))
                continue
            thread = threading.Thread(target=client_thread, args=(name,)) # 为新用户创建线程
            clients[name] = (connect, address, thread)
            print("{}的用户名为：{}".format(address, name))

def client_thread(name):
    '''用户进程'''
    print("成功创建{}线程".format(name))
    message = "Server：{}加入服务器".format(name) # 向全部用户发送新用户上线提醒
    group_send(message)
    user_list = []
    for user_name in clients:
        user_list.append(user_name)
    message = "当前在线用户：{}".format(user_list)
    group_send(message)
    while True:
        if name not in clients:
            break
        client = ClientProcess(name)
        date = client.recive() # 接收到数据后群发该数据
        message = name + '：' + date.decode()
        group_send(message)

def group_send(message:str):
    '''群发功能'''
    for name in clients:
            client = ClientProcess(name)
            client.send(message.encode())

if __name__ == "__main__":
    #listen = int(input("最大客户端连接数："))
    listen = 10
    Server() # 实例化服务器
    mutex = threading.Lock() # 互斥锁
    accept_client = AcceptClient() # 接收用户线程
    client_threads = ClientThread() # 总用户线程
    accept_client.start()
    client_threads.start()
    accept_client.join()
    client_threads.join()