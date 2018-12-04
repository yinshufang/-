from pymysql import connect


class Opensql:
    def __init__(self, database, host="localhost", user="root", password="123456", charset="utf8", port=3306):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.port = port

    # 连接数据库
    def open(self):
        # 创建数据库连接对象db
        self.db = connect(host=self.host, user=self.user,password=self.password,database=self.database,charset=self.charset, port=self.port)
        # 创建有游标对象cur
        self.cur = self.db.cursor()

    # 关闭
    def close(self):
        self.cur.close()
        self.db.close()

    # 执行ＳＱＬ语句
    def work_on(self, sql, L=[]):
        self.open()
        try:
            self.cur.execute(sql, L)
            self.db.commit()
            print("OK")
        except Exception as e:
            self.db.rollback()
            print("Failed:", e)
        self.close()

    # 查询语句
    def get_result(self, sql, L=[]):
        self.open()

        self.cur.execute(sql, L)
        # print("OK")
        result = self.cur.fetchall()  ###是一个元组

        self.close()
        return result


# if __name__ == "__main__":
#     # 测试
#     mysql = Opensql("db4")
#     sql = input("SQL命令:")
#     # mysql.work_on(sql)
#     print(mysql.get_result(sql))
