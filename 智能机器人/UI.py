
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from socket import *
import time


class denglu(QWidget):
    """
    登录窗口 ：程序的入口
    登录窗口的内容包括两个tabel标签："账号"、"密码"，两个输入框分别用来输入账号及密码
    两个按钮：确定和退出，一个radiobutton用来设置密码的显示格式，一个显示标签用来创建新的账号
    密码在输入时应该默认为掩码输入，点击radiobutton时可以切换密码显示格式
    点击显示标签"创建新用户"时弹出创建窗口
    创建新账号时应该进行核查：账号不许为空不许重复，密码不许为空
    创建完成时把账号及密码存储在本地文件中：账号.txt、密码.txt  并退出关闭创建窗口
    登录时应核查账号与密码的匹配，并根据各种出错情况给出相应的提示信息
    登陆成功时进入主页面并自动退出关闭登录窗口
    """

    def __init__(self):
        super(denglu, self).__init__()

        self.setGeometry(300, 300, 400, 247)
        # #登录窗口无边界
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # #登录窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 定义多个空label
        self.label_null1 = QLabel()
        self.label_null2 = QLabel()
        self.label_null3 = QLabel()
        self.label_null4 = QLabel()
        self.label_new = QLabel()
        # 定义创建新账户标签并设置信号槽绑定事件
        self.label_new.setText("<a href='#'>注册新用户</a>")
        self.label_new.setStyleSheet('''color: rgb(253,129,53);''')
        self.label_new.linkActivated.connect(self.idnew)
        # 设置隐藏密码RadioButton
        self.btn_check = QRadioButton("显示密码")
        self.btn_check.setStyleSheet('''color: rgb(253,129,53);;''')
        self.btn_check.clicked.connect(self.yanma)
        # 登录与退出按钮，设置按钮颜色及事件绑定
        self.btn_denglu = QPushButton("登录")
        self.btn_quxiao = QPushButton("退出")
        self.btn_denglu.setStyleSheet('''color: white;
                        background-color: rgb(218,181,150);''')
        self.btn_quxiao.setStyleSheet('''color: white;
                        background-color: rgb(218,181,150);''')
        self.btn_denglu.clicked.connect(self.check)
        self.btn_quxiao.clicked.connect(self.quxiao)
        # 账号和密码
        self.lineedit_id = QLineEdit()
        self.lineedit_id.setPlaceholderText("账号")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        self.lineedit_password.setPlaceholderText("密码")
        # 布局设置
        layout = QHBoxLayout(self)
        wid_denglu_right = QWidget()
        wid_denglu_left = QLabel()
        g = QGridLayout()
        g.addWidget(self.lineedit_id, 1, 1, 1, 2)
        g.addWidget(self.lineedit_password, 2, 1, 1, 2)
        g.addWidget(self.btn_check, 3, 1)
        g.addWidget(self.btn_denglu, 4, 1)
        g.addWidget(self.btn_quxiao, 4, 2)
        g.addWidget(self.label_null1, 5, 1)
        g.addWidget(self.label_null2, 6, 1)
        g.addWidget(self.label_null3, 7, 1)
        g.addWidget(self.label_null4, 8, 1)
        g.addWidget(self.label_new, 9, 2)
        wid_denglu_right.setLayout(g)
        layout.addWidget(wid_denglu_left)
        layout.addWidget(wid_denglu_right)
        self.setLayout(layout)
    # 密码隐藏

    def yanma(self):
        if self.btn_check.isChecked():
            self.lineedit_password.setEchoMode(QLineEdit.Normal)
        else:
            self.lineedit_password.setEchoMode(QLineEdit.Password)
    # 登录时核查账号及密码是否正确

    def check(self):
        username = self.lineedit_id.text()
        password = self.lineedit_password.text()
        msg = "L " + username + " " + password
        sockfd.send(msg.encode())
        # 接收登录结果
        data = sockfd.recv(1024).decode()
        if data == '登陆成功':
            # 账号密码验证成功，创建主界面，进入信息管理程序,并关闭登录窗口

            #----------------------------------------06647
            OnePage_glass.show()
            self.close()
            global name
            name = sockfd.recv(1024).decode()

        elif data == "用户名不存在":
            replay = QMessageBox.warning(self, "!", "账号输入错误", QMessageBox.Yes)
        elif data == "密码错误":
            replay = QMessageBox.warning(self, "!", "密码输入错误", QMessageBox.Yes)

        # 创建新的账号
    def idnew(self):
        self.label_idnew_name = QLabel("昵称")
        self.label_idnew_id = QLabel("用户名")
        self.label_idnew_password = QLabel("输入密码")
        self.label_idnew_password1 = QLabel("确认密码")
        self.lineedit_idnew_name = QLineEdit()
        self.lineedit_idnew_id = QLineEdit()
        self.lineedit_idnew_password = QLineEdit()
        self.lineedit_idnew_password1 = QLineEdit()
        self.btn_idnew_quren = QPushButton("注册")
        self.btn_idnew_quren.clicked.connect(self.idnewqueren)
        self.btn_idnew_quxiao = QPushButton("取消")
        self.btn_idnew_quxiao.clicked.connect(self.idnewclose)
        self.idnew = QWidget()
        layout_idnew = QGridLayout()
        layout_idnew.addWidget(self.label_idnew_name, 1, 0)
        layout_idnew.addWidget(self.label_idnew_id, 2, 0)
        layout_idnew.addWidget(self.label_idnew_password, 3, 0)
        layout_idnew.addWidget(self.label_idnew_password1, 4, 0)
        layout_idnew.addWidget(self.lineedit_idnew_name, 1, 1, 1, 4)
        layout_idnew.addWidget(self.lineedit_idnew_id, 2, 1, 1, 4)
        layout_idnew.addWidget(self.lineedit_idnew_password, 3, 1, 1, 4)
        layout_idnew.addWidget(self.lineedit_idnew_password1, 4, 1, 1, 4)
        layout_idnew.addWidget(self.btn_idnew_quren, 5, 1)
        layout_idnew.addWidget(self.btn_idnew_quxiao, 5, 2)
        self.idnew.setLayout(layout_idnew)
        self.idnew.move(self.pos())
        self.idnew.resize(200, 133)
        self.idnew.setWindowFlags(Qt.FramelessWindowHint)
        self.paintEvent(self)
        self.idnew.setStyleSheet("background-color :rgb(253,216,174)")
        self.idnew.show()
        # 新账号注册的确认

    def idnewqueren(self):
        name = self.lineedit_idnew_name.text()
        self.username = self.lineedit_idnew_id.text()
        password = self.lineedit_idnew_password.text()
        password1 = self.lineedit_idnew_password1.text()
        if "" in (name, self.username, password, password1):
            replay = QMessageBox.warning(self, "!", "请正确输入", QMessageBox.Yes)

        elif password != password1:
            replay = QMessageBox.warning(self, "!", "两次密码不一样", QMessageBox.Yes)
        else:
            msg = "Z " + name + " " + self.username + " " + password
            sockfd.send(msg.encode())
            data = sockfd.recv(1024)
            data = data.decode()
            if data == "注册成功":
                replay = QMessageBox.warning(
                    self, "!", "注册成功", QMessageBox.Yes)
            else:
                replay = QMessageBox.warning(
                    self, "!", "用户名已存在", QMessageBox.Yes)

    # 添加背景图片

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("2.jpg")
        painter.drawPixmap(self.rect(), pixmap)
    # 关闭创新账号窗口

    def idnewclose(self):
        self.idnew.close()
    # 取消创建新账号，并退出创建窗口

    def quxiao(self):
        sys.exit()

    def keyPressEvent(self, e):
        if str(e.key()) == '16777220' or e.key() == QtCore.Qt.Key_Enter:
            self.check()
