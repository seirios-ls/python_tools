import sys
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QFrame
from PyQt5.QtGui import QPalette, QColor, QResizeEvent, QKeyEvent
from PyQt5.QtCore import Qt
import requests
from bs4 import BeautifulSoup


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.text = None
        self.palette = None
        self.document = None
        self.color = '#333333'
        self.url = 'https://www.9txs.cc'
        self.routh = '/book/61781/870898.html'

        self.initUI()

    def initUI(self):
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setTextBackgroundColor(QColor(self.color))
        self.text.setTextColor(QColor(255, 255, 255))
        self.text.setStyleSheet('background-color:0,0,0')
        self.text.palette = QPalette()
        self.text.palette.setBrush(QPalette.Base, QColor(self.color))
        self.text.setTextColor(QColor('#6E6E6E'))
        self.text.setFontPointSize(12)
        self.text.setAutoFillBackground(True)
        self.text.setPalette(self.text.palette)
        self.text.setPlainText('初始化中.....')
        self.text.setFrameShape(QFrame.NoFrame)
        self.text.move(0, 0)

        self.setGeometry(400, 500, 500, 300)
        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(self.color))

        self.setPalette(self.palette)
        self.setWindowTitle('Absolute')

        self.show()
        self.config()
        self.setText()

    def resizeEvent(self, event: QResizeEvent):
        width = self.size().width()
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

    def config(self):
        with open('./config.txt', encoding='utf-8') as config:
            self.routh = config.readline()

    def setConfig(self):
        with open('./config.txt', 'w', encoding='utf-8') as config:
            config.write(self.routh)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
