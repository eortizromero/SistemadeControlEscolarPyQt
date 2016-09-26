from PyQt4.QtSql import (
    QSqlDatabase,
    QSqlQuery
)


class Database:
    def __init__(self):
        self.conected = False
        self.account_type = "ALUMNO"
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("localhost")
        db.setDatabaseName("sce_db")
        db.setUserName("root")
        db.setPassword("root")
        if db.open():
            print("Connection succeeded")

    def login(self, username, password):
        sql = "SELECT name_user, pass_user, account_type FROM users WHERE name_user =:username AND pass_user =:passwd"
        query = QSqlQuery()
        query.prepare(sql)
        query.bindValue(":username", username)
        query.bindValue(":passwd", password)
        query.exec_()
        if query.next():
            self.conected = True
            self.account_type = query.value(2).toString()






