# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 06:26:04 2019

@author: Kobs
"""
#qtui_dict.py

from PyQt5 import QtWidgets,QtCore,QtGui,sip
import sys
#import qtawesome

class DictPart(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(250,200,960,720)
        self.setMinimumSize(960,720)
        self.dictmain_widget = QtWidgets.QWidget()
        self.dictmain_layout = QtWidgets.QVBoxLayout()
        self.dictmain_widget.setLayout(self.dictmain_layout)
        self.setCentralWidget(self.dictmain_widget)
        
        #顶部部件
        self.topbar_widget = QtWidgets.QWidget()
        self.topbar_widget.setObjectName('topbar')
        self.topbar_layout = QtWidgets.QHBoxLayout()
        self.topbar_widget.setLayout(self.topbar_layout)
        self.right_close = QtWidgets.QPushButton('')
        self.right_close.setFixedSize(30,30)
        self.right_close.clicked.connect(QtWidgets.qApp.quit)
        self.right_max = QtWidgets.QPushButton('')
        self.right_max.setFixedSize(30,30)
        self.right_max.clicked.connect(self.showMaximized)
        self.right_min = QtWidgets.QPushButton('')
        self.right_min.setFixedSize(30,30)

        self.topbar_layout.addWidget(self.right_min)
        self.topbar_layout.addWidget(self.right_max)
        self.topbar_layout.addWidget(self.right_close)
        self.topbar_layout.setAlignment(QtCore.Qt.AlignRight)
        
        #搜索框部件
        self.topall_widget = QtWidgets.QWidget()
        self.topall_layout = QtWidgets.QVBoxLayout()
        self.topall_layout.setContentsMargins(10,0,10,0)
        self.topall_layout.setSpacing(0)
        self.topall_widget.setLayout(self.topall_layout)

        self.searchbox_widget = QtWidgets.QWidget()
        self.searchbox_widget.setObjectName('input')
        self.searchbox_layout = QtWidgets.QHBoxLayout()
        self.searchbox_layout.setContentsMargins(10,0,20,1)
        self.searchbox_widget.setLayout(self.searchbox_layout)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.textEdited.connect(self.dropDownWord)
        self.search_button = QtWidgets.QPushButton('查 询')
        self.search_button.setObjectName('search_button')
        self.search_button.setFixedSize(90,40)
        self.hist_button = QtWidgets.QPushButton('')
        self.hist_button.setObjectName('search')
        self.del_button = QtWidgets.QPushButton('')
        self.del_button.setObjectName('search')
        self.del_button.clicked.connect(self.clearWord)

        self.searchbox_layout.addWidget(self.search_input)
        self.searchbox_layout.addWidget(self.del_button)
        self.searchbox_layout.addWidget(self.hist_button)
        self.searchbox_layout.addWidget(self.search_button)

        self.topall_layout.addWidget(self.searchbox_widget)
        
        #信息显示
        self.wordinfo_widget = QtWidgets.QWidget()
        self.wordinfo_layout = QtWidgets.QVBoxLayout()
        self.wordinfo_widget.setLayout(self.wordinfo_layout)
        self.wordinfo_roll = QtWidgets.QScrollArea()
        self.wordinfo_roll.setWidget(self.wordinfo_widget)
        self.wordinfo_widget.setMinimumSize(50, 400)
        
        #主部件添加管理
        self.dictmain_layout.addWidget(self.topbar_widget)
        self.dictmain_layout.addWidget(self.topall_widget)
        self.dictmain_layout.addWidget(self.wordinfo_roll)
        self.dictmain_layout.setContentsMargins(10,0,10,0)
        self.dictmain_layout.setSpacing(0)
        
        #样式设置
        self.setQss()


    def dropDownWord(self):
        dict_ = ['1','2','3','1111','18']
        text = self.search_input.text()
        try:
            self.topall_layout.removeWidget(self.wordbars_widget)
            sip.delete(self.wordbars_widget)
        except:
            pass
        if text in dict_:
            self.wordbars_widget = QtWidgets.QWidget()
            self.wordbars_layout = QtWidgets.QVBoxLayout()
            self.wordbars_layout.setContentsMargins(0,0,0,0)
            self.wordbars_layout.setSpacing(0)
            self.wordbars_widget.setLayout(self.wordbars_layout)
            self.topall_layout.addWidget(self.wordbars_widget)

            self.wordbars_widget.setStyleSheet('''QPushButton:hover{background:#f0f1f4;}QPushButton{height:50px;font-family:Microsoft YaHei;}''')
            self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:1px solid #EAEAEF;}''')

            num = lambda n:8 if n>8 else n
            for bar in range(num(int(text))):
                self.wordbar = QtWidgets.QPushButton(text, self.wordbars_widget)
                self.wordbar.setMinimumHeight(50)
                self.wordbars_layout.addWidget(self.wordbar)
            self.wordbars_widget.show()
        else:
            self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')

    def clearWord(self):
        self.search_input.clear()
        self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')
        try:
            self.wordbars_widget.hide()
        except:
            pass

    def setQss(self):

        self.dictmain_widget.setStyleSheet('''
            QWidget{
                background:white;
                border:0px solid black;
                font-family:Microsoft YaHei;
            }
        ''')
        #f7f8fa
        self.topall_widget.setStyleSheet('''
            QWidget#input{background:#f4f5f8;}
            QWidget#wordbars{background:#f4f5f8;}
            QLineEdit{
                background:#f4f5f8;
                height:90px;
                font-size:30px;
            }
            QPushButton#search_button{
                border:none;
                color:white;
                background:#d2a9ca;
                border-radius:7px;
            }
            QPushButton#search{
                height:30px;
                background:purple;
            }
            QPushButton{background:#f7f8fa;}
        ''')
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            #self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    dictpart = DictPart()
    dictpart.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()