from socket import *
from hashlib import sha1
import sys
import os
import getpass  # 隐藏密码
from time import ctime


class HTTPClient:
    def __init__(self, client_addr):
        self.client_addr = client_addr

        # 创建套接字
        self.create_socket()

    def create_socket(self):
        self.sockfd = socket()
        # 连接服务端
        self.sockfd.connect(self.client_addr)

        while True:
            a = int(input("登入1,注册2:"))
            if a == 1:
                self.login()
            elif a == 2:
                self.annotation()  # 注释

    # 输入账户函数
    def do_input(self):
        self.username = input("请输入用户名")

    # 第一次输入密码
    def do_password(self):
        self.password = getpass.getpass("请输入密码:")
        s1 = sha1()  # 把输入的密码转化成和数据库相匹配的类型
        s1.update(self.password.encode("utf-8"))  # 转码是一个字节流
        self.password = s1.hexdigest()  # 返回１６进制的结果

    # 第二次输入密码
    def do_password1(self):
        self.password1 = getpass.getpass("请再次输入密码:")
        s1 = sha1()  # 把输入的密码转化成和数据库相匹配的类型
        s1.update(self.password1.encode("utf-8"))  # 转码是一个字节流
        return s1.hexdigest()  # 返回１６进制的结果

    # 登录
    def login(self):
        self.do_input()
        self.do_password()  # 隐藏密码
        while True:
            msg = "L " + self.username + " " + self.password
            self.sockfd.send(msg.encode())
            # 接收登录结果
            data = self.sockfd.recv(1024).decode()
            if data == '登陆成功':
                print("登入成功可以开始聊天了")
                self.name = self.sockfd.recv(1024).decode()
                self.do_chat()
            elif data == "用户名不存在":
                print("用户名不存在")
                self.do_input()
                self.do_password()  # 隐藏密码
                continue
            elif data == '密码错误':
                print("密码错误")
                self.do_password()  # 隐藏密码
                continue

    # 选择二时,即为注册账号
    def annotation(self):
        name = input("请输入昵称：")
        self.do_input()
        self.do_password()
        password1 = self.do_password1()
        # 选择发送时判断msg 与 msg是否相等
        while True:
            if self.password != password1:
                print("两次密码不一样")
                self.do_password()
                password1 = self.do_password1()
                continue
            else:
                msg = "Z " + name + " " + self.username + " " + self.password
                self.sockfd.send(msg.encode())
                data = self.sockfd.recv(1024)
                data = data.decode()
                if data == "注册成功":
                    print(data)
                    break
                else:
                    print(data)
                    self.do_input()
                    self.do_password()
                    password1 = self.do_password1()
                    continue

    # 发送消息
    def do_chat(self):
        while True:
            text = input("%s):" % self.name)
            # 退出
            if text.strip() == "quit":
                sys.exit()

            msg = "C %s" % text
            self.sockfd.send(msg.encode())
            msg = self.sockfd.recv(1024)
            print("大白", ":", msg.decode())


if __name__ == '__main__':
    client_addr = ("127.0.0.1", 34191)
    httpc = HTTPClient(client_addr)
    httpc.serve_forever()
