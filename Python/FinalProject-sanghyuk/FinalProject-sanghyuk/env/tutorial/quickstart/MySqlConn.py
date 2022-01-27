#MysqlConn.py
#DB연결
import pymysql

class MySqlConn:
    username = "admin"
    passwd = "Bitbit123!"
    connection = None

    @staticmethod
    def conn():
        MySqlConn.connection = pymysql.connect(host='database-2.cmunnjma8ku1.ap-northeast-2.rds.amazonaws.com', port=3306, user='admin', password='Bitbit123!',
                                     database='david_db')
        return MySqlConn.connection

    @staticmethod
    def makeCursor():
        cursor = MySqlConn.conn().cursor()
        return cursor

    @staticmethod
    def commit():
        MySqlConn.connection.commit()

    @staticmethod
    def close():
        MySqlConn.connection.close()