#--------------------08651


class MukuchiChatDemo(QDialog):

    def __init__(self, parent=None):
        super(MukuchiChatDemo, self).__init__(parent)
        self.set_palette()
        # self.setWindowFlags(Qt.FramelessWindowHint)#取消边框
        self.initUI()

    def initUI(self):

        # 提示字体设置
        QToolTip.setFont(QFont('微软雅黑', 20))
        self.setToolTip('这是<b>聊天</b>窗口')

        font = QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(13)
        Lab_ne = QLabel('智能聊天机器人大白正为您服务', self)
        # 创建多行文本框
        self.textBR = QTextBrowser(self)
        self.textBR.setToolTip('这是<b>信息页面</b>')
        self.textEdit = QTextEdit(self)  # 20181016
        self.textBR.setHtml("""<body  background='bg000.jpg'>""")  # 20181016

        # 创建按钮
        setbtn = QPushButton(self.setFont(font))
        self.btnPress1 = QPushButton('发 送', self)
        self.btnPress1.setToolTip('点击这个按钮<b>发送</b>')
        self.btnPress1.setStyleSheet('background-color:rgba(0, 255,255,200)')

        # 图片素材显示20181016
        pix = QPixmap('这就是个大白.png')
        lb1 = QLabel(self)
        lb1.setToolTip('你好<b>我是大白！</b>')
        lb1.setGeometry(465, 30, 280, 401)
        lb1.setPixmap(pix)
        pix0 = QPixmap('临时广告位.gif')
        lb2 = QLabel(self)
        lb2.setToolTip('<b>达内教育</b>火热招生中')
        lb2.setGeometry(476, 440, 430, 122)
        lb2.setPixmap(pix0)
        # 退出键20181016
        b = QPushButton(self.setFont(font))
        btn_et = QPushButton('EXIT', self)
        btn_et.setToolTip('点击这个按钮<b>退出</b>')
        btn_et.setStyleSheet('background-color:rgba(70,130,180,220)')
        btn_et.clicked.connect(QCoreApplication.instance().quit)
        # 设置位置20181016
        self.textBR.setGeometry(10, 30, 450, 400)  # 聊天显示框
        self.textEdit.setGeometry(10, 440, 450, 90)  # 输入框
        self.btnPress1.setGeometry(340, 535, 121, 30)  # 发送
        btn_et.setGeometry(200, 535, 121, 30)  # 退出按钮
        Lab_ne.setGeometry(20, 2, 300, 30)  # 上端字符
        # 将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.btnPress1.clicked.connect(self.btnPress1_clicked)
        # 窗口设置
        self.setWindowIcon(QIcon('AA.png'))
        self.setWindowTitle('聊天界面')
        self.resize(750, 570)
        self.center()

    def btnPress1_clicked(self):
        # 20181016
        msg0 = self.textEdit.toPlainText()  # 接收文本框中的信息
        msg1 = "[%s]" % name
        msgtime = time.ctime()
        msg1_ch = "<font color='red' size='4'>"+msg1+"</font>"  # 处理名字
        msgtime_ch = "<font color='blue' size='2'>"+msgtime+"</font>"  # 处理时间
        msg0_ch = "<font color='MidnightBlue' size='4' style='background-color:Cyan;'>" + \
            msg0+"</font>"  # 处理信息
        msg_final = "<hr>"+msg1_ch+msgtime_ch+"<br>"+msg0_ch
        self.textBR.insertHtml(msg_final)  # 发送到显示框

        self.textEdit.clear()  # 清空输入框

        self.Alice_Glass(msg0)
