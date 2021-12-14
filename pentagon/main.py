import datetime
import json
import sys
import threading
import time
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLCDNumber
from PyQt5.QtGui import QPalette, QColor, QResizeEvent, QKeyEvent, QMouseEvent, QCursor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.Qt import QThread
import requests
from bs4 import BeautifulSoup


class Example(QWidget):

    def __init__(self):
        super().__init__()
        # 文本1
        self.text = None
        self.text2 = None
        self.text3 = None
        self.palette = None
        self.button = None
        self.led = None
        self.color = '#232525'
        self.url = 'http://api.fortuneteller.janfish.cn/tests?datetime='
        self.date = '1980-01-01 00:00:00'
        self.m_flag = False
        self.m_Pos = None
        self.begin = False
        self.Timer = None
        self.times = 0
        self.maxDate = None
        self.max = None

        self.initUI()

    def initUI(self):
        self.text = QTextEdit(self)

        self.text2 = QTextEdit(self)
        self.text2.setReadOnly(True)

        self.text3 = QTextEdit(self)
        self.text3.setReadOnly(True)

        self.setUi(self.text)
        self.setUi(self.text2)
        self.setUi(self.text3)

        self.led = QLCDNumber(self)

        button = QPushButton('pentagon')
        hbox1 = QVBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.led)
        hbox1.addWidget(button)
        hbox1.addStretch(1)

        hbox = QVBoxLayout()
        hbox.addWidget(self.text2)
        hbox.addStretch(1)
        hbox.addWidget(self.text3)

        vbox = QHBoxLayout()
        vbox.addWidget(self.text)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        # 窗口设置
        self.setGeometry(300, 500, 500, 200)
        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(self.color))

        self.setPalette(self.palette)
        self.setLayout(vbox)
        self.setWindowTitle('Absolute')
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.show()
        self.config()
        button.clicked.connect(self.transition)
        self.button = button

        self.button.setStyleSheet('background-color:rgb(105,105,105)')
        self.led.setStyleSheet('background-color:rgb(35,37,37)')

        self.Timer = QTimer()
        self.Timer.timeout.connect(self.toOne)

        self.text2.append("" + self.maxDate + ':---:' + str(self.max))
        self.text3.setPlainText("" + self.maxDate + ':---:' + str(self.max))
        self.led.display(self.times)
        # self.transition()

    def setUi(self, text):
        text.setReadOnly(True)
        text.setTextBackgroundColor(QColor(self.color))
        text.setTextColor(QColor(255, 255, 255))
        text.setStyleSheet('background-color:0,0,0')
        text.palette = QPalette()
        text.palette.setBrush(QPalette.Base, QColor(self.color))
        text.setTextColor(QColor('#6E6E6E'))
        # self.text.setFontPointSize(12)
        text.setAutoFillBackground(True)
        text.setPalette(text.palette)
        text.setFrameShape(QFrame.NoFrame)
        text.verticalScrollBar().setStyleSheet("QScrollBar:vertical"
                                               "{"
                                               "width:5px;"
                                               "background:rgba(0,0,0,0%);"
                                               "margin:0px,0px,0px,0px;"
                                               "padding-top:9px;"
                                               "padding-bottom:9px;"
                                               "}"
                                               "QScrollBar::handle:vertical"
                                               "{"
                                               "width:5px;"
                                               "background:rgba(0,0,0,25%);"
                                               " border-radius:5px;"
                                               "min-height:20;"
                                               "}"
                                               "QScrollBar::handle:vertical:hover"
                                               "{"
                                               "width:5px;"
                                               "background:rgba(0,0,0,50%);"
                                               " border-radius:5px;"
                                               "min-height:20;"
                                               "}"
                                               "QScrollBar::add-line:vertical"
                                               "{"
                                               "height:9px;width:5px;"
                                               "border-image:url(:/images/a/3.png);"
                                               "subcontrol-position:bottom;"
                                               "}"
                                               "QScrollBar::sub-line:vertical"
                                               "{"
                                               "height:9px;width:5px;"
                                               "border-image:url(:/images/a/1.png);"
                                               "subcontrol-position:top;"
                                               "}"
                                               "QScrollBar::add-line:vertical:hover"
                                               "{"
                                               "height:9px;width:5px;"
                                               "border-image:url(:/images/a/4.png);"
                                               "subcontrol-position:bottom;"
                                               "}"
                                               "QScrollBar::sub-line:vertical:hover"
                                               "{"
                                               "height:9px;width:5px;"
                                               "border-image:url(:/images/a/2.png);"
                                               "subcontrol-position:top;"
                                               "}"
                                               "QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical"
                                               "{"
                                               "background:rgba(0,0,0,10%);"
                                               "border-radius:5px;"
                                               "}")

    def resizeEvent(self, event: QResizeEvent):
        width = self.size().width() - 5
        height = self.size().height()
        self.text.resize(width, height)

    def transition(self):
        if self.begin:
            self.Timer.stop()
            self.begin = False
            return
        self.begin = True
        self.Timer.setInterval(80)
        self.Timer.start()
        self.toOne()

    def toOne(self):
        ts = int(time.mktime(time.strptime(self.date, "%Y-%m-%d %H:%M:%S")))
        ts += 2 * 60 * 60
        self.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        self.times += 1
        self.led.display(self.times)

        response = requests.get(self.url + self.date)
        response = json.loads(response.text)
        attribute = response['data']['tests']['attribute']

        s = 0
        for i in attribute:
            if float(attribute[i]['val']) > 1.5:
                s += 1
        self.text.append("" + self.date + ':---:' + str(s))

        if s >= self.max:
            self.max = s
            self.maxDate = self.date
            self.text2.append("" + self.maxDate + ':---:' + str(self.max))
            self.text3.setPlainText("" + self.maxDate + ':---:' + str(self.max))

        # print(response['data']['tests']['attribute'])

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Right:
            self.setText()
        if event.key() == Qt.Key_Escape:
            # self.showMinimized()
            self.setConfig()
            quit()

    def config(self):
        with open('./config.txt', encoding='utf-8') as config:
            config = json.loads(config.readline())
            self.date = config['date']
            self.maxDate = config['maxDate']
            self.max = config['max']
            self.times = config['times']

    def setConfig(self):
        with open('./config.txt', 'w', encoding='utf-8') as config:
            da = {"date": self.date, 'maxDate': self.maxDate, 'max': self.max, "times": self.times}
            config.write(json.dumps(da))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event: QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
