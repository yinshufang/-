from socket import *
from threading import Thread
import sys
from mysql_robot import *
from Tuli import *
from hashlib import sha1


class HTTPServer(object):
    def __init__(self, server_addr):
        # 增添服务器对象属性
        self.server_address = server_addr
        self.ip = server_addr[0]
        self.port = server_addr[1]
        # 创建套接字
        self.create_socket()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self.server_address)

    # 设置监听等待客户端连接
    def serve_forever(self):
        self.sockfd.listen(5)
        print("Listen the port %d" % self.port)
        while True:
            try:
                connfd, addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit("服务器退出")
            except Exception:
                traceback.print_exc()
                continue
            # 创建新的线程处理请求
            clientThread = Thread(target=self.handleRequest, args=(connfd,))
            clientThread.setDaemon(True)
            clientThread.start()
# 用户登录

    def do_login(self, connfd, username, password):
        # 登入验证
        mysql = Opensql("user1")
        sql_select = "select password from user where username=%s"
        ss = mysql.get_result(sql_select, [username])
        if len(ss) == 0:
            msg = "用户名不存在"
            connfd.send(msg.encode())
        elif password == ss[0][0]:
            msg = "登陆成功"
            connfd.send(msg.encode())
            name = "select name from user where username=%s"
            sss = mysql.get_result(name, [username])
            connfd.send(sss[0][0].encode())
        else:
            msg = "密码错误"
            connfd.send(msg.encode())

    # 用户注册
    def do_zhuce(self, connfd, name, username, password):
        # print(name, username, password)
        # 查询用户名是否存在
        mysql = Opensql("user1")
        sql_select = "select password from user where username=%s"
        ss = mysql.get_result(sql_select, [username])
        # print(ss)  # ss是一个tuple
        # 通过判断返回元组ss的长度来判用用户名是否存在
        # 当返回值元组长度等于零时,及用户名不存在,可以注册,向客户端发送消息告知
        if len(ss) == 0:
            
            # 向数据库中插入数据账号密码
            mysql = Opensql("user1")
            sql_select = "insert into user values(null,%s,%s,%s)"
            mysql.work_on(sql_select, [name, username, password])

            msg = "注册成功"
            connfd.send(msg.encode())
        # 当返回值列表长度大于一时,及用户名以存在,向客户端发送消息告知
        else:
            msg = "用户名已存在"
            connfd.send(msg.encode())

    def do_chat(self, connfd, data, turing):
        # 将客户端传来的消息调用接口,然后将接口返回的消息转发个客户端
        # 将消息记录在文档中以便日后查看历史消息
        if "名字" in data:
            date ="你好,我叫大白"
        else:
            turing_data = turing.get_turing_text(data)
            # turing_data = "shide"
        connfd.send(turing_data.encode())
  

    # 接收客户端请求并处理
    def handleRequest(self, connfd):
        turing = TuringChatMode()
        while True:
            msg = connfd.recv(1024)
            msgList = msg.decode().split(' ')
            if msgList[0] == 'L':
                self.do_login(connfd, msgList[1], msgList[2])
            elif msgList[0] == 'C':
                # "C Levi [I miss you]"
                data = ' '.join(msgList[1:])
                self.do_chat(connfd, data, turing)
            elif msgList[0] == "Z":
                self.do_zhuce(connfd, msgList[1], msgList[2], msgList[3])


# 创建套接字，网络连接，创建父子进程


if __name__ == "__main__":
        # 服务器IP
    server_addr = ('127.0.0.1', 34191)
    # 生成对象
    httpd = HTTPServer(server_addr)
    # 启动服务器
    httpd.serve_forever()
