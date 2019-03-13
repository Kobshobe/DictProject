# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 06:26:04 2019

@author: Kobs
"""
#qtui_dict.py

from PyQt5 import QtWidgets,QtCore,QtGui,sip
import sys
import qtawesome

class DictPart(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(450,60,1200,820)
        self.setMinimumSize(1200,820)

        self.all_widget = QtWidgets.QWidget()
        self.all_layout = QtWidgets.QHBoxLayout()
        self.all_layout.setContentsMargins(0,0,0,0)
        self.all_widget.setLayout(self.all_layout)
        self.setCentralWidget(self.all_widget)

        #侧边栏
        self.side_widget = QtWidgets.QWidget()
        self.side_layout = QtWidgets.QVBoxLayout()
        self.side_layout.setSpacing(0)
        self.side_layout.setAlignment(QtCore.Qt.AlignTop)
        self.side_widget.setLayout(self.side_layout)
        self.side_layout.setContentsMargins(0,0,0,0)
        self.side_logo = QtWidgets.QPushButton()
        self.side_logo.setMinimumSize(200,200)
        self.side_logo.setIcon(QtGui.QIcon('logo.png'))
        self.side_logo.setIconSize(QtCore.QSize(80,90))
        self.side_layout.addWidget(self.side_logo)

        bot = {'词  典':[],'背单词':[],'阅  读':[],'设  置':[]}
        for k,_ in bot.items():
            self.side_botton = QtWidgets.QPushButton(k)
            self.side_layout.addWidget(self.side_botton)
            self.side_botton.setMinimumHeight(70)

        #右边内容
        self.dictmain_widget = QtWidgets.QWidget()
        self.dictmain_layout = QtWidgets.QVBoxLayout()
        self.dictmain_widget.setLayout(self.dictmain_layout)
        
        #顶部部件
        self.topbar_widget = QtWidgets.QWidget()
        self.topbar_widget.setObjectName('topbar')
        self.topbar_layout = QtWidgets.QHBoxLayout()
        self.topbar_widget.setLayout(self.topbar_layout)
        self.right_close = QtWidgets.QPushButton(qtawesome.icon('fa.times'),'')
        self.right_close.setFixedSize(30,30)
        self.right_close.clicked.connect(QtWidgets.qApp.quit)
        self.right_max = QtWidgets.QPushButton(qtawesome.icon('fa.square'),'')
        self.right_max.setFixedSize(30,30)
        self.right_max.clicked.connect(self.showMaximized)
        self.right_min = QtWidgets.QPushButton(qtawesome.icon('fa.minus',weight=0.2),'')
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

        self.search_input = QtWidgets.QLineEdit('')
        self.search_input.setPlaceholderText('请输入你要查询的单词...')
        self.search_input.textEdited.connect(self.inputWord)
        self.search_button = QtWidgets.QPushButton('查   询')
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
        self.wordinfo_roll.setStyleSheet('''
            QScrollBar:vertical{background:white;width:12px;}
            QScrollBar::handle:vertical{background:#f0f1f3;border-radius:6px;}
        ''')
        self.wordinfo_roll.setWidget(self.wordinfo_widget)
        self.wordinfo_widget.setMinimumSize(50, 400)
        
        #主部件添加管理
        self.dictmain_layout.addWidget(self.topbar_widget)
        self.dictmain_layout.addWidget(self.topall_widget)
        self.dictmain_layout.addWidget(self.wordinfo_roll)
        self.dictmain_layout.setContentsMargins(10,0,10,0)
        self.dictmain_layout.setSpacing(0)

        self.all_layout.addWidget(self.side_widget)
        self.all_layout.addWidget(self.dictmain_widget)
        
        #样式设置
        self.setQss()
    def eventFilter(self,obj,event):
        if obj == self.search_input:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                self.pressLine()
                print('-----------')
        return QtWidgets.QMainWindow.eventFilter(self, obj, event)  #将事件交给上层对话

    def inputWord(self):
        try:
            self.topall_layout.removeWidget(self.wordbars_widget)
            sip.delete(self.wordbars_widget)
        except:
            pass
        dict_ = ['1','2','3','22','11']
        text = self.search_input.text()
        if text in dict_:
            print('3:'+str(text))
            self.wordbars_widget = QtWidgets.QWidget()
            self.wordbars_layout = QtWidgets.QVBoxLayout()
            self.wordbars_layout.setContentsMargins(0,0,0,0)
            self.wordbars_layout.setSpacing(0)
            self.wordbars_widget.setLayout(self.wordbars_layout)
            self.topall_layout.addWidget(self.wordbars_widget)

            self.wordbars_widget.setStyleSheet('''QPushButton:hover{background:#f0f1f4;}QPushButton{height:50px;font-family:Microsoft YaHei;}''')
            self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:1px solid #EAEAEF;}QWidget{color:black}''')

            num = lambda n:8 if n>8 else n
            for bar in range(num(int(text))):
                self.wordbar = QtWidgets.QPushButton(text, self.wordbars_widget)
                self.wordbar.setMinimumHeight(50)
                self.wordbars_layout.addWidget(self.wordbar)
            self.wordbars_widget.show()
        else:
            self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')

    def finishEdit(self):
        try:
            self.topall_layout.removeWidget(self.wordbars_widget)
            sip.delete(self.wordbars_widget)
        except:
            pass

    def clearWord(self):
        self.search_input.clear()
        self.searchbox_widget.setStyleSheet('''QWidget#input{border-bottom:none;}''')
        try:
            self.topall_layout.removeWidget(self.wordbars_widget)
            sip.delete(self.wordbars_widget)
        except:
            pass

    def setQss(self):

        self.all_widget.setStyleSheet('''
            QWidget{background:white;border:0px solid black;font-family:Microsoft YaHei;}
        ''')
        self.side_widget.setStyleSheet('''
            QWidget{background:#f4f5f8}
        ''')
        self.topall_widget.setStyleSheet('''
            QWidget#input{background:#f4f5f8;}
            QWidget#wordbars{background:#f4f5f8;}
            QLineEdit{
                background:#f4f5f8;
                background-font:qwqeq;
                height:90px;
                font-size:30px;
                colOr:gray;
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

    def test(self):
        print('ok')

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    dictpart = DictPart()
    dictpart.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()