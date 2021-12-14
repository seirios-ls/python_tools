import sys
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QFrame,QVBoxLayout,QHBoxLayout,QPushButton
from PyQt5.QtGui import QPalette, QColor, QResizeEvent, QKeyEvent, QMouseEvent, QCursor
from PyQt5.QtCore import Qt
import requests
from bs4 import BeautifulSoup


class Example(QWidget):

    def __init__(self):
        super().__init__()
        # 文本1
        self.text = None
        self.text2 = None
        self.palette = None
        self.document = None
        self.color = '#232525'
        self.url = 'api.fortuneteller.janfish.cn/tests?datetime='
        self.routh = '1980-01-01 00:00:00'
        self.m_flag = False
        self.m_Pos = None

        self.initUI()

    def initUI(self):
        self.text = QTextEdit(self)
        # self.text.setReadOnly(True)
        self.text.setTextBackgroundColor(QColor(self.color))
        self.text.setTextColor(QColor(255, 255, 255))
        self.text.setStyleSheet('background-color:0,0,0')
        # self.text.palette = QPalette()
        # self.text.palette.setBrush(QPalette.Base, QColor(self.color))
        self.text.setTextColor(QColor('#6E6E6E'))
        self.text.setFontPointSize(12)
        button = QPushButton('五边形战士')
        # self.text.setAutoFillBackground(True)
        # self.text.setPalette(self.text.palette)
        # self.text.setPlainText('初始化中.....')
        # self.text.setFrameShape(QFrame.NoFrame)

        self.text2 = QTextEdit(self)

        vbox = QHBoxLayout()
        vbox.addWidget(self.text)
        vbox.addWidget(button)
        vbox.addStretch(1)
        vbox.addWidget(self.text2)
        # self.text.verticalScrollBar().setStyleSheet("QScrollBar:vertical"
        #                                             "{"
        #                                             "width:5px;"
        #                                             "background:rgba(0,0,0,0%);"
        #                                             "margin:0px,0px,0px,0px;"
        #                                             "padding-top:9px;"
        #                                             "padding-bottom:9px;"
        #                                             "}"
        #                                             "QScrollBar::handle:vertical"
        #                                             "{"
        #                                             "width:5px;"
        #                                             "background:rgba(0,0,0,25%);"
        #                                             " border-radius:5px;"
        #                                             "min-height:20;"
        #                                             "}"
        #                                             "QScrollBar::handle:vertical:hover"
        #                                             "{"
        #                                             "width:5px;"
        #                                             "background:rgba(0,0,0,50%);"
        #                                             " border-radius:5px;"
        #                                             "min-height:20;"
        #                                             "}"
        #                                             "QScrollBar::add-line:vertical"
        #                                             "{"
        #                                             "height:9px;width:5px;"
        #                                             "border-image:url(:/images/a/3.png);"
        #                                             "subcontrol-position:bottom;"
        #                                             "}"
        #                                             "QScrollBar::sub-line:vertical"
        #                                             "{"
        #                                             "height:9px;width:5px;"
        #                                             "border-image:url(:/images/a/1.png);"
        #                                             "subcontrol-position:top;"
        #                                             "}"
        #                                             "QScrollBar::add-line:vertical:hover"
        #                                             "{"
        #                                             "height:9px;width:5px;"
        #                                             "border-image:url(:/images/a/4.png);"
        #                                             "subcontrol-position:bottom;"
        #                                             "}"
        #                                             "QScrollBar::sub-line:vertical:hover"
        #                                             "{"
        #                                             "height:9px;width:5px;"
        #                                             "border-image:url(:/images/a/2.png);"
        #                                             "subcontrol-position:top;"
        #                                             "}"
        #                                             "QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical"
        #                                             "{"
        #                                             "background:rgba(0,0,0,10%);"
        #                                             "border-radius:5px;"
        #                                             "}")




        # 窗口设置
        self.setGeometry(400, 500, 500, 300)
        # self.palette = QPalette()
        # self.palette.setColor(self.backgroundRole(), QColor(self.color))

        # self.setPalette(self.palette)
        self.setLayout(vbox)
        # self.setWindowTitle('Absolute')
        # self.setWindowFlag(Qt.FramelessWindowHint)

        self.show()
        self.config()
        # self.setText()

    def resizeEvent(self, event: QResizeEvent):
        width = self.size().width() - 5
        height = self.size().height()
        self.text.resize(width, height)

    def setText(self):
        response = requests.get(self.url + self.routh)
        bs = BeautifulSoup(response.text, 'lxml')
        desc_items = ''.join(str(x) for x in bs.find('div', id='content').contents)
        desc_items = desc_items.replace('<p>', "")
        desc_items = desc_items.replace('</p>', "\r\n")
        title = bs.find('h1').text
        desc_items = title + "\r\n" + desc_items
        self.setConfig()

        for href in bs.find('div', class_='page').find_all('a'):
            self.routh = href['href']

        self.text.setPlainText(desc_items)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Right:
            self.setText()
        if event.key() == Qt.Key_Escape:
            # self.showMinimized()
            quit()

    def config(self):
        with open('./config.txt', encoding='utf-8') as config:
            self.routh = config.readline()

    def setConfig(self):
        with open('./config.txt', 'w', encoding='utf-8') as config:
            config.write(self.routh)

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