#---------------------------------------

    def Alice_Glass(self, msgABC):

        msg0 = RecvMsg(msgABC)  # 接收到的信息
        msg1 = "[智能机器人大白]"
        msgtime = time.ctime()
        msg1_ch = "<font color='red' size='4'>"+msg1+"</font>"  # 处理机器人的名字
        msgtime_ch = "<font color='blue' size='2'>"+msgtime+"</font>"  # 处理时间
        msg0_ch = "<font color='MidnightBlue' size='4'>"+msg0+"</font>"  # 处理机器人的信息
        msg_final = "<hr>"+msg1_ch+msgtime_ch+"<br>"+msg0_ch

        self.textBR.insertHtml(msg_final)  # 发送到显示框
        cursor = self.textBR.textCursor()
        pos = len(self.textBR.toPlainText())
        cursor.setPosition(pos-1)
        self.textBR.ensureCursorVisible()
        self.textBR.setTextCursor(cursor)
        self.textEdit.clear()  # 清空输入框

    def btnPress2_clicked(self):
        self.textBR.clear()

    def center(self):
        # ------居中显示方法-------------
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_palette(self):
        #------------设置背景----------------------
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setBrush(self.backgroundRole(), QBrush(
            QPixmap('bg4.jpg').scaled(400, 600)))
    
        self.setPalette(palette)

    def keyPressEvent(self, e):
        if str(e.key()) == '16777220' or e.key() == QtCore.Qt.Key_Enter:
            self.btnPress1_clicked()


def RecvMsg(msg):
        #-------回复信息------
    time.sleep(0.2)
    msg = "C " + msg
    sockfd.send(msg.encode())
    msg = sockfd.recv(1024).decode()
    return msg


if __name__ == "__main__":
    client_addr = ("127.0.0.1", 34191)
    sockfd = socket()
    # 连接服务端
    sockfd.connect(client_addr)
    app = QApplication(sys.argv)
    name = ""
    d = denglu()
    OnePage_glass = MukuchiChatDemo()  # 创建聊天界面对象
    d.show()
    print(11)
    sys.exit(app.exec_())
    print(22)
