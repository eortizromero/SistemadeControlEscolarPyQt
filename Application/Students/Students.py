# -*- coding: latin-1 -*-
# File: Students.py

from PyQt4.QtGui import (
    QWidget,
    QLabel,
    QPixmap,
    QPainter,
    QStackedWidget,
    QCalendarWidget,
    QTextEdit,
    QPushButton,
    QGridLayout
)

from PyQt4.QtCore import (
    Qt,
    QTimeLine
)


class Students(QWidget):
    def __init__(self):
        super(Students, self).__init__()
        self.setupGUI()

    def setupGUI(self):
        # Login Window
        self.setMinimumSize(800, 550)
        self.setWindowTitle("Sistema de Control Escolar")
        self.setObjectName("ventana_student")

        self.container_app = QWidget()
        self.container_app.setObjectName("container_app")

        self.container_menu = QWidget(self.container_app)
        self.container_menu.setObjectName("container_menu")

        self.button_account = QLabel(self.container_app)
        self.button_account.setGeometry(100, 30, 40, 40)
        self.button_account.setObjectName("button_account")

        stack = StackedWidget(self.container_app)
        calendar = QCalendarWidget(stack)
        calendar.setObjectName("cal")
        stack.addWidget(calendar)

        editor = QTextEdit(self.container_app)
        editor.setObjectName("edit")
        editor.setPlainText("Hello world! " * 100)
        stack.addWidget(editor)

        page1Button = QPushButton("Page 1", self.container_menu)

        page1Button.setObjectName("page1Button")
        page2Button = QPushButton("Page 2", self.container_menu)
        page2Button.setObjectName("page2Button")

        page1Button.clicked.connect(stack.setPage1)
        page2Button.clicked.connect(stack.setPage2)

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.container_app, 1, 2)

class FaderWidget(QWidget):
    def __init__(self, old_widget, new_widget):
        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


class StackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        QStackedWidget.__init__(self, parent)

    def setCurrentIndex(self, index):
        self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)

    def setPage1(self):
        self.setCurrentIndex(0)

    def setPage2(self):
        self.setCurrentIndex(1)
