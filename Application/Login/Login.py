# -*- coding: latin-1 -*-
# File: Login.py

from PyQt4.QtGui import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QPixmap,
    QIcon
)

from PyQt4.QtCore import (
    Qt,
    QMetaObject,
    QPropertyAnimation,
    QRect,
    QTimer,
    QEvent
)

from Application.Configs.Database import Database
from Application.Students.Students import Students

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./Resource/Images/favicon.png"))
        self.setWindowIcon(self.icon)
        self.setupGui()
        self.LoginGui()
        self.database = Database()

    def setupGui(self):
        # Login Window
        self.setMinimumSize(900, 650)
        self.setMaximumSize(900, 650)
        self.setWindowTitle("Inicia sesión | Sistema de Control Escolar")
        self.setObjectName("ventana_principal")

        # Main content
        self.widget_main = QWidget(self)
        self.widget_main.setMaximumSize(900, 650)
        self.widget_main.setMinimumSize(900, 650)
        self.widget_main.setObjectName("widget_main")

        # Label Icon Logo
        # self.label_logo = QLabel(self)
        # self.label_logo.setGeometry(415, 30, 70, 60)
        # self.label_logo.setPixmap(QPixmap("./Resource/Images/logo.png"))
        # self.label_logo.setScaledContents(True)
        # self.label_logo.setObjectName("label_logo")

    def LoginGui(self):
        # Labels
        self.label_session = QLabel(self.widget_main)
        self.label_session.setText("INICIA SESIÓN")
        self.label_session.setGeometry(350, 160, 200, 40)
        self.label_session.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.label_session.setObjectName("label_session")

        # Container Login
        self.container_login = QWidget(self.widget_main)
        self.container_login.setGeometry(200, 200, 500, 300)
        self.container_login.setObjectName("container_login")

        # Username
        self.line_username = QLineEdit(self.container_login)
        self.line_username.setPlaceholderText("USUARIO O MATRÍCULA")
        self.line_username.setGeometry(100, 60, 300, 30)
        self.line_username.setObjectName("line_username")
        self.line_username.setAcceptDrops(False)

        # Password
        self.line_password = QLineEdit(self.container_login)
        self.line_password.setPlaceholderText("CONTRASEÑA")
        self.line_password.setGeometry(100, 110, 300, 30)
        self.line_password.setEchoMode(QLineEdit.Password)
        self.line_password.setObjectName("line_password")

        # Toggle Remember
        self.checkbox_rememberme = QCheckBox(self.container_login)
        self.checkbox_rememberme.setText("recordarme")
        self.checkbox_rememberme.setLayoutDirection(Qt.RightToLeft)
        self.checkbox_rememberme.setGeometry(360, 170, 40, 20)
        self.checkbox_rememberme.setObjectName("checkbox_rememberme")

        # Label Icon Rememberme
        self.label_icon = QLabel(self.checkbox_rememberme)
        self.label_icon.setGeometry(0, 0, 20, 20)
        self.label_icon.setObjectName("label_icon")

        # Label Rememberme
        self.label_rememberme = QLabel(self.container_login)
        self.label_rememberme.setText("RECORDARME")
        self.label_rememberme.setGeometry(100, 170, 65, 20)
        self.label_rememberme.setObjectName("label_rememberme")

        # Login Button
        self.button_login = QPushButton(self.container_login)
        self.button_login.setGeometry(175, 220, 150, 30)
        self.button_login.setText("INICIAR SESIÓN")
        self.button_login.setObjectName("button_login")

        QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.line_username, self.line_password)
        self.setTabOrder(self.line_password, self.checkbox_rememberme)
        self.setTabOrder(self.checkbox_rememberme, self.button_login)

        # Button connections and widgets
        self.checkbox_rememberme.stateChanged.connect(self.rememberme)
        self.button_login.clicked[bool].connect(self.logging)
        self.line_username.returnPressed.connect(self.logging)
        self.line_password.returnPressed.connect(self.logging)

    def anim_left(self):
        animation = QPropertyAnimation(self.label_icon, "geometry")
        animation.setDuration(250)
        animation.setStartValue(QRect(0, 0, 20, 20))
        animation.setEndValue(QRect(20, 0, 20, 20))
        animation.start()

        self.animation = animation

    def anim_right(self):
        animation = QPropertyAnimation(self.label_icon, "geometry")
        animation.setDuration(250)
        animation.setStartValue(QRect(20, 0, 20, 20))
        animation.setEndValue(QRect(0, 0, 20, 20))
        animation.start()

        self.animation = animation

    def rememberme(self):
        if self.checkbox_rememberme.isChecked():
            self.anim_left()
            self.label_icon.setGeometry(20, 0, 20, 20)
        else:
            self.anim_right()
            self.label_icon.setGeometry(0, 0, 20, 20)

    def logging(self):
        username = self.line_username.text()
        password = self.line_password.text()

        if len(username) == 0:
            self.line_username.setFocus(True)
        elif len(password) == 0:
            self.line_password.setFocus(True)
        else:
            # Validate with database MySQL
            self.database.login(username, password)
            if self.database.conected:
                if self.database.account_type == "ADMINISTRADOR":
                    print("Bienvenido " + self.database.account_type)
                    # Open Admin Form
                elif self.database.account_type == "MAESTRO":
                    print("Bienvenido " + self.database.account_type)
                    # Open Maestro Form
                else:
                    # Open Alumno Form
                    print("Bienvenido " + self.database.account_type)
                    self.close()
                    with open("Resource/Styles/Base.css", "r") as t:
                        tema = t.read()
                    self.students = Students()
                    self.students.button_account.setText(username)
                    self.students.show()
                    self.students.setStyleSheet(tema)

                self.line_password.setText("")
                self.line_username.setText("")

            else:
                print("Usuario incorrecto")
                self.line_password.setText("")
                self.line_username.setText("")
                self.line_username.setFocus(True)


