# -*- coding: latin-1 -*-
# File: Main.pyw

from PyQt4.QtGui import QApplication
from Application.Login.Login import Login
import os
r = os.getcwd()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    with open("Resource/Styles/Base.css", "r") as t:
        tema = t.read()
    login.setStyleSheet(tema)
    sys.exit(app.exec_())


